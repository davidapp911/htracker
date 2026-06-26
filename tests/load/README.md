# Load Testing

Tool: [Locust](https://locust.io)  
Target: Railway production backend  
Users: 50 concurrent  
Duration: ~2.5 minutes  
Date: 2026-06-26

## Running

```bash
locust -f tests/load/locustfile.py
```

Then open `http://localhost:8089`, set users to 50, spawn rate to 5, and start.

The base URL is read from `LOAD_TEST_URL` in `.env`.

## Scenario

Each virtual user:
1. Registers a unique account and logs in (once, on spawn)
2. Creates one habit (once, on spawn)
3. Loops continuously:
   - `GET /habits/` (weight 3)
   - `POST /habits/{id}/logs` with today's date (weight 2)
   - `GET /stats/summary` (weight 2)

## Baseline results (2026-06-26)

50 concurrent users, ~5 minutes, warm Railway instance.

| Endpoint | Requests | Failures | p50 | p95 | p99 | max |
|---|---|---|---|---|---|---|
| GET /habits/ | 3158 | 0 | 66ms | 73ms | 100ms | 304ms |
| GET /stats/summary | 2185 | 0 | 68ms | 76ms | 120ms | 290ms |
| POST /habits/{id}/logs | ~50 success / ~2150 409 | — | 68ms | 77ms | — | — |

Auth endpoints (login ~260ms, register ~370ms on warm instance) are one-time setup costs, not looped — not included in the baseline.

## Notes

- The unique constraint on `(habit_id, logged_at)` means repeated completions for the
  same habit on the same day return 409. This is expected behaviour, not an error.
  Each virtual user gets exactly one successful completion per run; all subsequent
  attempts return 409 at similar latency (~68ms).
- First cold-start run showed higher auth latency (login ~767ms, register ~1008ms)
  which dropped significantly once Railway was warm.
