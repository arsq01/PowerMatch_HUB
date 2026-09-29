# PowerMatch Data Hub

Публичный репозиторий данных для приложения **PowerMatch**.

## Что здесь

- **`data/characters/`** — карточки персонажей
- **`data/abilities/`** — каталог способностей
- **`data/tags/`** — схема тегов (что такое «урон», «дальность» и т. д.)
- **`data/roles/`** — роли (Боец, Медик, …)
- **`data/scenarios/`** — сценарии боя
- **`data/worlds/`** — миры (Naruto, Bleach, Marvel, …)
- **`data/axes/`** — оси характеристики (опционально)
- **`index/`** — авто-сгенерированные индексы для приложения

## Как использовать в приложении

1. Откройте **Настройки → Данные → HUB**.
2. Вставьте URL:
   ```
   https://raw.githubusercontent.com/USER/powermatch-data/main/index/manifest.json
   ```
3. Нажмите «Обновить каталог».
4. Выбирайте данные и импортируйте.

## Как добавить свои данные

### Через fork (ручной способ)

1. Форкните репозиторий.
2. Создайте папку в `data/characters/`:
   ```
   my_character__<UUID>/
   ├── character.json
   └── icon.png
   ```
   Имя папки — `<латиница>__<UUID>`. UUID можно сгенерировать на [uuidgenerator.net](https://www.uuidgenerator.net/).
3. Заполните `character.json` по схеме из `schema/character.schema.json`.
4. Закоммитьте, запушьте.
5. GitHub Action автоматически пересоберёт `index/*.index.json`.

### Через pull request (если хотите в общий)

1. Форк → правки → PR в upstream.
2. Мейнтейнер проверит (валидация JSON запустится автоматически).
3. После merge индексы обновятся автоматически.

## Структура одного файла

Пример `data/characters/naruto__a1b2c3d4-.../character.json`:

```json
{
  "id": "a1b2c3d4-0001-0001-0001-000000000001",
  "name": "Наруто Узумаки",
  "y": 0.8,
  "worldId": "naruto",
  "familyId": "naruto",
  "variant": "War Mode",
  "tags": ["konoha", "jinchuriki"],
  "abilities": ["rasengan__b1c2d3e4-..."],
  "axes": { "str": {...}, "spd": {...}, ... },
  "createdAt": "2025-01-01T00:00:00.000Z",
  "updatedAt": "2025-01-01T00:00:00.000Z"
}
```

## Как работает build_index.py

GitHub Action запускает скрипт при каждом push в `main`, если изменилось что-то в `data/`.

Скрипт:
1. Проходит по всем папкам `data/<type>/`.
2. Читает `<type>.json` в каждой.
3. Строит `<type>.index.json` — плоский список всех сущностей с минимумом полей (id, name, path, icon).
4. Обновляет `manifest.json` — общий индекс с ссылками.

Индексы **не нужно править руками** — при следующем push всё перезапишется.

## Версионирование схемы

Файл `VERSION` содержит текущую версию схемы, например `1.0.0`.

При изменении схемы:
1. Увеличьте `VERSION`.
2. Обновите `schema/*.schema.json`.
3. Запустите `scripts/migrate.py` — он применит изменения ко всем файлам в `data/`.

## Лицензия

Данные — CC BY-SA 4.0. Скрипты — MIT.