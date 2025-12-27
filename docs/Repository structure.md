
# Структура репозитория

## Ниже приводится логическая структура репозитория. 

ci-cd-learning-project/

├─ backend/                     # Backend (Flask API)

│  ├─ app.py                    # Основной файл Flask приложения

│  ├─ requirements.txt          # Зависимости backend (prod/runtime)

│  ├─ Dockerfile                # Docker сборка backend

│  └─ tests/

│     └─ test_app.py            # pytest тесты (контракт API)

│
├─ frontend/                    # Frontend (React)

│  ├─ src/

│  │  └─ App.js                 # UI + логика запросов в API

│  ├─ public/

│  ├─ package.json              # npm зависимости + скрипты

│  ├─ .env                      # local (dev) конфиг (НЕ обязателен)

│  └─ build/                    # production артефакт (создается npm run build)

│
├─ .github/workflows/

│  └─ ci.yml                    # GitHub Actions pipeline (tests + docker + deploy)

│
└─ docs/                        # (рекомендуется) документация проекта

### Важное примечание о build/

frontend/build/— это необходимые продукты-сборки , он включается командой:

npm run build


build/ не заменяет исходники.

как правило, build/ не коммитят в git. 