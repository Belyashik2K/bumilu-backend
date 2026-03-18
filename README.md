# BumiLu-users-service
Users service for mobile ans web application BumiLu (不迷路), PAB project

Доки доступны на:
1. http://localhost:8000/docs/swagger - Swagger
2. http://localhost:8000/docs/redoc - ReDoc

### Установка
### 1. Клонирование
```bash
git clone https://github.com/BumiLuDev/users-service.git
cd users-service
git checkout dev
```
### 2. Создание .env
```bash
cp .env.example .env
```
Также нужно заменить:
```env
AUTH__EMAIL__SMTP__HOST=smtp.example.com
AUTH__EMAIL__SMTP__PORT=1127
AUTH__EMAIL__SMTP__USERNAME=username
AUTH__EMAIL__SMTP__PASSWORD=password
```
и
```env
CHAT__AI_ASSISTANT__OPENAI__API_KEY=your_openai_key
```
на:
```env
AUTH__EMAIL__SMTP__HOST=smtp.mail.selcloud.ru
AUTH__EMAIL__SMTP__PORT=1127
AUTH__EMAIL__SMTP__USERNAME="username"
AUTH__EMAIL__SMTP__PASSWORD="REDACTED_SMTP_PASSWORD"
```
и
```env
CHAT__AI_ASSISTANT__OPENAI__API_KEY=REDACTED_OPENROUTER_API_KEY
```
### 3. Запуск
```bash
docker-compose -f docker-compose.dev.yml -f docker-compose.yml up --build
```
_Если есть IDE от Jetbrains: можно запустить через конфигурацию_ `[DEV] Run service`
