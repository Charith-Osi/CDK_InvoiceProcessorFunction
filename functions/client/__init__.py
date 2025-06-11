import logging, json
import azure.functions as func
import azure.durable_functions as df

async def main(req: func.HttpRequest, starter: str) -> func.HttpResponse:
    client = df.DurableOrchestrationClient(starter)
    payload = req.get_json()
    instance_id = await client.start_new("orchestrator", None, payload)
    logging.info(f"Started orchestration: {instance_id}")
    return client.create_check_status_response(req, instance_id)
