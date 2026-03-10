# BLE People Tracker API

REST API for tracking BLE (Bluetooth Low Energy) readers, events, and people. Built with AWS SAM (Serverless Application Model), Lambda, API Gateway, and PostgreSQL.

## Features

- **Readers** – BLE reader locations (lat/long) with CRUD operations
- **Events** – Track in/out events by MAC address at each reader
- **Active BLE** – Child/person records with parent contact info
- **Auth** – User registration, login, logout, password reset

## Tech Stack

- **Runtime:** Python 3.9 (Lambda)
- **Database:** PostgreSQL (RDS or external)
- **API:** AWS API Gateway (REST) with API key auth
- **IaC:** AWS SAM / CloudFormation

## Quick Start

### Test the API (curl)

```bash
# Set credentials (or use static-2week-api-access.env)
export BLE_API_URL="https://rkali63t89.execute-api.us-east-2.amazonaws.com/Prod"
export BLE_API_KEY="MlzzVbn4og1AN93aBra5pa9OTKZs716j35uFuV1I"

# List readers
curl -s -H "x-api-key: $BLE_API_KEY" "$BLE_API_URL/readers"

# Login (test user: testuser2 / TestPass123!)
curl -s -X POST -H "x-api-key: $BLE_API_KEY" -H "Content-Type: application/json" \
  -d '{"username":"testuser2","password":"TestPass123!"}' "$BLE_API_URL/auth/login"
```

### Swagger UI (interactive docs)

```bash
python3 -m http.server 8080
```

Open **http://localhost:8080/swagger.html**, click **Authorize**, enter the API key, then use "Try it out" on any endpoint.

## API Overview

| Resource | Endpoints |
|----------|-----------|
| **Readers** | GET/POST `/readers`, GET/PUT/PATCH/DELETE `/readers/{readerName}`, GET `/readers/{readerName}/events` |
| **Events** | GET/POST `/events`, GET/PUT/PATCH/DELETE `/events/{id}`, GET `/events/person/{mac}` |
| **Active BLE** | GET `/active-ble`, GET `/active-ble/{id}`, POST `/active-ble`, PATCH `/active-ble/{id}` |
| **Auth** | POST `/auth/register`, `/auth/login`, GET `/auth/me`, POST `/auth/logout`, `/auth/password-reset/*` |

**Required:** Send `x-api-key` header on every request. For `/auth/me` and `/auth/logout`, also send `Authorization: Bearer <token>` (token from login).

## Project Structure

```
├── template.yml          # SAM/CloudFormation definition
├── openapi.yaml          # OpenAPI 3.0 spec
├── swagger.html          # Swagger UI (all endpoints)
├── src/
│   ├── handlers/         # Lambda handlers
│   │   ├── readers.py
│   │   ├── events.py
│   │   ├── active_ble.py
│   │   └── auth.py
│   ├── db.py             # DB connection
│   └── auth.py           # Auth helpers
├── database/
│   ├── schema.sql
│   └── migrations/
└── scripts/              # Dev/access scripts
```

## Deployment (AWS SAM)

```bash
# Build and deploy
sam build
sam deploy --guided
```

After first deploy, invoke the Schema Runner Lambda once to run `schema.sql` and migrations.

## Documentation

| File | Purpose |
|------|---------|
| [APP_API_REFERENCE.md](APP_API_REFERENCE.md) | Full API reference for applications |
| [DEVELOPER_ACCESS.md](DEVELOPER_ACCESS.md) | How developers get URL + API key |
| [openapi.yaml](openapi.yaml) | OpenAPI 3.0 specification |

## Test Account

| Field | Value |
|-------|-------|
| Username | `testuser2` |
| Password | `TestPass123!` |
| Email | `testuser2@example.com` |
