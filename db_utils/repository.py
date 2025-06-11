# shared/repository.py

import logging
from typing import List
from .db import SessionLocal
from .models import InvoiceHeaderORM, InvoiceDetailORM

class InvoiceRepository:
    def __init__(self):
        self.db = SessionLocal()

    def insert_header(self, header_data: dict):
        """
        Insert a new header. If you want to skip duplicates, catch the integrity error.
        """
        header_id = header_data["Id"]
        existing = (
            self.db.query(InvoiceHeaderORM)
                   .filter(InvoiceHeaderORM.Id == header_id)
                   .one_or_none()
        )
        if existing:
            return
        
        header = InvoiceHeaderORM(
            Id                      = header_data["Id"],
            Name                    = header_data.get("Name"),
            FIN_Invoice_Date__c     = header_data.get("FIN_Invoice_Date__c"),
            Total_Amount__c         = header_data.get("Total_Amount__c"),
            FIN_Due_Date__c         = header_data.get("FIN_Due_Date__c"),
            Dispute_Comments__c     = header_data.get("Dispute_Comments__c"),
            CID_Cancelled__c        = header_data.get("CID_Cancelled__c"),
            blng__InvoiceBatches__c = header_data.get("blng__InvoiceBatches__c"),
            Bill_To_Account_SF_Id   = header_data.get("Bill_To_Account_SF_Id"),
            Bill_To_AccountNumber   = header_data.get("Bill_To_AccountNumber"),
            Bill_To_AccountName     = header_data.get("Bill_To_AccountName"),
            BillingCity             = header_data.get("BillingCity"),
            BillingState            = header_data.get("BillingState"),
            BillingPostalCode       = header_data.get("BillingPostalCode"),
            BillingStreet           = header_data.get("BillingStreet"),
            Email_List              = header_data.get("Email_List"),
            FIN_Langauge__c         = header_data.get("FIN_Langauge__c"),
            FIN_Invoice_Delivery_Method__c = header_data.get("FIN_Invoice_Delivery_Method__c")
        )
        self.db.add(header)
        logging.info("Queued INSERT for InvoiceHeader Id=%s", header.Id)

    def insert_details(self, header_id: str, details: List[dict]):
        for d in details:
            detail = InvoiceDetailORM(
                Header_Id               = header_id,
                Invoice_SF_Id           = d.get("Invoice_SF_Id"),
                Invoice_Number          = d.get("Invoice_Number"),
                Invoice_Date            = d.get("Invoice_Date"),
                Invoice_Line_SF_Id      = d.get("Invoice_Line_SF_Id"),
                FIN_Invoice_Ship_to_Account__c = d.get("FIN_Invoice_Ship_to_Account__c"),
                Ship_To_AccountNumber   = d.get("Ship_To_AccountNumber"),
                Ship_To_AccountName     = d.get("Ship_To_AccountName"),
                blng__BillingFrequency__c = d.get("blng__BillingFrequency__c"),
                Order_Product_SF_ID     = d.get("Order_Product_SF_ID"),
                Contract_Line__c        = d.get("Contract_Line__c"),
                External_Order_Item_ID__c = d.get("External_Order_Item_ID__c"),
                blng__RequiredBy__c     = d.get("blng__RequiredBy__c"),
                blng__Notes__c          = d.get("blng__Notes__c"),
                Product_SF_ID           = d.get("Product_SF_ID"),
                ProductCode             = d.get("ProductCode"),
                Description             = d.get("Description"),
                blng__ChargeType__c     = d.get("blng__ChargeType__c"),
                blng__Quantity__c       = float(d.get("blng__Quantity__c") or 0),
                blng__Subtotal__c       = float(d.get("blng__Subtotal__c") or 0),
                blng__TaxAmount__c      = float(d.get("blng__TaxAmount__c") or 0),
                blng__TotalAmount__c    = float(d.get("blng__TotalAmount__c") or 0)
            )
            self.db.add(detail)
        logging.info("Queued INSERT of %d InvoiceDetail lines for Header_Id=%s", len(details), header_id)

    def commit_and_close(self):
        try:
            self.db.commit()
            logging.info("Committed transaction.")
        except Exception as e:
            self.db.rollback()
            logging.exception("Rollback after error: %s", e)
            raise
        finally:
            self.db.close()
            logging.info("Session closed.")
