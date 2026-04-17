# Postgres for students

## What is inside
- `docker-compose.yml` — starts a clean PostgreSQL container.
- `.env` — database settings.
- `student-sql/` — folder for SQL scripts.

## How to start

1. Clone the repository.
2. Open the repository folder in a terminal.
3. Start PostgreSQL:
   ```bash
   docker compose up -d
   ```
4. Check that the container is running:
   ```bash
   docker compose ps
   ```
5. Connect to the database:
   ```bash
   docker compose exec postgres psql -U student -d student_db
   ```

## Useful commands

Stop the database:
```bash
docker compose down
```

Stop the database and remove data:
```bash
docker compose down -v
```

## Where to put SQL scripts
Put your SQL files in `student-sql/`.

Example:
```bash
student-sql/task1.sql
student-sql/task2.sql
```
