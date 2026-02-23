# Posit Connect Deployment (Flask API)

This project can be deployed to Posit Connect without changing the Flask entrypoint.

## 1) Entry point check

- Flask app object: `app/main.py` -> `app = Flask(...)`
- Deploy entrypoint should be: `app.main:app`
- The `if __name__ == "__main__": ...` block is only for local run and can remain unchanged.

## 2) Install rsconnect-python

```bash
python3 -m pip install --upgrade rsconnect-python
rsconnect version
```

## 3) Add Posit Connect server with API key

Create an API key in Posit Connect web UI first, then run:

```bash
# safer: avoid putting API key directly in shell history
export CONNECT_API_KEY="<YOUR_API_KEY>"

rsconnect add \
  --name my-connect \
  --server https://<your-connect-domain> \
  --api-key-envvar CONNECT_API_KEY
```

## 4) Deploy this API

From repository root (`/Users/zhuricardo/Desktop/5381`):

```bash
rsconnect deploy api \
  --server my-connect \
  --entrypoint app.main:app \
  .
```

## 5) Notes

- Keep `requirements.txt` for runtime dependencies only.
- Keep dev/test dependencies in `requirements-dev.txt`.
- Existing DigitalOcean files (for example `Procfile`) can stay; they do not block Posit Connect deployment.

## Posit Connect Cloud (GitHub + Shiny)

If you are using Posit Connect Cloud UI and want direct GitHub publishing:

1. Choose framework: `Shiny`
2. Select your GitHub repository and branch
3. Set primary file to `app.py`
4. Publish

This repository now includes `app.py` (Shiny for Python app) for that workflow.
