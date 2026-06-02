# Бортжурнал автомобіліста (REST + GraphQL + WebSockets)

Комплексний клієнт‑серверний демо‑застосунок на **Django**, який демонструє роботу **REST API (DRF)**, **GraphQL (Strawberry)** та **WebSockets (Django Channels)**.

## Функції

- **Auth**
  - Реєстрація: `POST /api/auth/register/`
  - Логін (JWT): `POST /api/auth/token/`
  - Профіль: `GET /api/auth/me/`
  - Забули пароль: `POST /api/auth/password/forgot/` (у dev payload друкується в консоль бекенду)
  - Reset підтвердження: `POST /api/auth/password/reset/`
- **REST**
  - CRUD для авто: VIN, марка, модель
  - Фіксація базових витрат: заправки (дата, пробіг, літри, сума)
  - CRUD для замовлень запчастин: `SparePartOrder` (назва, артикул, к-сть, статус, ціна)
- **GraphQL**
  - Гнучкий запит `maintenanceHistory(vin: String!)` — історія ТО + плани ТО з привʼязкою до пробігу
- **WebSockets**
  - Push‑нагадування `/ws/reminders/` — “due soon / overdue” за планами ТО (після нової заправки/ТО оновлюється автоматично)

## Запуск (Windows / PowerShell)

### Backend

```powershell
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
.\.venv\Scripts\python backend\manage.py migrate
.\.venv\Scripts\python backend\manage.py createsuperuser
.\.venv\Scripts\python backend\manage.py runserver 0.0.0.0:8000
```

- Адмінка: `http://localhost:8000/admin/`
- Auth: `http://localhost:8000/api/auth/...`
- REST: `http://localhost:8000/api/cars/`, `http://localhost:8000/api/fuel-fillups/`, `http://localhost:8000/api/spare-part-orders/`
- GraphQL: `http://localhost:8000/graphql/`
- WS: `ws://localhost:8000/ws/reminders/`

### Frontend (простий статичний демо‑клієнт)

Відкрий `frontend/index.html` у браузері (або запусти будь‑який static server у папці `frontend/`).

## Дані для нагадувань

Нагадування зʼявляються, якщо:

- є **заправка** (вона дає “поточний пробіг”)
- є **план ТО** (`MaintenancePlan`) або запис ТО (`MaintenanceRecord`) — після збереження запису ТО план створюється/оновлюється автоматично

Планові інтервали за замовчуванням: `10_000` км, “due soon” = `<= 500` км до наступного ТО.

## Docker / деплой (VPS)

Локально:

```powershell
docker compose up --build
```

Мінімальні env (для docker-compose або VPS):

- `DJANGO_SECRET_KEY`: обовʼязково в проді
- `DJANGO_DEBUG=0`
- `DJANGO_ALLOWED_HOSTS=your-domain.com,1.2.3.4`
- `REDIS_URL=redis://redis:6379/0` (для WS у проді)

На VPS (Ubuntu) зазвичай достатньо:

- встановити Docker + Docker Compose
- відкрити порт `8000` (або проксувати через Nginx)
- задати `DJANGO_ALLOWED_HOSTS` під домен/IP

### Приклад деплою на VPS (Ubuntu) з публічним посиланням

1) На VPS встанови Docker і Compose.

2) Склонуй проєкт:

```bash
git clone <your-repo>
cd avto
```

3) В `docker-compose.yml` або через `.env` вистав:

- `DJANGO_SECRET_KEY` (випадковий довгий рядок)
- `DJANGO_DEBUG=0`
- `DJANGO_ALLOWED_HOSTS=<domain>,<server_ip>`
- `REDIS_URL=redis://redis:6379/0`

4) Запусти:

```bash
docker compose up --build -d
```

5) Створи адміна в контейнері:

```bash
docker compose exec web python backend/manage.py createsuperuser
```

6) Відкрий у браузері:

- `http://<server_ip>:8000/admin/`
- `http://<server_ip>:8000/api/...`
- `http://<server_ip>:8000/graphql/`

> Для красивого домену + HTTPS зазвичай ставлять Nginx як reverse proxy (на 80/443) і проксють на `localhost:8000`.

## Безкоштовний деплой (рекомендовано): Fly.io (backend) + GitHub Pages (frontend)

### 1) Підготуй GitHub репозиторій

- Встанови Git for Windows (щоб працювала команда `git`)
- Створи репозиторій на GitHub і запуш проєкт

### 2) Backend на Fly.io (Django + WebSockets)

1) Зареєструйся на Fly.io і встанови CLI:

```powershell
winget install -e --id FlyIO.Flyctl
flyctl auth login
```

2) У корені проєкту запусти:

```powershell
flyctl launch
```

- обери **region** (будь-який)
- **не додавай Postgres** (нам він не потрібен)

3) Додай секрети (обовʼязково!):

```powershell
flyctl secrets set DJANGO_SECRET_KEY="your-long-secret" DJANGO_DEBUG="0" DJANGO_ALLOWED_HOSTS="<your-app>.fly.dev"
```

4) Задеплой:

```powershell
flyctl deploy
```

5) Після деплою відкрий:

- `https://<your-app>.fly.dev/admin/`
- `https://<your-app>.fly.dev/api/...`
- `https://<your-app>.fly.dev/graphql/`
- WS: `wss://<your-app>.fly.dev/ws/reminders/`

> Примітка: без Redis WS працюватиме для 1 інстансу (достатньо для навчального демо). Якщо захочеш “як у проді” — додаси Redis і виставиш `REDIS_URL`.

### 3) Frontend на GitHub Pages (статичний)

1) У `frontend/main.js` заміни `API_BASE` на URL твого бекенду (наприклад `https://<your-app>.fly.dev`)
2) Створи в репозиторії папку `docs/` і скопіюй туди `frontend/index.html` та `frontend/main.js`
3) У GitHub → **Settings → Pages**:
   - Source: **Deploy from a branch**
   - Branch: `main`
   - Folder: `/docs`
4) Отримаєш публічне посилання на фронтенд, який звертається до твого бекенду на Fly.io.


