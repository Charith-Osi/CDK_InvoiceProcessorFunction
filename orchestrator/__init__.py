import re, os
from pathlib import Path
import azure.durable_functions as df

RULE_DIR = re.compile(r"^r\d+_")

def orchestrator_function(ctx: df.DurableOrchestrationContext):
    data  = ctx.get_input() or {}
    base  = Path(__file__).parent.parent      # project root

    rule_dirs = sorted(
        d for d in base.iterdir()
        if d.is_dir() and RULE_DIR.match(d.name)
    )

    for rd in rule_dirs:
        data = yield ctx.call_activity(rd.name, data)

    return data

main = df.Orchestrator.create(orchestrator_function)
