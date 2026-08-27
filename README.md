# BumiLu Backend

Backend for BumiLu (不迷路) — a mobile & web app for discovering places and building routes.

Originally built as a university project ("Basics of Subject-Oriented Development"), where it reached the finals among 256 teams. This repository covers the backend: API, business logic, and the infrastructure/CI-CD setup.

## Tech Stack

- **API**: FastAPI, Python 3.14
- **Persistence**: PostgreSQL + PostGIS, SQLAlchemy 2.0 (async), Alembic migrations
- **Cache / sessions / queues**: Redis, Taskiq (background jobs & scheduler)
- **Routing**: [Valhalla](https://github.com/valhalla/valhalla)
- **DI**: Dishka
- **Observability**: structured logging, Prometheus (`prometheus-fastapi-instrumentator`)
- **Infra**: Docker / Docker Compose, GitHub Actions
- **Testing**: pytest, testcontainers

## Architecture

The codebase follows DDD-flavored layering with CQRS on the application layer. Every module under `app/modules/<name>` has the same internal structure:

- `domain` — entities, value objects, domain exceptions; no framework or infrastructure dependencies
- `application` — commands, queries, handlers, and interfaces (ports) that the domain and infrastructure implement against
- `infrastructure` — SQLAlchemy repositories, Redis-backed stores, external clients (adapters implementing the application ports)
- `presentation` — FastAPI routers, request/response schemas, DI wiring

Cross-cutting concerns (base exceptions, DB session/transaction handling, logging, config, DI container setup) live in `app/core`.

Modules: `auth`, `chat`, `favourites`, `places`, `reviews`, `routes`, `routing`, `staff`, `stats`, `users`.

## API

~90 endpoints across the modules listed above, split per module into user-facing and admin-facing routers (`user_router.py` / `admin_router.py`). Full interactive reference: `/docs/swagger` or `/docs/redoc` once the app is running — endpoint counts change too often for a static list here to stay accurate.

### Authentication & Access Control

Two principal types: **User** (mobile/web app end users) and **Staff** (internal admin panel).

- **User login** — two methods:
  - **Guest** — anonymous, device-bound session, no credentials required.
  - **Email OTP** — passwordless: request a one-time code by email, then verify it to get a session.
- **Staff login** — email + password.

Both flows issue a short-lived JWT access token plus a server-side, revocable refresh session (rotated on every refresh). Delivery differs by client: user refresh tokens are returned in the response body (mobile app), staff refresh tokens are set as an `httpOnly` cookie (web admin panel) — a deliberate split, not an inconsistency.

Admin routes are gated by a "is this a staff principal" check. Staff roles (`OWNER` / `ADMIN` / `SUPPORT`) exist in the domain model but aren't yet enforced per-endpoint — any authenticated staff member can currently reach any admin route.

## Getting Started

Prerequisites: Docker and Docker Compose.

1. **Clone**

   ```bash
   git clone https://github.com/Belyashik2K/bumilu-backend.git
   cd bumilu-backend
   ```

2. **Configure environment**

   ```bash
   cp .env.example .env
   ```

   Fill in real values for SMTP credentials, JWT/OTP secret keys, and S3 credentials. An OpenAI/OpenRouter API key is only needed if you want to exercise the chat assistant module.

3. **Create the shared external network**

   ```bash
   docker network create bumilu
   ```

4. **(Optional) Routing** — the `routing` module talks to a separate map service ([spb-map-service](https://github.com/BumiLuDev/spb-map-service)) for building routes via Valhalla. Skip this if you don't need routing endpoints.

5. **Run**

   ```bash
   docker-compose -f docker-compose.dev.yml -f docker-compose.yml up --build
   ```

   The `migrations` service applies Alembic migrations automatically before the API starts.

6. **API docs**: `http://localhost:8000/docs/swagger` (Swagger) or `http://localhost:8000/docs/redoc` (ReDoc).

7. **(Optional) Seed data** — `stubs/temp_places_and_routes_data.sql` has sample places/categories/routes for local exploration. Copy it into the running Postgres container and apply it with `psql`.

## Testing

```bash
pytest -m "not integration"   # unit tests only, no external services required
pytest                        # full suite; spins up a Redis container via testcontainers (needs Docker)
```

## Known Limitations / Roadmap

- **No per-role authorization for staff.** Staff roles (`OWNER` / `ADMIN` / `SUPPORT`) exist in the domain model, but admin endpoints only check "is this a staff principal", not the specific role.
- **No retry/backoff on external calls** (SMTP, S3, routing service). A transient failure of an external dependency currently fails the request instead of being retried.
- **No application-level caching.** Caching for map/place lookups was handled at the gateway layer (`Traefik → Kong`), not in application code.
- **Test coverage** is currently limited to the domain and part of the application layer (`tests/unit`), plus one infrastructure integration test against a real Redis instance (`tests/integration`). E2E flows were covered manually during development, not by automated tests.
