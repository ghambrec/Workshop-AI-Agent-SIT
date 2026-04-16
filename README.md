
# Logistics Order Extraction Agent

An AI agent that reads incoming freight forwarding emails and extracts structured order data for a Transport Management System (TMS). The agent automatically replies to the sender — confirming a complete order or requesting any missing information.

## Features

- **Email-to-Order Extraction:** Parses unstructured email bodies into a validated Pydantic order schema.
- **Gmail Integration:** Reads unread emails via the Gmail API and replies within the same thread.
- **Structured Output:** Produces a typed `AgentResponse` with full order data or a list of missing fields.
- **Automatic Reply:** Calls `send_mail` as a tool — confirmed orders get a friendly confirmation, incomplete orders get a polite follow-up request.
- **Observability:** Every agent run is traced in Langfuse for full visibility.
- **Evaluation Pipeline:** Automated experiment runs with LLM-based and trajectory-based metrics via DeepEval.

---

## Prerequisites

- **Python 3.13+**
- **uv** (Python package manager)
- A **Google Cloud Project** with the **Vertex AI API** enabled
- A **Service Account JSON key** (`gcloud.json`) in the root directory
- A **Gmail OAuth2 credentials file** (`gmail_credentials.json`) in the root directory
- A **Langfuse** account with a project configured

---

## Setup

### 1. Install dependencies

```bash
uv sync
```

### 2. Environment variables

Copy the template and fill in your credentials:

```bash
cp template.env .env
```

```env
GOOGLE_APPLICATION_CREDENTIALS="/path/to/gcloud.json"
LANGFUSE_PUBLIC_KEY="pk-lf-..."
LANGFUSE_SECRET_KEY="sk-lf-..."
LANGFUSE_HOST="https://cloud.langfuse.com"
```

### 3. Gmail OAuth2

Place your `gmail_credentials.json` (downloaded from Google Cloud Console) in the root directory. On first run, a browser window will open for authentication. The token is saved to `token.json` and reused automatically.

---

## Running the Application

```bash
uv run uvicorn app.main:app --reload
```

API docs available at `http://localhost:8000/docs`.

---

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/order/create` | Extract an order from a raw email body (JSON: `{"emailBody": "..."}`) |
| `GET` | `/order/processMail` | Fetch the latest unread Gmail, extract the order, and reply to the sender |

---

## Project Structure

```
app/
  main.py                     # FastAPI app entry point
  prompts/soul.md             # System prompt for the agent
  models/
    order.py                  # Order schema + AgentResponse
    evaluation.py             # EvalSuite / EvalItem models
  services/
    agent.py                  # PydanticAI agent definition
    gmail.py                  # Gmail API: fetch + send
    database.py               # Writes extracted orders to data/order.json
  routers/
    order.py                  # HTTP route handlers
  evaluation/
    evaluators.py             # answer_relevancy + tool_calling_accuracy
    providers.py              # DeepEval VertexGemini adapter
data/
  order.json                  # Last extracted order
  evaluation_data/
    eval_data.json            # Evaluation test cases
scripts/
  run_evaluation_pipeline.py  # Runs the full evaluation experiment
```

---

## Evaluation Pipeline

The pipeline uploads test cases to Langfuse, runs the agent against each one, and scores the results automatically.

### Metrics

- `answer_relevancy` — LLM-based: how relevant is the agent's output to the input?
- `tool_call_accuracy` — Trajectory-based: did the agent call the expected tools (`send_mail`)?

### Running evaluations

```bash
uv run python -m scripts.run_evaluation_pipeline
```

### Test cases

Stored in `data/evaluation_data/eval_data.json`. Each item contains:

- `question` — the raw email text passed to the agent
- `expected_output` — the expected summary (status, shipper, consignee, goods, weight, pickup date)
- `metadata.expected_tool_calls` — tools the agent should have called (e.g. `["send_mail"]`)
