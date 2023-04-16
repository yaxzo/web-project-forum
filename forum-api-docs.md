# FORUM API

```PUBLIC_APIKEY: GJYE-HY34-NBSD-LN4C```

все места, где указан <string:apikey> заменить на публичный API-ключ
для приватных ключей указано <string:private_apikey>


## API для класса User

### GET

получение информации о всех пользователях

**Requset:**

```
http://127.0.0.1:5050/api/v1/<string:apikey>/users
```

**Example response:**

```
{
  "users": [
    {
      "created_date": "2023-04-15 00:00:00",
      "email": "pochta@gmail.com",
      "username": "yaxzo",
      "id": 1
    },
    {
      "created_date": "2023-04-15 00:00:00",
      "email": "pochta123@gmail.com",
      "username": "yaxzo123",
      "id": 2
    }
  ]
}
```

**Error:**

если пользователя не существует

```
{
  "error": "users not found"
}
```

если API ключ не подходит

```
{
  "error": "bad apikey"
}
```

---

### GET

получение информации о конкретном пользователе

**Request:**
```
http://127.0.0.1:5050/api/v1/user/<user_id>
```
<user_id> заменить на id пользователя, для получения информации о нём

**Example response:**

```
{
  "user": {
    "created_date": "2023-04-15 00:00:00",
    "email": "pochta@gmail.com",
    "username": "yaxzo",
    "id": 1
  }
}
```

**Error:**

если пользователя не существует

```
{
  "error": "users not found"
}
```

если API ключ не подходит

```
{
  "error": "bad apikey"
}
```

---

### DELETE

удаление пользователя по id

```
http://127.0.0.1:5050/api/v1/<string:private_apikey>/<int:user_id>
```

удалить пользователя может только разработчик, имеющий доступ к `PRIVATE_APIKEY`

**Response:**

```
{
  "success": "OK"
}
```

**Error:**

если пользователя не существует

```
{
  "error": "users not found"
}
```

если API ключ не подходит

```
{
  "error": "bad apikey"
}
```

## Trad API
допишу, когда доделаю
