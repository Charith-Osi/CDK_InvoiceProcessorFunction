# 🧾 Azure Durable Functions - Invoice Processing Pipeline

This repository implements a **serverless, event-driven invoice transformation pipeline** using **Azure Durable Functions**.

It is designed to:
- Accept invoice data via a Service Bus trigger or HTTP
- Execute multiple transformation steps (rules)
- Produce a compressed, enriched invoice output ready for downstream processing
