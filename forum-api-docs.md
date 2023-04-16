# FORUM API FOR DEVELOPERS

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
http://127.0.0.1:5050/api/v1/user/delete/<string:private_apikey>/<int:user_id>
```

#### удалить пользователя может только разработчик, имеющий доступ к `PRIVATE_APIKEY`

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

### GET

получение информации о всех обсуждениях

**Request:**

```
http://127.0.0.1:5050/api/v1/trads/<string:apikey>
```

**Response:**

```
{
  "trads": [
    {
      "id": 1,
      "author_id": 1,
      "title": "\u0437\u0430\u0433\u043e\u043b\u043e\u0432\u043a \u043e\u0431\u0441\u0443\u0436\u0434\u0435\u043d\u0438\u044f 1",
      "created_date": "2023-04-16 00:00:00"
    },
    {
      "id": 2,
      "author_id": 3,
      "title": "\u043e\u0431\u0441\u0443\u0436\u0434\u0435\u043d\u0438\u0435 2",
      "created_date": "2023-04-16 00:00:00"
    }
  ]
}
```

**Error:**

если обсуждений не существует

```
{
  "error": "trads not found"
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

получение информации об определённой статье по её id

**Request:**

```
http://127.0.0.1:5050/api/v1/trad/<string:apikey>/<int:trad_id>
```

<trad_id> заменить на id обсуждения, о котором надо получить информацию

**Response:**

```
{
  "trad": {
    "id": 2,
    "author_id": 1,
    "title": "\u0437\u0430\u0433\u043e\u043b\u043e\u0432\u043a \u043e\u0431\u0441\u0443\u0436\u0434\u0435\u043d\u0438\u044f 1",
    "created_date": "2023-04-16 00:00:00"
  }
}
```

**Error:**

если обсуждений не существует

```
{
  "error": "trads not found"
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

удалить обсуждение по id

**Request:**

```
http://127.0.0.1:5050/api/v1/trad/delete/<string:private_apikey>/<int:trad_id>
```

#### удалить пользователя может только разработчик, имеющий доступ к `PRIVATE_APIKEY`

**Response:**

```
{
  "success": "OK"
}
```

**Error:**

если обсуждения не существует

```
{
  "error": "trad not found"
}
```

если API ключ не подходит

```
{
  "error": "bad apikey"
}
```

## Articles API

```
аналогично Trad API
доделаю позже
```
