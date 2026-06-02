# Бортжурнал автомобіліста (REST + GraphQL + WebSockets)

Комплексний клієнт-серверний демо-застосунок на **Django**, який демонструє роботу **REST API (Django REST Framework)**, **GraphQL (Strawberry)** та **WebSockets (Django Channels)**.

---

## 🔗 Демо-посилання


Адмін-панель:
https://avto-8w3n.onrender.com/admin/
Логін: admin
Пароль: AvtoAdmin_2026!StrongPass9

### Frontend (Render)

https://avto-1-1p0q.onrender.com

---

## ⚙️ Функціонал

### 🔐 Auth

* Реєстрація користувача
* Логін (JWT)
* Отримання профілю користувача
* Відновлення пароля (dev-режим)

---

### 🚗 REST API

* CRUD для автомобілів (VIN, марка, модель)
* Заправки (дата, пробіг, літри, сума)
* Замовлення запчастин (`SparePartOrder`):

  * назва
  * артикул
  * кількість
  * статус
  * ціна

---

### 📊 GraphQL

* Запит:

  * `maintenanceHistory(vin: String!)`
* Повертає:

  * історію ТО
  * плани ТО
  * прив’язку до пробігу

---

### 🔔 WebSockets

* Канал: `/ws/reminders/`
* Реальний час:

  * нагадування про ТО
  * “due soon / overdue”
* Оновлення після додавання заправки або ТО

---

## 📡 API Endpoints

### Auth

* `POST /api/auth/register/`
* `POST /api/auth/token/`
* `GET /api/auth/me/`
* `POST /api/auth/password/forgot/`
* `POST /api/auth/password/reset/`

### Cars

* `GET /api/cars/`

### Fuel

* `GET /api/fuel-fillups/`

### Spare parts

* `GET /api/spare-part-orders/`

### GraphQL

* `/graphql/`

### WebSockets

* `ws:// / wss:// avto-8w3n.onrender.com/ws/reminders/`

---

## 🧠 Бізнес-логіка нагадувань

Нагадування формуються якщо:

* є заправки (формують поточний пробіг)
* є план технічного обслуговування
* після кожного запису ТО план оновлюється автоматично

Стандартний інтервал ТО:

* 10 000 км
* “due soon” = ≤ 500 км до планового ТО

---

## 🚀 Деплой

Проєкт повністю розгорнутий на **Render**:

* Backend: Django + DRF + GraphQL + Channels
* Frontend: Static site (HTML/CSS/JS)
* База даних: PostgreSQL (Render managed)

---

## 🔧 Frontend

Фронтенд — це простий SPA/статичний клієнт:

* працює через fetch-запити до API
* не потребує Node.js збірки
* розгортається як Static Site

---

## 🧩 Архітектура

* Backend: Django
* API: Django REST Framework
* GraphQL: Strawberry
* Real-time: Django Channels (WebSockets)
* Frontend: Vanilla JS (static)
* Hosting: Render

---

## 📌 Примітка

Проєкт створений як навчально-демонстраційний:

* показує роботу трьох типів API
* демонструє real-time оновлення
* імітує систему бортжурналу автомобіля



