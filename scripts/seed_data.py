#!/usr/bin/env python3
"""
seed_data.py — базовый набор данных: Jujutsu Kaisen.

Создаёт:
  • 20 персонажей
  • 1 мир (Jujutsu Kaisen)
  • ~20 способностей
  • стандартные роли / сценарии / оси

Идемпотентен: существующие папки не перезаписываются.

Запуск:
    python scripts/seed_data.py
    python scripts/build_index.py
"""

import json
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

NS = uuid.UUID("12345678-1234-5678-1234-567812345678")


def make_uuid(type_name: str, name: str) -> str:
    return str(uuid.uuid5(NS, f"{type_name}:{name}"))


def slug(name: str) -> str:
    s = name.lower().replace(" ", "_")
    return "".join(c if c.isalnum() or c == "_" else "_" for c in s)


def axes_to_dict(values):
    keys = ["a", "aMin", "aMax", "bMax", "bMin"]
    return dict(zip(keys, values))


# ============================================================================
# ПЕРСОНАЖИ JJK
# ============================================================================

CHARACTERS = [
    # 1. Сатору Годжо — Special Grade, сильнейший
    {
        "name": "Сатору Годжо", "y": 0.9,
        "worldId": "jujutsu_kaisen",
        "familyId": "gojo", "variant": "Awakened",
        "tags": ["jujutsu_high", "special_grade", "gojo_clan"],
        "axes": {
            "str":   [30, 20, 45, 90, 10],
            "spd":   [75, 65, 85, 95, 5],
            "acc":   [70, 55, 85, 92, 8],
            "stam":  [85, 70, 100, 95, 5],
            "dur":   [90, 80, 100, 95, 5],
            "ctrl":  [80, 65, 95, 88, 12],
            "ment":  [40, 25, 60, 75, 25],
            "sens":  [75, 60, 90, 88, 12],
            "heal":  [70, 50, 90, 85, 15],
            "supp":  [70, 55, 85, 82, 18],
            "intel": [80, 65, 95, 90, 10],
            "util":  [85, 75, 95, 92, 8],
            "range": [85, 75, 95, 90, 10],
            "aoe":   [80, 65, 95, 88, 12],
        },
    },
    # 2. Рёмен Сукуна
    {
        "name": "Рёмен Сукуна", "y": 0.7,
        "worldId": "jujutsu_kaisen",
        "familyId": "sukuna", "variant": "Heian Era",
        "tags": ["cursed_spirit", "king_of_curses"],
        "axes": {
            "str":   [35, 25, 50, 90, 10],
            "spd":   [70, 60, 80, 92, 8],
            "acc":   [65, 50, 80, 88, 12],
            "stam":  [90, 80, 100, 95, 5],
            "dur":   [75, 60, 90, 90, 10],
            "ctrl":  [85, 70, 100, 92, 8],
            "ment":  [60, 40, 80, 85, 15],
            "sens":  [65, 50, 80, 85, 15],
            "heal":  [75, 60, 90, 88, 12],
            "supp":  [40, 25, 60, 75, 25],
            "intel": [90, 80, 100, 95, 5],
            "util":  [90, 80, 100, 95, 5],
            "range": [80, 65, 90, 88, 12],
            "aoe":   [85, 70, 100, 90, 10],
        },
    },
    # 3. Юдзи Итадори
    {
        "name": "Юдзи Итадори", "y": 0.6,
        "worldId": "jujutsu_kaisen",
        "familyId": "itadori", "variant": "Shibuya",
        "tags": ["jujutsu_high", "vessel"],
        "axes": {
            "str":   [35, 25, 50, 85, 15],
            "spd":   [45, 35, 55, 85, 15],
            "acc":   [40, 30, 50, 80, 20],
            "stam":  [70, 55, 85, 88, 12],
            "dur":   [45, 35, 55, 82, 18],
            "ctrl":  [25, 15, 35, 60, 30],
            "ment":  [30, 20, 40, 65, 33],
            "sens":  [35, 25, 45, 70, 30],
            "heal":  [55, 40, 70, 82, 18],
            "supp":  [35, 20, 50, 70, 30],
            "intel": [40, 25, 55, 70, 30],
            "util":  [55, 40, 70, 85, 15],
            "range": [25, 18, 35, 70, 30],
            "aoe":   [35, 25, 50, 75, 25],
        },
    },
    # 4. Мегуми Фушигуро
    {
        "name": "Мегуми Фушигуро", "y": 0.6,
        "worldId": "jujutsu_kaisen",
        "familyId": "fushiguro", "variant": "Shibuya",
        "tags": ["jujutsu_high", "zenin"],
        "axes": {
            "str":   [28, 18, 40, 80, 20],
            "spd":   [50, 40, 60, 85, 15],
            "acc":   [45, 35, 55, 82, 18],
            "stam":  [60, 45, 75, 82, 18],
            "dur":   [30, 20, 40, 75, 25],
            "ctrl":  [50, 35, 65, 80, 20],
            "ment":  [35, 25, 45, 70, 30],
            "sens":  [50, 35, 65, 80, 20],
            "heal":  [40, 25, 55, 78, 22],
            "supp":  [55, 40, 70, 82, 18],
            "intel": [70, 55, 85, 88, 12],
            "util":  [75, 60, 90, 88, 12],
            "range": [60, 45, 75, 82, 18],
            "aoe":   [55, 40, 70, 80, 20],
        },
    },
    # 5. Нобара Кугисаки
    {
        "name": "Нобара Кугисаки", "y": 0.5,
        "worldId": "jujutsu_kaisen",
        "familyId": "kugisaki", "variant": "Shibuya",
        "tags": ["jujutsu_high"],
        "axes": {
            "str":   [25, 15, 35, 78, 22],
            "spd":   [40, 30, 50, 80, 20],
            "acc":   [35, 25, 45, 75, 25],
            "stam":  [55, 40, 70, 80, 20],
            "dur":   [28, 18, 38, 75, 25],
            "ctrl":  [35, 25, 45, 70, 30],
            "ment":  [30, 20, 40, 65, 33],
            "sens":  [30, 20, 40, 68, 32],
            "heal":  [35, 20, 50, 72, 28],
            "supp":  [40, 25, 55, 75, 25],
            "intel": [45, 30, 60, 75, 25],
            "util":  [60, 45, 75, 85, 15],
            "range": [45, 30, 60, 78, 22],
            "aoe":   [40, 25, 55, 75, 25],
        },
    },
    # 6. Маки Зенин
    {
        "name": "Маки Зенин", "y": 0.6,
        "worldId": "jujutsu_kaisen",
        "familyId": "zenin", "variant": "Awakened",
        "tags": ["jujutsu_high", "zenin"],
        "axes": {
            "str":   [35, 25, 45, 82, 18],
            "spd":   [45, 35, 55, 82, 18],
            "acc":   [45, 35, 55, 80, 20],
            "stam":  [65, 50, 80, 85, 15],
            "dur":   [35, 25, 45, 78, 22],
            "ctrl":  [30, 20, 40, 68, 32],
            "ment":  [25, 15, 35, 60, 30],
            "sens":  [35, 25, 45, 70, 30],
            "heal":  [20, 10, 30, 60, 30],
            "supp":  [40, 25, 55, 72, 28],
            "intel": [55, 40, 70, 80, 20],
            "util":  [55, 40, 70, 82, 18],
            "range": [40, 30, 50, 72, 28],
            "aoe":   [35, 25, 45, 70, 30],
        },
    },
    # 7. Тоге Инумаки
    {
        "name": "Тоге Инумаки", "y": 0.5,
        "worldId": "jujutsu_kaisen",
        "familyId": "inumaki", "variant": "Shibuya",
        "tags": ["jujutsu_high", "inumaki_clan"],
        "axes": {
            "str":   [18, 10, 25, 70, 30],
            "spd":   [35, 25, 45, 78, 22],
            "acc":   [40, 30, 50, 78, 22],
            "stam":  [45, 30, 60, 75, 25],
            "dur":   [20, 12, 28, 68, 32],
            "ctrl":  [50, 35, 65, 82, 18],
            "ment":  [35, 25, 45, 72, 28],
            "sens":  [30, 20, 40, 68, 32],
            "heal":  [15,  8, 22, 55, 28],
            "supp":  [55, 40, 70, 80, 20],
            "intel": [55, 40, 70, 82, 18],
            "util":  [70, 55, 85, 88, 12],
            "range": [55, 40, 70, 78, 22],
            "aoe":   [50, 35, 65, 78, 22],
        },
    },
    # 8. Панда
    {
        "name": "Панда", "y": 0.5,
        "worldId": "jujutsu_kaisen",
        "familyId": "panda", "variant": "Shibuya",
        "tags": ["jujutsu_high", "cursed_corpse"],
        "axes": {
            "str":   [40, 30, 50, 82, 18],
            "spd":   [35, 25, 45, 75, 25],
            "acc":   [35, 25, 45, 75, 25],
            "stam":  [70, 55, 85, 85, 15],
            "dur":   [55, 40, 70, 82, 18],
            "ctrl":  [30, 20, 40, 68, 32],
            "ment":  [25, 15, 35, 60, 30],
            "sens":  [30, 20, 40, 65, 33],
            "heal":  [30, 20, 40, 70, 30],
            "supp":  [35, 20, 50, 70, 30],
            "intel": [35, 25, 45, 68, 32],
            "util":  [45, 30, 60, 75, 25],
            "range": [30, 20, 40, 65, 33],
            "aoe":   [30, 20, 40, 68, 32],
        },
    },
    # 9. Кенто Нанами
    {
        "name": "Кенто Нанами", "y": 0.6,
        "worldId": "jujutsu_kaisen",
        "familyId": "nanami", "variant": "Grade 1",
        "tags": ["jujutsu_high", "grade_1"],
        "axes": {
            "str":   [25, 15, 35, 78, 22],
            "spd":   [40, 30, 50, 80, 20],
            "acc":   [45, 35, 55, 80, 20],
            "stam":  [60, 45, 75, 82, 18],
            "dur":   [30, 20, 40, 75, 25],
            "ctrl":  [45, 30, 60, 78, 22],
            "ment":  [45, 30, 60, 78, 22],
            "sens":  [35, 25, 45, 70, 30],
            "heal":  [25, 15, 35, 65, 33],
            "supp":  [45, 30, 60, 75, 25],
            "intel": [65, 50, 80, 85, 15],
            "util":  [60, 45, 75, 82, 18],
            "range": [50, 35, 65, 78, 22],
            "aoe":   [45, 30, 60, 78, 22],
        },
    },
    # 10. Сугуру Гето
    {
        "name": "Сугуру Гето", "y": 0.6,
        "worldId": "jujutsu_kaisen",
        "familyId": "geto", "variant": "Curse User",
        "tags": ["curse_user", "special_grade"],
        "axes": {
            "str":   [28, 18, 40, 80, 20],
            "spd":   [55, 45, 65, 85, 15],
            "acc":   [55, 45, 65, 85, 15],
            "stam":  [70, 55, 85, 88, 12],
            "dur":   [35, 25, 45, 78, 22],
            "ctrl":  [70, 55, 85, 88, 12],
            "ment":  [55, 40, 70, 85, 15],
            "sens":  [55, 40, 70, 82, 18],
            "heal":  [55, 40, 70, 82, 18],
            "supp":  [65, 50, 80, 85, 15],
            "intel": [85, 75, 95, 92,  8],
            "util":  [85, 70, 100, 92, 8],
            "range": [70, 55, 85, 85, 15],
            "aoe":   [65, 50, 80, 82, 18],
        },
    },
    # 11. Махито
    {
        "name": "Махито", "y": 0.6,
        "worldId": "jujutsu_kaisen",
        "familyId": "mahito", "variant": "Full Power",
        "tags": ["cursed_spirit", "special_grade"],
        "axes": {
            "str":   [30, 20, 40, 78, 22],
            "spd":   [60, 50, 70, 88, 12],
            "acc":   [50, 40, 60, 82, 18],
            "stam":  [80, 65, 95, 90, 10],
            "dur":   [75, 60, 90, 88, 12],
            "ctrl":  [65, 50, 80, 82, 18],
            "ment":  [70, 55, 85, 85, 15],
            "sens":  [55, 40, 70, 80, 20],
            "heal":  [80, 65, 95, 90, 10],
            "supp":  [30, 20, 40, 65, 33],
            "intel": [55, 40, 70, 80, 20],
            "util":  [85, 70, 100, 92, 8],
            "range": [55, 40, 70, 80, 20],
            "aoe":   [65, 50, 80, 82, 18],
        },
    },
    # 12. Джого
    {
        "name": "Джого", "y": 0.5,
        "worldId": "jujutsu_kaisen",
        "familyId": "jogo", "variant": "Shibuya",
        "tags": ["cursed_spirit", "special_grade", "disaster"],
        "axes": {
            "str":   [30, 20, 40, 78, 22],
            "spd":   [55, 45, 65, 85, 15],
            "acc":   [45, 35, 55, 80, 20],
            "stam":  [75, 60, 90, 88, 12],
            "dur":   [50, 40, 60, 82, 18],
            "ctrl":  [55, 40, 70, 80, 20],
            "ment":  [40, 25, 55, 75, 25],
            "sens":  [45, 30, 60, 75, 25],
            "heal":  [30, 20, 40, 65, 33],
            "supp":  [35, 20, 50, 70, 30],
            "intel": [45, 30, 60, 75, 25],
            "util":  [80, 65, 95, 90, 10],
            "range": [70, 55, 85, 85, 15],
            "aoe":   [75, 60, 90, 88, 12],
        },
    },
    # 13. Хана
    {
        "name": "Хана", "y": 0.5,
        "worldId": "jujutsu_kaisen",
        "familyId": "hanami", "variant": "Shibuya",
        "tags": ["cursed_spirit", "special_grade", "disaster"],
        "axes": {
            "str":   [28, 18, 38, 75, 25],
            "spd":   [45, 35, 55, 80, 20],
            "acc":   [40, 30, 50, 78, 22],
            "stam":  [75, 60, 90, 88, 12],
            "dur":   [55, 40, 70, 82, 18],
            "ctrl":  [55, 40, 70, 80, 20],
            "ment":  [35, 25, 45, 70, 30],
            "sens":  [45, 30, 60, 75, 25],
            "heal":  [75, 60, 90, 88, 12],
            "supp":  [40, 25, 55, 72, 28],
            "intel": [35, 25, 45, 68, 32],
            "util":  [75, 60, 90, 88, 12],
            "range": [65, 50, 80, 82, 18],
            "aoe":   [70, 55, 85, 85, 15],
        },
    },
    # 14. Дагон
    {
        "name": "Дагон", "y": 0.5,
        "worldId": "jujutsu_kaisen",
        "familyId": "dagon", "variant": "Shibuya",
        "tags": ["cursed_spirit", "special_grade", "disaster"],
        "axes": {
            "str":   [28, 18, 38, 75, 25],
            "spd":   [55, 45, 65, 85, 15],
            "acc":   [45, 35, 55, 80, 20],
            "stam":  [75, 60, 90, 88, 12],
            "dur":   [50, 40, 60, 82, 18],
            "ctrl":  [65, 50, 80, 85, 15],
            "ment":  [45, 30, 60, 75, 25],
            "sens":  [45, 30, 60, 75, 25],
            "heal":  [30, 20, 40, 65, 33],
            "supp":  [35, 20, 50, 70, 30],
            "intel": [40, 30, 50, 70, 30],
            "util":  [80, 65, 95, 88, 12],
            "range": [70, 55, 85, 85, 15],
            "aoe":   [75, 60, 90, 88, 12],
        },
    },
    # 15. Чосо
    {
        "name": "Чосо", "y": 0.5,
        "worldId": "jujutsu_kaisen",
        "familyId": "kamo", "variant": "Death Painting",
        "tags": ["cursed_womb", "death_painting"],
        "axes": {
            "str":   [25, 15, 35, 75, 25],
            "spd":   [45, 35, 55, 78, 22],
            "acc":   [35, 25, 45, 72, 28],
            "stam":  [55, 40, 70, 78, 22],
            "dur":   [35, 25, 45, 75, 25],
            "ctrl":  [40, 25, 55, 70, 30],
            "ment":  [35, 25, 45, 70, 30],
            "sens":  [35, 25, 45, 70, 30],
            "heal":  [30, 20, 40, 65, 33],
            "supp":  [35, 20, 50, 70, 30],
            "intel": [60, 45, 75, 82, 18],
            "util":  [60, 45, 75, 82, 18],
            "range": [55, 40, 70, 78, 22],
            "aoe":   [55, 40, 70, 78, 22],
        },
    },
    # 16. Юта Оккоцу
    {
        "name": "Юта Оккоцу", "y": 0.7,
        "worldId": "jujutsu_kaisen",
        "familyId": "okkotsu", "variant": "Special Grade",
        "tags": ["jujutsu_high", "special_grade"],
        "axes": {
            "str":   [28, 18, 38, 78, 22],
            "spd":   [60, 50, 70, 85, 15],
            "acc":   [55, 40, 70, 82, 18],
            "stam":  [85, 70, 100, 92, 8],
            "dur":   [50, 40, 60, 82, 18],
            "ctrl":  [65, 50, 80, 82, 18],
            "ment":  [55, 40, 70, 80, 20],
            "sens":  [55, 40, 70, 80, 20],
            "heal":  [80, 65, 95, 90, 10],
            "supp":  [60, 45, 75, 82, 18],
            "intel": [70, 55, 85, 85, 15],
            "util":  [85, 70, 100, 92, 8],
            "range": [70, 55, 85, 85, 15],
            "aoe":   [70, 55, 85, 85, 15],
        },
    },
    # 17. Хакари Кинджи
    {
        "name": "Хакари Кинджи", "y": 0.6,
        "worldId": "jujutsu_kaisen",
        "familyId": "hakari", "variant": "Jackpot",
        "tags": ["jujutsu_high", "suspended"],
        "axes": {
            "str":   [35, 25, 45, 80, 20],
            "spd":   [50, 40, 60, 82, 18],
            "acc":   [40, 30, 50, 78, 22],
            "stam":  [80, 65, 95, 90, 10],
            "dur":   [45, 35, 55, 80, 20],
            "ctrl":  [35, 25, 45, 70, 30],
            "ment":  [35, 25, 45, 70, 30],
            "sens":  [35, 25, 45, 70, 30],
            "heal":  [70, 55, 85, 85, 15],
            "supp":  [30, 20, 40, 65, 33],
            "intel": [45, 30, 60, 75, 25],
            "util":  [70, 55, 85, 88, 12],
            "range": [45, 30, 60, 72, 28],
            "aoe":   [50, 35, 65, 75, 25],
        },
    },
    # 18. Аой Тодо
    {
        "name": "Аой Тодо", "y": 0.5,
        "worldId": "jujutsu_kaisen",
        "familyId": "todo", "variant": "Kyoto",
        "tags": ["jujutsu_high", "grade_1"],
        "axes": {
            "str":   [40, 30, 50, 82, 18],
            "spd":   [45, 35, 55, 80, 20],
            "acc":   [40, 30, 50, 78, 22],
            "stam":  [65, 50, 80, 82, 18],
            "dur":   [40, 30, 50, 78, 22],
            "ctrl":  [45, 30, 60, 75, 25],
            "ment":  [35, 25, 45, 70, 30],
            "sens":  [40, 30, 50, 72, 28],
            "heal":  [20, 10, 30, 60, 30],
            "supp":  [65, 50, 80, 85, 15],
            "intel": [70, 55, 85, 85, 15],
            "util":  [60, 45, 75, 80, 20],
            "range": [40, 30, 50, 72, 28],
            "aoe":   [40, 30, 50, 72, 28],
        },
    },
    # 19. Момо Нишимия
    {
        "name": "Момо Нишимия", "y": 0.4,
        "worldId": "jujutsu_kaisen",
        "familyId": "nishimiya", "variant": "Kyoto",
        "tags": ["jujutsu_high"],
        "axes": {
            "str":   [15,  8, 22, 65, 33],
            "spd":   [35, 25, 45, 72, 28],
            "acc":   [35, 25, 45, 72, 28],
            "stam":  [40, 30, 50, 70, 30],
            "dur":   [18, 10, 25, 60, 30],
            "ctrl":  [40, 30, 50, 72, 28],
            "ment":  [30, 20, 40, 65, 33],
            "sens":  [35, 25, 45, 68, 32],
            "heal":  [20, 10, 30, 58, 30],
            "supp":  [45, 30, 60, 75, 25],
            "intel": [55, 40, 70, 78, 22],
            "util":  [50, 35, 65, 75, 25],
            "range": [45, 30, 60, 72, 28],
            "aoe":   [40, 30, 50, 70, 30],
        },
    },
    # 20. Мэй Мэй
    {
        "name": "Мэй Мэй", "y": 0.6,
        "worldId": "jujutsu_kaisen",
        "familyId": "mei_mei", "variant": "Grade 1",
        "tags": ["jujutsu_high", "grade_1", "mercenary"],
        "axes": {
            "str":   [20, 12, 28, 68, 32],
            "spd":   [40, 30, 50, 75, 25],
            "acc":   [60, 45, 75, 85, 15],
            "stam":  [55, 40, 70, 78, 22],
            "dur":   [25, 15, 35, 70, 30],
            "ctrl":  [55, 40, 70, 80, 20],
            "ment":  [40, 25, 55, 72, 28],
            "sens":  [45, 30, 60, 75, 25],
            "heal":  [25, 15, 35, 62, 30],
            "supp":  [45, 30, 60, 75, 25],
            "intel": [60, 45, 75, 82, 18],
            "util":  [70, 55, 85, 85, 15],
            "range": [80, 65, 95, 90, 10],
            "aoe":   [60, 45, 75, 80, 20],
        },
    },
]


# ============================================================================
# РОЛИ / СЦЕНАРИИ / ОСИ (универсальные)
# ============================================================================

ROLES = [
    {"name": "Боец", "weights": {
        "str": 2.0, "spd": 1.5, "acc": 1.2, "stam": 1.0, "dur": 1.8,
        "ctrl": 0.8, "ment": 1.0, "sens": 1.0, "heal": 0.3, "supp": 0.1,
        "intel": 1.0, "util": 1.0, "range": 1.5, "aoe": 1.5,
    }},
    {"name": "Контролёр", "weights": {
        "str": 0.3, "spd": 1.2, "acc": 0.8, "stam": 0.8, "dur": 0.3,
        "ctrl": 2.5, "ment": 1.8, "sens": 1.0, "heal": 0.3, "supp": 0.1,
        "intel": 1.5, "util": 1.0, "range": 1.2, "aoe": 1.2,
    }},
    {"name": "Медик", "weights": {
        "str": 0.2, "spd": 2.0, "acc": 0.2, "stam": 1.5, "dur": 1.0,
        "ctrl": 0.5, "ment": 0.5, "sens": 1.0, "heal": 2.5, "supp": 2.5,
        "intel": 0.3, "util": 1.0, "range": 0.0, "aoe": 0.5,
    }},
    {"name": "Разведчик", "weights": {
        "str": 0.0, "spd": 2.0, "acc": 2.0, "stam": 1.0, "dur": 0.6,
        "ctrl": 1.0, "ment": 1.0, "sens": 2.5, "heal": 0.0, "supp": 0.0,
        "intel": 1.2, "util": 1.0, "range": 1.5, "aoe": 1.0,
    }},
    {"name": "Координатор", "weights": {
        "str": 0.2, "spd": 1.0, "acc": 0.2, "stam": 0.5, "dur": 0.2,
        "ctrl": 0.8, "ment": 1.5, "sens": 1.5, "heal": 0.2, "supp": 2.5,
        "intel": 4.0, "util": 1.0, "range": 2.0, "aoe": 1.5,
    }},
    {"name": "Универсал", "weights": {
        "str": 1.0, "spd": 1.0, "acc": 1.0, "stam": 1.0, "dur": 1.0,
        "ctrl": 1.0, "ment": 1.0, "sens": 1.0, "heal": 1.0, "supp": 1.0,
        "intel": 1.0, "util": 1.0, "range": 1.0, "aoe": 1.0,
    }},
]


SCENARIOS = [
    {
        "name": "Дуэль",
        "decayCurve": 0.4,
        "axisWeights": None,
    },
    {
        "name": "Разведка",
        "decayCurve": 0.4,
        "axisWeights": {
            "str": 0.4, "spd": 1.4, "acc": 0.3, "stam": 1.4, "dur": 0.1,
            "ctrl": 1.6, "ment": 1.7, "sens": 2.0, "heal": 0.2, "supp": 0.4,
            "intel": 1.6, "range": 1.6, "aoe": 0.4,
        },
    },
    {
        "name": "Открытый бой",
        "decayCurve": 0.4,
        "axisWeights": {
            "spd": 2.0, "aoe": 2.0, "acc": 1.5, "stam": 1.3, "dur": 1.5,
            "ment": 0.6, "sens": 0.5, "heal": 0.5, "intel": 0.5, "range": 2.0,
        },
    },
    {
        "name": "Осада",
        "decayCurve": 0.4,
        "axisWeights": {
            "stam": 2.0, "ctrl": 2.0, "supp": 2.0, "heal": 2.0,
            "str": 0.7, "spd": 0.7, "acc": 0.1, "dur": 2.0,
            "sens": 0.2, "intel": 1.5, "range": 0.4, "aoe": 0.4,
        },
    },
    {
        "name": "Война",
        "decayCurve": 0.4,
        "axisWeights": {
            "ctrl": 2.0, "ment": 2.0, "sens": 2.0,
            "str": 0.4, "spd": 1.4, "acc": 0.4, "stam": 1.2,
            "heal": 1.3, "supp": 1.2, "intel": 1.5,
            "range": 0.6, "aoe": 0.6, "dur": 0.6,
        },
    },
]


AXES = [
    {"name": "Сила",         "id_key": "str",   "order": 1,  "desc": "Физический урон, пробитие"},
    {"name": "Скорость",     "id_key": "spd",   "order": 2,  "desc": "Реакция, передвижение, атака"},
    {"name": "Точность",     "id_key": "acc",   "order": 3,  "desc": "Попадание по цели"},
    {"name": "Выносливость", "id_key": "stam",  "order": 4,  "desc": "Длительность боя"},
    {"name": "Прочность",    "id_key": "dur",   "order": 5,  "desc": "Сопротивление урону"},
    {"name": "Контроль",     "id_key": "ctrl",  "order": 6,  "desc": "Барьеры, зоны, доминирование"},
    {"name": "Ментальное",   "id_key": "ment",  "order": 7,  "desc": "Телепатия, внушение, иллюзии"},
    {"name": "Сенсорика",    "id_key": "sens",  "order": 8,  "desc": "Обнаружение, радар, восприятие"},
    {"name": "Лечение",      "id_key": "heal",  "order": 9,  "desc": "Восстановление себя и союзников"},
    {"name": "Поддержка",    "id_key": "supp",  "order": 10, "desc": "Баффы, командная синергия"},
    {"name": "Интеллект",    "id_key": "intel", "order": 11, "desc": "Планирование, тактика, адаптация"},
    {"name": "Полезные",     "id_key": "util",  "order": 12, "desc": "Прочие способности"},
    {"name": "Дальность",    "id_key": "range", "order": 13, "desc": "Дистанция атаки"},
    {"name": "AoE",          "id_key": "aoe",   "order": 14, "desc": "Площадь поражения"},
]


# ============================================================================
# МИР JJK
# ============================================================================

WORLDS = [
    {
        "name": "Jujutsu Kaisen",
        "creators": ["Gege Akutami"],
        "physicality": "hybrid",
        "powerSource": "cursed_energy",
        "powerScaleMax": 85,
        "rules": {
            "canBeAffectedBy": ["physical", "cursed_energy", "spiritual"],
            "immuneTo": ["pure_physical_by_nonsorcerer"],
        },
        "compatibility": {
            "jujutsu_kaisen": {"compatible": "same",
                               "note": "Тот же мир"},
            "naruto": {"compatible": "compatible",
                       "note": "Оба используют энергию; маги видят духов"},
            "bleach": {"compatible": "requires_hax",
                       "note": "Требуется способность видеть духов"},
            "onepiece": {"compatible": "requires_hax",
                         "note": "Проклятые духи невидимы для обычных"},
        },
    },
]


# ============================================================================
# СПОСОБНОСТИ JJK
# ============================================================================

ABILITIES = [
    {
        "name": "Безграничность",
        "description": "Пространственный барьер между пользователем и целью. "
                       "Ничто не может коснуться его, если он того не хочет.",
        "type": "innate_technique",
        "tags": [
            {"tagId": "buff", "aspectValues": {
                "target": "self", "buffedAxis": "dur",
                "bonus": 50, "durationType": "toggle"}},
            {"tagId": "utility", "aspectValues": {
                "effectKind": "teleport",
                "note": "Управляет бесконечностью пространства"}},
        ],
    },
    {
        "name": "Шесть Глаз",
        "description": "Врождённая техника клана Годжо. Позволяет воспринимать "
                       "проклятую энергию в идеальной точности.",
        "type": "innate_technique",
        "tags": [
            {"tagId": "buff", "aspectValues": {
                "target": "self", "buffedAxis": "sens",
                "bonus": 40, "durationType": "passive"}},
            {"tagId": "buff", "aspectValues": {
                "target": "self", "buffedAxis": "acc",
                "bonus": 30, "durationType": "passive"}},
        ],
    },
    {
        "name": "Красный (Reversal Red)",
        "description": "Обратная техника. Отталкивающая сила, усиленная "
                       "инверсией проклятой энергии.",
        "type": "innate_technique",
        "tags": [
            {"tagId": "damage", "aspectValues": {
                "power": 80, "damageType": "energy",
                "ignoresDefense": True}},
            {"tagId": "ranged", "aspectValues": {
                "meters": 100, "projectileSpeed": 90}},
            {"tagId": "aoe", "aspectValues": {
                "radiusMeters": 50, "shape": "circle"}},
        ],
    },
    {
        "name": "Пустой Фиолетовый (Hollow Purple)",
        "description": "Совмещение Синего и Красного. Аннигилирует всё на пути.",
        "type": "innate_technique",
        "tags": [
            {"tagId": "damage", "aspectValues": {
                "power": 95, "damageType": "conceptual",
                "ignoresDefense": True}},
            {"tagId": "ranged", "aspectValues": {
                "meters": 500, "projectileSpeed": 95}},
            {"tagId": "aoe", "aspectValues": {
                "radiusMeters": 200, "shape": "line"}},
        ],
    },
    {
        "name": "Домен: Бесконечная Пустота",
        "description": "Домен Годжо. Заставляет цель воспринимать бесконечный "
                       "поток информации — паралич на всю жизнь.",
        "type": "domain_expansion",
        "tags": [
            {"tagId": "control", "aspectValues": {
                "controlType": "stun", "targets": 100,
                "durationSeconds": 9999}},
            {"tagId": "aoe", "aspectValues": {
                "radiusMeters": 500, "shape": "circle"}},
            {"tagId": "cooldown", "aspectValues": {
                "turns": 1, "description": "Один раз в день, большая цена"}},
        ],
    },
    {
        "name": "Расщепление (Cleave)",
        "description": "Техника Сукуны. Разрезает цель в зависимости от её "
                       "прочности и проклятой энергии.",
        "type": "innate_technique",
        "tags": [
            {"tagId": "damage", "aspectValues": {
                "power": 85, "damageType": "energy",
                "ignoresDefense": True}},
            {"tagId": "melee", "aspectValues": {"reachMeters": 5}},
        ],
    },
    {
        "name": "Рассечение (Dismantle)",
        "description": "Метательные разрезы Сукуны. Поражают на расстоянии.",
        "type": "innate_technique",
        "tags": [
            {"tagId": "damage", "aspectValues": {
                "power": 80, "damageType": "energy",
                "ignoresDefense": True}},
            {"tagId": "ranged", "aspectValues": {
                "meters": 100, "projectileSpeed": 85}},
        ],
    },
    {
        "name": "Десять Теней",
        "description": "Врождённая техника клана Зенин. Призыв теневых "
                       "шикигами через руки.",
        "type": "innate_technique",
        "tags": [
            {"tagId": "summon", "aspectValues": {
                "summonedType": "шикигами", "count": 10,
                "durationMinutes": 60}},
            {"tagId": "chakra_cost", "aspectValues": {
                "description": "растёт с числом призванных",
                "percentOfPool": 30}},
        ],
    },
    {
        "name": "Маhорага",
        "description": "Сильнейший шикигами Десяти Теней. Адаптируется "
                       "к любой технике после первого попадания.",
        "type": "innate_technique",
        "tags": [
            {"tagId": "summon", "aspectValues": {
                "summonedType": "шикигами", "count": 1,
                "durationMinutes": 30}},
            {"tagId": "buff", "aspectValues": {
                "target": "self", "buffedAxis": "dur",
                "bonus": 60, "durationType": "temporary"}},
            {"tagId": "cooldown", "aspectValues": {
                "turns": 30,
                "description": "требует ритуала полного раскрытия"}},
        ],
    },
    {
        "name": "Проклятая речь",
        "description": "Техника клана Инумаки. Слова становятся приказами, "
                       "которые нельзя ослушаться.",
        "type": "innate_technique",
        "tags": [
            {"tagId": "control", "aspectValues": {
                "controlType": "mind_control", "targets": 3,
                "durationSeconds": 30}},
            {"tagId": "debuff", "aspectValues": {
                "target": "group", "debuffedAxis": "spd",
                "penalty": 30, "durationType": "temporary"}},
            {"tagId": "chakra_cost", "aspectValues": {
                "description": "сильно нагружает горло",
                "percentOfPool": 20}},
        ],
    },
    {
        "name": "Резонанс",
        "description": "Техника Нобары. Через куклу вуду наносит урон, "
                       "связанный с частью тела цели.",
        "type": "innate_technique",
        "tags": [
            {"tagId": "damage", "aspectValues": {
                "power": 60, "damageType": "spiritual",
                "ignoresDefense": True}},
            {"tagId": "ranged", "aspectValues": {
                "meters": 10000, "projectileSpeed": 40}},
            {"tagId": "chakra_cost", "aspectValues": {
                "description": "требует часть тела цели",
                "percentOfPool": 15}},
        ],
    },
    {
        "name": "Идле Трансфигурэйшн",
        "description": "Техника Махито. Изменяет форму души любого существа.",
        "type": "innate_technique",
        "tags": [
            {"tagId": "damage", "aspectValues": {
                "power": 80, "damageType": "conceptual",
                "ignoresDefense": True}},
            {"tagId": "heal", "aspectValues": {
                "amount": 90, "targets": "self",
                "curesStatuses": True}},
            {"tagId": "melee", "aspectValues": {"reachMeters": 5}},
        ],
    },
    {
        "name": "Буги-Вуги (Boogie Woogie)",
        "description": "Техника Тодо. Мгновенный обмен позициями двух "
                       "объектов с проклятой энергией.",
        "type": "innate_technique",
        "tags": [
            {"tagId": "utility", "aspectValues": {
                "effectKind": "teleport",
                "note": "хлопок в ладоши меняет местами любые две цели"}},
            {"tagId": "cooldown", "aspectValues": {
                "turns": 1, "description": "ограничена хлопком"}},
        ],
    },
    {
        "name": "Пропорция 7:3",
        "description": "Техника Нанами. Слабые точки противника делятся "
                       "по пропорции 7:3, попадание в них критично.",
        "type": "innate_technique",
        "tags": [
            {"tagId": "damage", "aspectValues": {
                "power": 75, "damageType": "physical",
                "ignoresDefense": True}},
            {"tagId": "melee", "aspectValues": {"reachMeters": 2}},
            {"tagId": "chakra_cost", "aspectValues": {
                "description": "средний расход",
                "percentOfPool": 20}},
        ],
    },
    {
        "name": "Манипуляция кровью",
        "description": "Техника Чосо. Управляет собственной кровью как "
                       "оружием и снарядом.",
        "type": "innate_technique",
        "tags": [
            {"tagId": "damage", "aspectValues": {
                "power": 65, "damageType": "energy",
                "ignoresDefense": True}},
            {"tagId": "ranged", "aspectValues": {
                "meters": 50, "projectileSpeed": 60}},
            {"tagId": "aoe", "aspectValues": {
                "radiusMeters": 20, "shape": "circle"}},
        ],
    },
    {
        "name": "Рика",
        "description": "Особый проклятый дух Юты. Меняет форму и силу "
                       "по желанию хозяина.",
        "type": "special",
        "tags": [
            {"tagId": "summon", "aspectValues": {
                "summonedType": "проклятый дух", "count": 1,
                "durationMinutes": 999}},
            {"tagId": "buff", "aspectValues": {
                "target": "self", "buffedAxis": "str",
                "bonus": 40, "durationType": "toggle"}},
            {"tagId": "buff", "aspectValues": {
                "target": "self", "buffedAxis": "heal",
                "bonus": 30, "durationType": "toggle"}},
        ],
    },
    {
        "name": "Домен Хакари (Idle Death Gamble)",
        "description": "Домен Хакари. Даёт бесконечную проклятую энергию "
                       "на время действия при выпадении джекпота.",
        "type": "domain_expansion",
        "tags": [
            {"tagId": "buff", "aspectValues": {
                "target": "self", "buffedAxis": "stam",
                "bonus": 50, "durationType": "temporary"}},
            {"tagId": "heal", "aspectValues": {
                "amount": 90, "targets": "self",
                "curesStatuses": True}},
            {"tagId": "aoe", "aspectValues": {
                "radiusMeters": 200, "shape": "circle"}},
        ],
    },
    {
        "name": "Снайпер-техника",
        "description": "Техника Мэй Мэй. Выстрел на огромные расстояния "
                       "с максимальной точностью.",
        "type": "innate_technique",
        "tags": [
            {"tagId": "damage", "aspectValues": {
                "power": 70, "damageType": "energy",
                "ignoresDefense": False}},
            {"tagId": "ranged", "aspectValues": {
                "meters": 5000, "projectileSpeed": 85}},
            {"tagId": "chakra_cost", "aspectValues": {
                "description": "оплачивается за использование",
                "percentOfPool": 15}},
        ],
    },
    {
        "name": "Домен Джого (Coffin of the Iron Mountain)",
        "description": "Домен Джого. Заполняет пространство лавой и "
                       "вулканическим пеплом.",
        "type": "domain_expansion",
        "tags": [
            {"tagId": "damage", "aspectValues": {
                "power": 85, "damageType": "energy",
                "ignoresDefense": True, "isDot": True}},
            {"tagId": "aoe", "aspectValues": {
                "radiusMeters": 100, "shape": "circle"}},
            {"tagId": "control", "aspectValues": {
                "controlType": "bind", "targets": 5,
                "durationSeconds": 60}},
        ],
    },
    {
        "name": "Домен Хана",
        "description": "Домен Хана. Заполняет пространство цветущим лесом, "
                       "постоянно восстанавливающим его владельца.",
        "type": "domain_expansion",
        "tags": [
            {"tagId": "heal", "aspectValues": {
                "amount": 80, "targets": "self",
                "curesStatuses": True}},
            {"tagId": "aoe", "aspectValues": {
                "radiusMeters": 100, "shape": "circle"}},
            {"tagId": "control", "aspectValues": {
                "controlType": "bind", "targets": 3,
                "durationSeconds": 45}},
        ],
    },
]


# ============================================================================
# ЗАПИСЬ
# ============================================================================

def write_entity(type_name: str, name: str, json_data: dict) -> bool:
    entity_uuid = make_uuid(type_name, name)
    folder_name = f"{slug(name)}__{entity_uuid}"

    type_dir = DATA / type_name
    type_dir.mkdir(parents=True, exist_ok=True)
    folder = type_dir / folder_name

    if folder.exists():
        print(f"  ⚠ {type_name}/{folder_name} уже существует — пропуск")
        return False

    folder.mkdir()

    json_name = {
        "characters": "character.json",
        "abilities":  "ability.json",
        "roles":      "role.json",
        "scenarios":  "scenario.json",
        "axes":       "axis.json",
        "worlds":     "world.json",
        "tags":       "tag.json",
    }[type_name]

    with (folder / json_name).open("w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    return True


def build_character(data: dict) -> dict:
    name = data["name"]
    return {
        "id": make_uuid("characters", name),
        "name": name,
        "y": data["y"],
        "worldId": data.get("worldId"),
        "familyId": data.get("familyId"),
        "variant": data.get("variant"),
        "tags": data.get("tags", []),
        "abilities": [],
        "description": data.get("description"),
        "lore": data.get("lore"),
        "iconPath": None,
        "axes": {k: axes_to_dict(v) for k, v in data["axes"].items()},
        "createdAt": "2025-01-01T00:00:00.000Z",
        "updatedAt": "2025-01-01T00:00:00.000Z",
    }


def build_role(data: dict) -> dict:
    return {
        "id": make_uuid("roles", data["name"]),
        "name": data["name"],
        "weights": data["weights"],
        "enabled": True,
        "bgColor": None,
        "textColor": None,
    }


def build_scenario(data: dict) -> dict:
    out = {
        "id": make_uuid("scenarios", data["name"]),
        "name": data["name"],
        "decayCurve": data.get("decayCurve", 0.4),
        "enabled": True,
    }
    weights = data.get("axisWeights")
    if weights:
        out["axisWeights"] = weights
    return out


def build_axis(data: dict) -> dict:
    return {
        "id": data["id_key"],
        "name": data["name"],
        "order": data["order"],
        "enabled": True,
        "isCustom": False,
        "description": data.get("desc"),
    }


def build_world(data: dict) -> dict:
    return {
        "id": slug(data["name"]),
        "name": data["name"],
        "creators": data.get("creators", []),
        "physicality": data["physicality"],
        "powerSource": data.get("powerSource"),
        "powerScaleMax": data.get("powerScaleMax"),
        "rules": data.get("rules", {}),
        "compatibility": data.get("compatibility", {}),
    }


def build_ability(data: dict) -> dict:
    name = data["name"]
    return {
        "id": make_uuid("abilities", name),
        "name": name,
        "description": data.get("description"),
        "type": data.get("type"),
        "tags": data.get("tags", []),
        "createdAt": "2025-01-01T00:00:00.000Z",
        "updatedAt": "2025-01-01T00:00:00.000Z",
    }


def main() -> int:
    print("[seed] Создание базовых данных (Jujutsu Kaisen)…")

    counts = {
        "characters": 0, "roles": 0, "scenarios": 0,
        "axes": 0, "worlds": 0, "abilities": 0,
    }

    for c in CHARACTERS:
        if write_entity("characters", c["name"], build_character(c)):
            counts["characters"] += 1
    for r in ROLES:
        if write_entity("roles", r["name"], build_role(r)):
            counts["roles"] += 1
    for s in SCENARIOS:
        if write_entity("scenarios", s["name"], build_scenario(s)):
            counts["scenarios"] += 1
    for a in AXES:
        if write_entity("axes", a["name"], build_axis(a)):
            counts["axes"] += 1
    for w in WORLDS:
        if write_entity("worlds", w["name"], build_world(w)):
            counts["worlds"] += 1
    for ab in ABILITIES:
        if write_entity("abilities", ab["name"], build_ability(ab)):
            counts["abilities"] += 1

    print("\n[seed] Итого создано:")
    for k, v in counts.items():
        print(f"  {k}: {v}")

    print("\n[seed] Готово. Не забудьте запустить:")
    print("  python scripts/build_index.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())