import azure.durable_functions as df
import logging

def orchestrator_function(ctx: df.DurableOrchestrationContext):
    data = ctx.get_input() or {}

    logging.info("Calling activity: Consolidation1a")
    step1a = yield ctx.call_activity("Consolidation1a", data)

    logging.info("Calling activity: Consolidation1b")
    step1b = yield ctx.call_activity("Consolidation1b", step1a)

    return step1b

main = df.Orchestrator.create(orchestrator_function)
