#!/usr/bin/env python3
"""
build_index.py — генерирует index/*.index.json из data/.

Запускается:
  • автоматически через GitHub Action (workflow update-index.yml)
  • вручную: python scripts/build_index.py

Что делает:
  1. Проходит по каждой папке в data/<type>/.
  2. Читает <type>.json внутри.
  3. Строит <type>.index.json — плоский список сущностей.
  4. Собирает manifest.json — общий указатель на все индексы.
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
INDEX_DIR = ROOT / "index"
VERSION_FILE = ROOT / "VERSION"


# Описание типов данных.
# file     — имя JSON-файла внутри папки сущности
# idKey    — поле с ID
# nameKey  — поле с отображаемым именем
# extras   — какие дополнительные поля тащить в индекс
DATA_TYPES = {
    "characters": {
        "file": "character.json",
        "idKey": "id",
        "nameKey": "name",
        "extras": ["worldId", "familyId", "variant", "tags", "y"],
    },
    "abilities": {
        "file": "ability.json",
        "idKey": "id",
        "nameKey": "name",
        "extras": ["tags", "type"],
    },
    "roles": {
        "file": "role.json",
        "idKey": "id",
        "nameKey": "name",
        "extras": [],
    },
    "scenarios": {
        "file": "scenario.json",
        "idKey": "id",
        "nameKey": "name",
        "extras": [],
    },
    "tags": {
        "file": "tag.json",
        "idKey": "id",
        "nameKey": "name",
        "extras": ["category", "color"],
    },
    "worlds": {
        "file": "world.json",
        "idKey": "id",
        "nameKey": "name",
        "extras": ["physicality", "compatibleWith"],
    },
    "axes": {
        "file": "axis.json",
        "idKey": "id",
        "nameKey": "name",
        "extras": ["isCustom"],
    },
}


def read_version() -> str:
    if not VERSION_FILE.exists():
        return "0.0.0"
    return VERSION_FILE.read_text(encoding="utf-8").strip()


def iter_items(type_dir: Path, filename: str):
    """Пройти по папкам внутри type_dir и вернуть (folder_name, json_data)."""
    if not type_dir.exists():
        return
    for folder in sorted(type_dir.iterdir()):
        if not folder.is_dir():
            continue
        json_file = folder / filename
        if not json_file.exists():
            print(f"  ⚠ skip: {folder.name} — нет {filename}", file=sys.stderr)
            continue
        try:
            with json_file.open(encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"  ✗ invalid JSON: {json_file} — {e}", file=sys.stderr)
            continue
        yield folder.name, data


def build_index_for(type_name: str, cfg: dict) -> dict:
    """Построить index для одного типа данных."""
    type_dir = DATA_DIR / type_name
    entries = []

    for folder_name, data in iter_items(type_dir, cfg["file"]):
        entry = {
            "folder": folder_name,
            "id": data.get(cfg["idKey"]),
            "name": data.get(cfg["nameKey"]),
            "path": f"data/{type_name}/{folder_name}/{cfg['file']}",
        }

        # Иконка, если есть.
        icon = type_dir / folder_name / "icon.png"
        entry["iconPath"] = (
            f"data/{type_name}/{folder_name}/icon.png"
            if icon.exists()
            else None
        )

        # Дополнительные поля по типу.
        for key in cfg.get("extras", []):
            if key in data:
                entry[key] = data[key]

        entries.append(entry)

    return {
        "version": read_version(),
        "type": type_name,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "count": len(entries),
        "items": entries,
    }


def main() -> int:
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    version = read_version()

    manifest = {
        "version": version,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "indices": {},
    }

    print(f"[build_index] VERSION={version}")
    total = 0

    for type_name, cfg in DATA_TYPES.items():
        index = build_index_for(type_name, cfg)
        out_path = INDEX_DIR / f"{type_name}.index.json"

        with out_path.open("w", encoding="utf-8") as f:
            json.dump(index, f, ensure_ascii=False, indent=2)

        manifest["indices"][type_name] = {
            "path": f"index/{type_name}.index.json",
            "count": index["count"],
        }
        total += index["count"]
        print(f"  ✓ {type_name}: {index['count']} items")

    with (INDEX_DIR / "manifest.json").open("w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"[build_index] Готово. Всего {total} записей.")
    print(f"[build_index] manifest → index/manifest.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())