import azure.durable_functions as df
import logging

def orchestrator_function(ctx: df.DurableOrchestrationContext):
    #very first input is the raw JSON dict
    payload = ctx.get_input() or {}

    # Call DataLoad, passing the full payload.  It returns invoice_id (string).
    logging.info("Calling activity: DataLoad")
    invoice_id = yield ctx.call_activity("DataLoad", payload)

    # rule1 (Consolidation1a)
    logging.info("Calling activity: Consolidation1a")
    step1a = yield ctx.call_activity("Consolidation1a", invoice_id)

    # rule2 (Consolidation1b)
    logging.info("Calling activity: Consolidation1b")
    step1b = yield ctx.call_activity("Consolidation1b", step1a)

    # SaveToDb
    logging.info("Calling activity: SaveToDb")
    save_result = yield ctx.call_activity("SaveToDb", step1b)

    return save_result

main = df.Orchestrator.create(orchestrator_function)
