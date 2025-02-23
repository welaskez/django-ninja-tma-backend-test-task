## Инструкция по запуску

### 1. Настройка переменных окружения

Не забудьте задать переменную BOT_TOKEN

```bash
mv api/.env.example api/.env
```

```bash
mv pg_db.env.example pg_db.env
```

### 2. Генерация сертификатов для jwt
```bash
mkdir -p api/certs
```

```bash
openssl genrsa -out api/certs/jwt-private.pem 2048  
```

```bash
openssl rsa -in api/certs/jwt-private.pem -outform PEM -pubout -out api/certs/jwt-public.pem
  
```

### 3. Сборка и запуск приложения
```bash
docker compose up --build -d
```

### 4. Доступ к админке
После того как приложение успешно запущено необходимо
создать админа
```bash
docker exec -it api bash
```

```bash
./manage.py createsuperuser
```
Далее по инструкции создаем супер юзера

---

Админка http://localhost:8080/admin

Swagger UI http://localhost:8080/api/v1/docs
