# 🧾 Azure Durable Functions - Invoice Processing Pipeline

This repository implements a **serverless, event-driven invoice transformation pipeline** using **Azure Durable Functions**.

It is designed to:
- Accept invoice data via a Service Bus trigger or HTTP
- Execute multiple transformation steps (rules)
- Produce a compressed, enriched invoice output ready for downstream processing

---

## 📁 Project Structure

```bash
.
├── .venv/                      # Python virtual environment
├── host.json                   # Azure Functions host settings
├── local.settings.json         # Local config for runtime + Azurite
├── requirements.txt            # Python dependencies
├── client/                     # Orchestration client (Service Bus trigger)
├── orchestrator/               # Durable orchestrator function
├── Consolidation1a/            # Rule 1: Parent/Child Rollup
├── Consolidation1b/            # Rule 2: Monthly Compression
├── test-payload.json           # Sample invoice JSON input
