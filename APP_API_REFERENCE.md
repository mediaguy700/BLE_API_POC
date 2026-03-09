# Full API reference for applications

Everything an application needs to call all endpoints.

**Quick list (24 endpoints):**  
Readers: GET/POST `/readers`, GET/PUT/PATCH/DELETE `/readers/{readerName}`, GET `/readers/{readerName}/events`  
Events: GET/POST `/events`, GET/PUT/PATCH/DELETE `/events/{id}`, GET `/events/person/{mac}`  
Active BLE: GET `/active-ble`, GET `/active-ble/{id}`, POST `/active-ble`, PATCH `/active-ble/{id}`  
Auth: POST `/auth/register`, POST `/auth/login`, GET `/auth/me`, POST `/auth/logout`, POST `/auth/password-reset/request`, POST `/auth/password-reset/confirm`

---

## 1. Base URL and API key

| Item | Value |
|------|--------|
| **Base URL** | `https://rkali63t89.execute-api.us-east-2.amazonaws.com/Prod` |
| **API key** | `MlzzVbn4og1AN93aBra5pa9OTKZs716j35uFuV1I` |

---

## 2. Headers (every request)

| Header | Value | When |
|--------|--------|------|
| **x-api-key** | Your API key (above) | **Required on every request.** Without it → 403. |
| **Content-Type** | `application/json` | Required for POST, PUT, PATCH bodies. |
| **Authorization** | `Bearer <session-token>` | Required for `/auth/me` and `/auth/logout` (token from login). |

---

## 3. All endpoints

### Readers

| Method | Path | Description | Body / Query |
|--------|------|-------------|--------------|
| GET | `/readers` | List all readers | — |
| GET | `/readers/{readerName}` | Get one reader | — |
| POST | `/readers` | Create reader | `reader_name`, `latitude`, `longitude`; optional: `display_name` |
| PUT | `/readers/{readerName}` | Full update reader | `latitude`, `longitude`; optional: `name`, `display_name` |
| PATCH | `/readers/{readerName}` | Partial update reader | any of: `latitude`, `longitude`, `name`, `display_name` |
| DELETE | `/readers/{readerName}` | Delete reader | — |
| GET | `/readers/{readerName}/events` | List events at reader (children) | Optional query: `?direction=in` or `?direction=out` |

### Events

| Method | Path | Description | Body / Query |
|--------|------|-------------|--------------|
| GET | `/events` | List all events | Optional: `?direction=in` or `?direction=out` |
| GET | `/events/{id}` | Get one event | — |
| GET | `/events/person/{mac}` | List events for person (MAC) | Optional: `?direction=in` or `?direction=out` |
| POST | `/events` | Create event | Required: `reader_name`, `mac`. Optional: `direction`, `name`, etc. |
| PUT | `/events/{id}` | Full update event | fields to update |
| PATCH | `/events/{id}` | Partial update event | any event fields |
| DELETE | `/events/{id}` | Delete event | — |

### Active BLE

| Method | Path | Description | Body |
|--------|------|-------------|------|
| GET | `/active-ble` | List all active_ble rows | — |
| GET | `/active-ble/{id}` | Get one active_ble row by id | — |
| POST | `/active-ble` | Insert row into active_ble | `mac` (required), optional: `active`, `lname`, `fname`, `parent_id`, `duration`, `parent_fname`, `parent_lname`, `parent_phone`. Returns **409 "User Exists"** if `mac` already in table. |
| PATCH | `/active-ble/{id}` | Update row by id | Any of: `mac`, `active`, `lname`, `fname`, `parent_id`, `duration`, `parent_fname`, `parent_lname`, `parent_phone`. Returns **409 "User Exists"** if new `mac` already in table. |

### Auth (users & login)

| Method | Path | Description | Body | Extra headers |
|--------|------|-------------|------|----------------|
| POST | `/auth/register` | Create user | `username`, `password`; optional: `email` | — |
| POST | `/auth/login` | Log in | `username`, `password` | — |
| GET | `/auth/me` | Current user | — | **Authorization: Bearer &lt;token&gt;** |
| POST | `/auth/logout` | Log out (invalidate session) | — | **Authorization: Bearer &lt;token&gt;** |
| POST | `/auth/password-reset/request` | Request password reset | `email` or `username` | — |
| POST | `/auth/password-reset/confirm` | Set new password with reset token | `token`, `new_password` | — |

---

## 4. Request body examples (JSON)

**Readers**
- Create: `{"reader_name": "Lobby-01", "latitude": 40.71, "longitude": -74.01, "display_name": "Main Lobby"}`

**Events**
- Create: `{"mac": "AA:BB:CC:DD:EE:01", "reader_name": "Lobby-01", "direction": "in", "name": "Alice"}`

**Active BLE**
- Create: `{"mac": "AA:BB:CC:DD:EE:01", "active": true, "lname": "Doe", "fname": "Jane", "parent_id": null, "duration": 60, "parent_fname": "Bob", "parent_lname": "Doe", "parent_phone": "555-1234"}`. `mac` required; returns 409 `{"error": "User Exists"}` if mac already exists.
- Update: `PATCH /active-ble/{id}` with body e.g. `{"active": false, "duration": 300, "parent_fname": "Mary", "parent_lname": "Smith", "parent_phone": "555-9999"}`. Only included fields are updated. Returns 409 if new `mac` is already used by another row.

**Auth**
- Register: `{"username": "alice", "password": "YourPassword", "email": "alice@example.com"}`
- Login: `{"username": "alice", "password": "YourPassword"}`
- Password reset request: `{"email": "alice@example.com"}` or `{"username": "alice"}`
- Password reset confirm: `{"token": "<reset-token>", "new_password": "NewPassword"}`

---

## 5. Typical response shapes

- **Readers list:** `{"readers": [{ "reader_name", "latitude", "longitude", "display_name", "created_at", "updated_at" }]}`
- **Events list:** `{"events": [{ "id", "mac", "reader_name", "direction", "name", "date_time", "created_at", ... }]}`
- **Active BLE list:** `{"active_ble": [{ "id", "mac", "active", "lname", "fname", "parent_id", "duration", "parent_fname", "parent_lname", "parent_phone" }, ...]}`
- **Active BLE get/create/update (single):** `{ "id", "mac", "active", "lname", "fname", "parent_id", "duration", "parent_fname", "parent_lname", "parent_phone" }`
- **Login:** `{"user": { "id", "username", "email", "created_at" }, "token": "...", "expires_at": "..."}`
- **Auth me:** `{"user": { "id", "username", "email", "created_at" }}`
- **Errors:** `{"error": "message"}` with status 4xx/5xx

---

## 6. Test user (for QA / demos)

You can use this built-in test account:

| Field | Value |
|--------|--------|
| **Username** | `testuser2` |
| **Password** | `TestPass123!` |
| **Email** | `testuser2@example.com` |

Login body:
```json
{"username": "testuser2", "password": "TestPass123!"}
```

---

## 7. App config (copy-paste)

```env
BLE_API_URL=https://rkali63t89.execute-api.us-east-2.amazonaws.com/Prod
BLE_API_KEY=MlzzVbn4og1AN93aBra5pa9OTKZs716j35uFuV1I
```

**Usage in code:**
- Every request: add header `x-api-key: <BLE_API_KEY>`.
- After login: store `token`; for `/auth/me` and `/auth/logout` add `Authorization: Bearer <token>`.
- POST/PUT/PATCH: set `Content-Type: application/json` and send JSON body.

---

## 8. Quick cURL examples

```bash
# Readers
curl -s -H "x-api-key: $BLE_API_KEY" "$BLE_API_URL/readers"
curl -s -X POST -H "x-api-key: $BLE_API_KEY" -H "Content-Type: application/json" \
  -d '{"reader_name":"Lobby-01","latitude":40.71,"longitude":-74.01}' "$BLE_API_URL/readers"

# Events
curl -s -H "x-api-key: $BLE_API_KEY" "$BLE_API_URL/events?direction=in"
curl -s -X POST -H "x-api-key: $BLE_API_KEY" -H "Content-Type: application/json" \
  -d '{"mac":"AA:BB:CC:DD:EE:01","reader_name":"Lobby-01","direction":"in","name":"Alice"}' "$BLE_API_URL/events"

# Active BLE
curl -s -H "x-api-key: $BLE_API_KEY" "$BLE_API_URL/active-ble"
curl -s -H "x-api-key: $BLE_API_KEY" "$BLE_API_URL/active-ble/1"
curl -s -X POST -H "x-api-key: $BLE_API_KEY" -H "Content-Type: application/json" \
  -d '{"mac":"AA:BB:CC:DD:EE:01","fname":"Jane","lname":"Doe","parent_phone":"555-1234"}' "$BLE_API_URL/active-ble"
curl -s -X PATCH -H "x-api-key: $BLE_API_KEY" -H "Content-Type: application/json" \
  -d '{"parent_phone":"555-9999"}' "$BLE_API_URL/active-ble/1"

# Auth
curl -s -X POST -H "x-api-key: $BLE_API_KEY" -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"secret"}' "$BLE_API_URL/auth/login"
# Then use returned token:
curl -s -H "x-api-key: $BLE_API_KEY" -H "Authorization: Bearer <TOKEN>" "$BLE_API_URL/auth/me"
```

---

This is the full info needed for an application to use all endpoints.

---

## 9. Swagger / OpenAPI docs

- **Spec:** `openapi.yaml` (OpenAPI 3.0)
- **Swagger UI:** Open `swagger.html` in a browser. For it to load the spec, serve the project folder (e.g. `python3 -m http.server 8080`) then go to `http://localhost:8080/swagger.html`. Click **Authorize** and enter the API key to try requests.
