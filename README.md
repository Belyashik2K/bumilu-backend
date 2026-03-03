# BumiLu-users-service
Users service for mobile ans web application BumiLu (不迷路), PAB project

### Установка
### 1. Клонирование
```bash
git clone https://github.com/BumiLuDev/users-service.git
cd users-service
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
на:
```env
AUTH__EMAIL__SMTP__HOST=smtp.mail.selcloud.ru
AUTH__EMAIL__SMTP__PORT=1127
AUTH__EMAIL__SMTP__USERNAME="username"
AUTH__EMAIL__SMTP__PASSWORD="REDACTED_SMTP_PASSWORD"
```
### 3. Запуск
```bash
docker-compose -f docker-compose.dev.yml -f docker-compose.dev.yml up --build
```
_Если есть IDE от Jetbrains: можно запустить через конфигурацию_ `[DEV] Run service`

