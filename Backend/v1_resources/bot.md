## `GET /dabolinkbot/api/v1.0/bot/start/:channel`

Starts a bot in channel :channel

### Parameters

NONE

### Example Request

```bash
curl -X GET https://localhost:8000/dabolinkbot/api/v1.0/bot/start/dabolink/
```

### Example Response

```json
{
  "result": "success",
}
```

## `GET /dabolinkbot/api/v1.0/bot/end/:channel`

Ends a bot in channel :channel

### Parameters

NONE

### Example Request

```bash
curl -X GET https://localhost:8000/dabolinkbot/api/v1.0/bot/end/dabolink/
```

### Example Response

```json
{
  "result": "success",
}
```

## `GET /dabolinkbot/api/v1.0/bot/status/:channel`

status of a bot in channel :channel

### Parameters

NONE

### Example Request

```bash
curl -X GET https://localhost:8000/dabolinkbot/api/v1.0/bot/status/dabolink/
```

### Example Response

```json
{
  "online": False,
}
```

## `GET /dabolinkbot/api/v1.0/dabolinkbot/status/channel/:channel/:user`

returns stats of user :user in channel :channel

### Parameters

NONE

### Example Request

```bash
curl -X GET https://localhost:8000/dabolinkbot/api/v1.0/bot/channel/thepretenderr/dabolink/
```

### Example Response

```json
{
  "thepretenderr": {
    "credits": 0.0,
    "hours": 58.16480305555555,
    "lines_of_text": 539
  },
  "user": "dabolink"
}
```

## `GET /dabolinkbot/api/v1.0/user/:user`

returns stats of user :user in all chats

### Parameters

NONE

### Example Request

```bash
curl -X GET https://localhost:8000/dabolinkbot/api/v1.0/bot/user/dabolink/
```

### Example Response

```json
{
  "channels": [
    {
      "dabolink": {
        "credits": 0.0,
        "hours": 0.33555000000000007,
        "lines of text": 9
      }
    },
    {
      "dabolinkbot": {
        "credits": 0.0,
        "hours": 0.03988083333333334,
        "lines of text": 5
      }
    },
    {
      "thepretenderr": {
        "credits": 0.0,
        "hours": 58.16480305555555,
        "lines of text": 539
      }
    }
  ],
  "user": "dabolink"
}
```