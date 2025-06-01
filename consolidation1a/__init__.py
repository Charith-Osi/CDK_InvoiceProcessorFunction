"""
r01_consolidation1a – parent/child roll-up
"""
import logging

def main(payload: dict): # gets a dict automatically
    logging.info("Consolidation1a IN: %s", payload)

    consolidated = payload.get("Consolidated_Invoice", {})
    lines        = payload.get("Invoice_Details", [])

    parents = [l.copy() for l in lines if not l.get("blng__RequiredBy__c")]

    sums = {}
    for l in lines:
        parent = l.get("blng__RequiredBy__c")
        if parent:
            amt = float(l.get("blng__TotalAmount__c") or 0)
            sums[parent] = sums.get(parent, 0) + amt

    for p in parents:
        pid = p.get("External_Order_Item_ID__c")
        if pid in sums:
            p["blng__TotalAmount__c"] = str(sums[pid])

    result = {
        "Consolidated_Invoice": consolidated,
        "Invoice_Details": parents
    }
    logging.info("Consolidation1a OUT: %s", result)
    return result  # runtime re-serialises to JSON
