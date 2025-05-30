import logging
from collections import defaultdict

def main(payload):
    header  = payload.get("Consolidated_Invoice", {})
    lines   = payload.get("Invoice_Details", [])

    groups = defaultdict(list)
    for ln in lines:
        groups[ln.get("Contract_Line__c")].append(ln)

    compressed = []
    for contract, grp in groups.items():
        base = grp[0].copy()

        qty_sum   = sum(float(l.get("blng__Quantity__c") or 0)     for l in grp)
        tot_sum   = sum(float(l.get("blng__TotalAmount__c") or 0)  for l in grp)

        monthly_present = any(
            (l.get("blng__BillingFrequency__c") or "").lower() == "monthly"
            for l in grp
        )

        if monthly_present:
            # output a single, monthly, aggregated line
            base["blng__BillingFrequency__c"] = "Monthly"
            base["blng__Quantity__c"]    = str(qty_sum)
            base["blng__TotalAmount__c"] = str(tot_sum)
            compressed.append(base)
        else:
            compressed.extend(grp)

    result = {
        "Consolidated_Invoice": header,
        "Invoice_Details": compressed
    }
    logging.info("Compression Result:\n%s", result)
    return result
