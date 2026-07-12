# Deployment

SmartSpend is deployed as two services:

- `smartspend-web` is a Vite/React site suitable for Vercel.
- `smartspend-core` is a FastAPI service and must be deployed separately.

The backend intentionally keeps temporary analysis sessions in memory. It should run as one long-lived service; it is not suitable for Vercel serverless functions without replacing session storage with a shared store.

## Frontend: Vercel

1. Import the `Alpha-project` GitHub repository into Vercel.
2. Set the **Root Directory** to `SmartSpend/smartspend-web`.
3. Add the environment variable `VITE_API_BASE_URL` with the public URL of the deployed backend, without a trailing slash.
4. Deploy. The included `vercel.json` supports direct visits to React routes such as `/about` and `/how-it-works`.

## Backend

Deploy `SmartSpend/smartspend-core` to a long-running Python host such as Render, Railway, or Fly.io. Use:

```text
Build command: pip install -r requirements.txt
Start command: uvicorn api.app:app --host 0.0.0.0 --port $PORT
```

Set `SMARTSPEND_ALLOWED_ORIGINS` to the exact Vercel URL, for example:

```text
SMARTSPEND_ALLOWED_ORIGINS=https://smartspend.example.vercel.app
```

After deploying both services, upload a small CSV and confirm the preview, analysis, dashboard, and report download flows work from the Vercel URL.
