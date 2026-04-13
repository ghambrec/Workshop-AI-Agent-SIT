
# 🛒 Workshop-Agents: Retail Assistant & Evaluation Lab

Welcome to the **Workshop-Agents** repository! This project is a hands-on lab designed to teach the fundamentals of building, tracing, and evaluating AI Agents.

The core of this workshop features a "Broken Agent"—a sophisticated conversational assistant that is helpful and polite but contains critical business logic flaws. This provides the perfect baseline for learning how to use evaluation frameworks to catch silent AI failures.

## 🚀 Features
- **Vertex AI Integration:** Enterprise-grade authentication using Google Cloud Service Accounts.
- **Stateful JSON Database:** A mock store database that tracks inventory, pricing, and sales.
- **Automatic Seed Reset:** The database automatically resets to its original state on every startup for consistent testing.
- **Agentic Capabilities:** The agent can fetch store data, restock items, adjust individual prices, and apply category-wide discounts.
- **Conversational Memory:** Native support for session-based chat history and context retention.

---

## 🛠️ Prerequisites
- **Python 3.13+**
- **uv** (Modern Python package manager)
- A **Google Cloud Project** with the **Vertex AI API** enabled.
- A **Service Account JSON key** file (`gcloud.json`) located in the root directory.

---

## ⚙️ Setup Instructions

### 1. Project Initialization
This project uses `uv` for ultra-fast dependency management and environment isolation.

```bash
# Clone the repository
git clone <your-repo-url>
cd Workshop-Agents

# Synchronize dependencies and create virtual environment
uv sync

# Activate the virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Environment Configuration
Credentials are managed via a `.env` file. Do not commit your actual `.env` file to version control.

1. Copy the template file:
   ```bash
   cp template.env .env
   ```
2. Open `.env` and provide the **path** to your service account key:
   ```env
   GOOGLE_APPLICATION_CREDENTIALS="/path/to/gcloud.json"
   ```

### 3. Database Initialization
Ensure your `data/` folder contains the file `initial_store.json`. The application will automatically create a working `store.json` copy every time the server boots.

---

## 🏃 Running the Application

Start the FastAPI server using `uv`:

```bash
uv run python -m app.main
```

The server will start at `http://localhost:8000`. You can test the endpoints via the interactive Swagger docs at `http://localhost:8000/docs`.

---

## 📁 Project Structure
- `app/main.py`: Entry point and server lifespan management (DB resets).
- `app/services/agent.py`: Pydantic AI Agent definition, persona, and tool wiring.
- `app/services/database.py`: File-based CRUD logic with JSON "Seed" pattern.
- `app/routers/assistant.py`: FastAPI endpoints and session-based chat memory.
- `app/evaluation/`: Evaluation metrics and models.
- `data/`: Directory for JSON database files and evaluation datasets.
- `scripts/run_evaluation_pipeline.py`: Main entry point for running the evaluation experiment.

---

## 📊 Evaluation Pipeline

The project includes a robust evaluation pipeline to measure agent performance using **Langfuse** for experiment tracking and **DeepEval** for LLM-based metrics.

### 1. Key Components
- **Dataset Management:** Automatic dataset creation and versioning in Langfuse.
- **LLM-based Metrics:**
    - `answer_relevancy`: Measures how relevant the agent's response is to the input question.
    - `tool_calling_accuracy`: Evaluates if the agent called the correct tools in the right sequence.
- **Human-in-the-loop:** Automatically creates annotation queues in Langfuse for manual review of agent traces.

### 2. Running Evaluations
Ensure you have your Langfuse credentials configured in your `.env` file:
```env
LANGFUSE_PUBLIC_KEY="pk-lf-..."
LANGFUSE_SECRET_KEY="sk-lf-..."
LANGFUSE_HOST="https://cloud.langfuse.com"
```

To run the full evaluation suite:
```bash
uv run python -m scripts.run_evaluation_pipeline
```

### 3. Evaluation Data
Evaluation test cases are stored in `data/evaluation_data/eval_data.json`. Each test case includes:
- `question`: The input for the agent.
- `expected_output`: The desired natural language response.
- `metadata`: Contains `expected_tool_calls` for trajectory validation.