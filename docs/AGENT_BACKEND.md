# Replace Hermes with your own agent

Hermes is an optional placeholder for the external execution agent. You can use any agent framework or service by exposing the compatible API below, or writing an adapter that translates this API to your agent. Changing the URL alone works only if the replacement already supports this protocol and authentication.

1. Deploy your agent backend/adapter separately.
2. Set its HTTPS URL in ignored `Gemini_Live/local_config.h` (`HERMES_BASE_URL`); the tracked example uses `https://agent.example.com`.
3. Ensure its TLS certificate chains to the public root in `hermes_roots.h`, or update that root.
4. Support the authentication headers `CF-Access-Client-Id`, `CF-Access-Client-Secret` and `Authorization: Bearer ...`. If your backend uses another scheme, adapt `hermesHttp()` and runtime configuration accordingly.
5. Build, upload and supply your own runtime credentials as described in SETUP.md.

## Required API

| Request | Expected behavior |
| --- | --- |
| `GET /v1/models` | Authenticated availability check; successful HTTP response. |
| `POST /v1/runs` | Accept JSON `{"input":"user task"}` and `Idempotency-Key`; return HTTP 202 with `{"run_id":"task_123","status":"queued"}`. |
| `GET /v1/runs/task_123` | Return HTTP 200 with `run_id`, `status`, and optional string `output` or `error`. |

Run IDs: 1–128 alphanumeric, underscore or hyphen characters. Deduplicate submissions using the idempotency key, including retries after connection failures. Return JSON with a known Content-Length, at most 65,536 bytes; this firmware rejects unknown-length responses.

Example completed response:

```json
{"run_id":"task_123","status":"completed","output":"The requested task is finished."}
```

Terminal statuses: `completed`, `failed`, `cancelled`, `interrupted`. `waiting_for_approval` raises a notification while the task stays pending. Other statuses continue polling. The bridge truncates output to 6,000 characters and errors to 500 characters.

The internal tool names `submit_hermes_task`, configuration command `configure_hermes`, and Hermes UI/log labels are retained for firmware compatibility; they do not require the backend implementation to be Hermes. Gemini handles voice; the replacement agent handles submitted tasks. Agent capabilities and permissions come from your backend configuration.
