#!/usr/bin/env python3
"""
validate.py — проверяет все JSON в data/ против соответствующих схем.

Запускается:
  • автоматически в GitHub Action при push/PR
  • вручную: python scripts/validate.py

Возвращает exit code 0, если всё валидно, и 1, если есть ошибки.
"""

import json
import sys
from pathlib import Path

try:
    import jsonschema
    from jsonschema import Draft7Validator
except ImportError:
    print("✗ Не установлен jsonschema. Запустите:", file=sys.stderr)
    print("  pip install -r scripts/requirements.txt", file=sys.stderr)
    sys.exit(2)


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
SCHEMA_DIR = ROOT / "schema"


# Соответствие: имя папки в data/ → файл схемы + имя json-файла внутри
TYPE_MAP = {
    "characters": ("character.schema.json", "character.json"),
    "abilities":  ("ability.schema.json",   "ability.json"),
    "roles":      ("role.schema.json",      "role.json"),
    "scenarios":  ("scenario.schema.json",  "scenario.json"),
    "tags":       ("tag.schema.json",       "tag.json"),
    "worlds":     ("world.schema.json",     "world.json"),
    "axes":       ("axis.schema.json",      "axis.json"),
}


def load_schemas() -> dict:
    """Загрузить все схемы и построить общий $ref-store."""
    schemas = {}
    store = {}
    for schema_file in SCHEMA_DIR.glob("*.json"):
        try:
            with schema_file.open(encoding="utf-8") as f:
                data = json.load(f)
            schemas[schema_file.name] = data
            if "$id" in data:
                store[data["$id"]] = data
        except json.JSONDecodeError as e:
            print(f"✗ Схема повреждена: {schema_file.name}: {e}",
                  file=sys.stderr)
            sys.exit(2)
    return schemas, store


def validate_folder(
    folder: Path,
    json_name: str,
    schema: dict,
    store: dict,
    errors: list,
) -> bool:
    """Проверить один файл. Возвращает True, если валидно."""
    json_file = folder / json_name
    if not json_file.exists():
        errors.append(f"  ✗ {folder.name}: нет {json_name}")
        return False

    try:
        with json_file.open(encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f"  ✗ {folder.name}: сломанный JSON — {e}")
        return False

    validator = Draft7Validator(schema, resolver=None)
    # Простой резолвер ref'ов через store
    from jsonschema import RefResolver
    validator = Draft7Validator(
        schema,
        resolver=RefResolver.from_schema(schema, store=store),
    )

    ok = True
    for err in sorted(validator.iter_errors(data), key=lambda e: e.path):
        path = " → ".join(str(p) for p in err.path) or "(root)"
        errors.append(f"  ✗ {folder.name}: [{path}] {err.message}")
        ok = False

    return ok


def main() -> int:
    if not DATA_DIR.exists():
        print("✗ Нет папки data/", file=sys.stderr)
        return 1
    if not SCHEMA_DIR.exists():
        print("✗ Нет папки schema/", file=sys.stderr)
        return 1

    schemas, store = load_schemas()
    print(f"[validate] Загружено схем: {len(schemas)}")

    total_ok = 0
    total_err = 0
    all_errors = []

    for type_name, (schema_name, json_name) in TYPE_MAP.items():
        schema = schemas.get(schema_name)
        if schema is None:
            print(f"⚠ Нет схемы {schema_name} для типа {type_name}")
            continue

        type_dir = DATA_DIR / type_name
        if not type_dir.exists():
            continue

        type_errors = []
        for folder in sorted(type_dir.iterdir()):
            if not folder.is_dir():
                continue
            if validate_folder(folder, json_name, schema, store,
                               type_errors):
                total_ok += 1
            else:
                total_err += 1
                all_errors.extend(type_errors[-len([
                    e for e in type_errors
                ]):] if False else [])

        if type_errors:
            print(f"\n[{type_name}] ошибок: {len(type_errors)}")
            for e in type_errors:
                print(e)
            all_errors.extend(type_errors)
        else:
            count = sum(
                1 for f in type_dir.iterdir()
                if f.is_dir()
            )
            if count:
                print(f"  ✓ {type_name}: {count} записей валидны")

    print(f"\n[validate] Итог: {total_ok} ok, {total_err} с ошибками")

    if all_errors:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())