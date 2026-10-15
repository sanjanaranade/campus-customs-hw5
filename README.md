# Campus Customs · HW5

Campus Customs is a database-backed multi-agent operations desk with a FastMCP server, FastAPI backend, and React/Vite dashboard. The repository includes both the untouched source database and the working copy used by the app.

## Clean-run rule

The original database is `data/campus_customs.db`; the app uses `data/campus_customs_new.db`. Before a full three-ticket run, reset the working copy by copying the original over it:

```bash
cp data/campus_customs.db data/campus_customs_new.db
```

Never edit the original database. Reset before each clean grading run.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Put your PORTKEY_API_KEY in .env; do not commit .env.
npm --prefix frontend install
```

## Run the services

From the repository root, start the MCP server, FastAPI backend, and React board in separate terminals:

```bash
python -m mcp_server.server
cd backend && uvicorn main:app --reload --port 8000
cd frontend && npm run dev
```

Open `http://localhost:5173`; the backend is at `http://localhost:8000`. The backend allows the Vite origin and the agents use the local MCP tools. Use only `gpt-6-luna` through Portkey, as configured in `.env`.

## Safety and grading notes

Payments require a human approval route, cannot create a negative checking balance, and update the working database only after approval. Customer and vendor communications remain drafts. Audit events append to `output/audit_trail.json`. The `output/` folder contains the harness, smoke evidence, ticket plan, design record, resolved evidence, and the final repository URL.
