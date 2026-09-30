#!/usr/bin/env python3
"""
migrate.py — применяет миграции схемы к данным в data/.

Запускается:
  • вручную: python scripts/migrate.py
  • с флагом --dry-run — показать, что будет изменено, не трогая файлы

Как работает:
  1. Читает VERSION (текущая версия схемы).
  2. Для каждой миграции из MIGRATIONS, где from_version == текущая,
     применяет функцию ко всем файлам нужного типа.
  3. Обновляет VERSION.
  4. Пишет изменения в файлы.

Как добавить миграцию:
  • Пишете функцию transform(type_name, data) -> dict | None.
    • Возвращает изменённый dict — если что-то поменяли.
    • Возвращает None — если нужно пропустить.
  • Регистрируете её в MIGRATIONS.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Callable, Optional


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
VERSION_FILE = ROOT / "VERSION"


# ==== Тип: имя папки → имя JSON-файла внутри ====
TYPE_FILES = {
    "characters": "character.json",
    "abilities":  "ability.json",
    "roles":      "role.json",
    "scenarios":  "scenario.json",
    "tags":       "tag.json",
    "worlds":     "world.json",
    "axes":       "axis.json",
}


# ==== Функции миграции ====
#
# Каждая принимает (type_name, data) и возвращает:
#   - dict — обновлённые данные
#   - None — пропустить (не трогать файл)

def migrate_1_0_0_to_1_1_0(type_name: str, data: dict) -> Optional[dict]:
    """
    Пример: добавляет поле worldId к персонажам.
    Значение по умолчанию — "unknown".
    """
    if type_name != "characters":
        return None
    if "worldId" in data:
        return None
    data = dict(data)
    data["worldId"] = "unknown"
    return data


def migrate_1_0_0_to_1_1_0_add_family(type_name: str,
                                        data: dict) -> Optional[dict]:
    """
    Пример: добавляет familyId = slug от name для персонажей.
    """
    if type_name != "characters":
        return None
    if "familyId" in data:
        return None
    name = (data.get("name") or "").strip().lower()
    slug = "".join(c if c.isalnum() else "_" for c in name) or "unknown"
    data = dict(data)
    data["familyId"] = slug
    return data


# ==== Реестр миграций ====
# Формат: target_version -> {"from": from_version, "fns": [f1, f2, ...]}
#
# Каждая миграция применяется ко ВСЕМ файлам указанных типов.
# Если f возвращает None — файл не трогается.
MIGRATIONS = {
    "1.1.0": {
        "from": "1.0.0",
        "fns": [migrate_1_0_0_to_1_1_0, migrate_1_0_0_to_1_1_0_add_family],
    },
    # "1.2.0": {
    #     "from": "1.1.0",
    #     "fns": [migrate_1_1_0_to_1_2_0],
    # },
}


def read_version() -> str:
    if not VERSION_FILE.exists():
        return "0.0.0"
    return VERSION_FILE.read_text(encoding="utf-8").strip()


def write_version(v: str) -> None:
    VERSION_FILE.write_text(v + "\n", encoding="utf-8")


def iter_data_files():
    """Пройти по всем (type_name, folder, json_path)."""
    for type_name, json_name in TYPE_FILES.items():
        type_dir = DATA_DIR / type_name
        if not type_dir.exists():
            continue
        for folder in sorted(type_dir.iterdir()):
            if not folder.is_dir():
                continue
            json_file = folder / json_name
            if json_file.exists():
                yield type_name, folder, json_file


def apply_migration(
    version: str,
    fns: list[Callable],
    dry_run: bool,
) -> int:
    """
    Применить набор функций миграции ко всем файлам.
    Возвращает количество изменённых файлов.
    """
    changed = 0

    for type_name, folder, json_file in iter_data_files():
        try:
            with json_file.open(encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"  ✗ {json_file}: сломанный JSON — {e}", file=sys.stderr)
            continue

        modified = False
        for fn in fns:
            result = fn(type_name, data)
            if result is not None and result != data:
                data = result
                modified = True

        if not modified:
            continue

        changed += 1
        rel = json_file.relative_to(ROOT)
        print(f"  {'would update' if dry_run else 'update'}: {rel}")

        if not dry_run:
            with json_file.open("w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description="Migrate data schema")
    parser.add_argument("--dry-run", action="store_true",
                        help="Показать, что будет изменено, не трогая файлы")
    parser.add_argument("--to", type=str, default=None,
                        help="Целевая версия (по умолчанию — последняя "
                             "из MIGRATIONS)")
    args = parser.parse_args()

    current = read_version()
    print(f"[migrate] Текущая версия: {current}")

    if not MIGRATIONS:
        print("[migrate] Нет зарегистрированных миграций.")
        return 0

    # Сортируем ключи (версии) лексикографически по семантике.
    def vkey(v: str):
        return tuple(int(x) for x in v.split("."))

    targets = sorted(MIGRATIONS.keys(), key=vkey)
    if args.to:
        targets = [t for t in targets if vkey(t) <= vkey(args.to)]

    applied_any = False

    for target in targets:
        info = MIGRATIONS[target]
        if info["from"] != current:
            continue
        print(f"[migrate] {current} → {target}")
        n = apply_migration(target, info["fns"], args.dry_run)
        print(f"[migrate] изменено файлов: {n}")
        if not args.dry_run:
            write_version(target)
        current = target
        applied_any = True

    if not applied_any:
        print("[migrate] Нечего применять — версия актуальна.")
        return 0

    if args.dry_run:
        print("[migrate] (dry-run, файлы не изменены)")

    return 0


if __name__ == "__main__":
    sys.exit(main())