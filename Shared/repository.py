# shared/repository.py

import logging
from typing import List
from .db import get_connection
from .models import InvoiceHeader, InvoiceDetail

class InvoiceRepository:
    """Encapsulates all DB operations for InvoiceHeader and InvoiceDetail."""

    def __init__(self):
        self.conn = get_connection()

    def upsert_header(self, header: InvoiceHeader):
        """
        Insert or replace the InvoiceHeader row.
        Uses REPLACE INTO so that if the Id already exists, it overwrites.
        """
        sql = """
        REPLACE INTO InvoiceHeader (
          Id, Name, FIN_Invoice_Date, Total_Amount,
          FIN_Due_Date, Dispute_Comments, CID_Cancelled,
          blng_InvoiceBatches, Bill_To_Account_SF_Id,
          Bill_To_AccountNumber, Bill_To_AccountName,
          BillingCity, BillingState, BillingPostalCode,
          BillingStreet, Email_List, FIN_Language,
          FIN_Invoice_Delivery
        ) VALUES (
          %s, %s, %s, %s,
          %s, %s, %s,
          %s, %s, %s,
          %s, %s, %s, %s,
          %s, %s, %s, %s
        )
        """
        params = (
            header.Id,
            header.Name,
            header.FIN_Invoice_Date__c,
            header.Total_Amount__c,
            header.FIN_Due_Date__c,
            header.Dispute_Comments__c,
            header.CID_Cancelled__c,
            header.blng__InvoiceBatches__c,
            header.Bill_To_Account_SF_Id,
            header.Bill_To_AccountNumber,
            header.Bill_To_AccountName,
            header.BillingCity,
            header.BillingState,
            header.BillingPostalCode,
            header.BillingStreet,
            header.Email_List,
            header.FIN_Langauge__c,
            header.FIN_Invoice_Delivery_Method__c
        )

        with self.conn.cursor() as cursor:
            cursor.execute(sql, params)
        logging.info("Upserted InvoiceHeader Id=%s", header.Id)

    def delete_details_for_header(self, header_id: str):
        """Delete any existing details for that InvoiceHeader."""
        sql = "DELETE FROM InvoiceDetail WHERE Header_Id = %s"
        with self.conn.cursor() as cursor:
            cursor.execute(sql, (header_id,))
        logging.info("Deleted existing InvoiceDetail for Header_Id=%s", header_id)

    def insert_details(self, header_id: str, details: List[InvoiceDetail]):
        """
        Insert each InvoiceDetail row. All numeric strings are cast to float.
        """
        sql = """
        INSERT INTO InvoiceDetail (
          Header_Id,
          Invoice_SF_Id, Invoice_Number, Invoice_Date,
          Invoice_Line_SF_Id, FIN_Invoice_Ship_to,
          Ship_To_AccountNumber, Ship_To_AccountName,
          blng_BillingFrequency, Order_Product_SF_ID,
          Contract_Line, External_Order_Item_ID,
          blng_RequiredBy, blng_Notes, Product_SF_ID,
          ProductCode, Description, blng_ChargeType,
          blng_Quantity, blng_Subtotal, blng_TaxAmount,
          blng_TotalAmount
        ) VALUES (
          %s, %s, %s, %s,
          %s, %s, %s, %s,
          %s, %s, %s, %s,
          %s, %s, %s, %s,
          %s, %s, %s, %s,
          %s, %s
        )
        """

        with self.conn.cursor() as cursor:
            for line in details:
                params = (
                    header_id,
                    line.Invoice_SF_Id,
                    line.Invoice_Number,
                    line.Invoice_Date,
                    line.Invoice_Line_SF_Id,
                    line.FIN_Invoice_Ship_to_Account__c,
                    line.Ship_To_AccountNumber,
                    line.Ship_To_AccountName,
                    line.blng__BillingFrequency__c,
                    line.Order_Product_SF_ID,
                    line.Contract_Line__c,
                    line.External_Order_Item_ID__c,
                    line.blng__RequiredBy__c,
                    line.blng__Notes__c,
                    line.Product_SF_ID,
                    line.ProductCode,
                    line.Description,
                    line.blng__ChargeType__c,
                    float(line.blng__Quantity__c or 0),
                    float(line.blng__Subtotal__c or 0),
                    float(line.blng__TaxAmount__c or 0),
                    float(line.blng__TotalAmount__c or 0),
                )
                cursor.execute(sql, params)
        logging.info("Inserted %d InvoiceDetail lines for Header_Id=%s", len(details), header_id)

    def commit_and_close(self):
        """Commit the transaction and close the connection."""
        self.conn.commit()
        self.conn.close()
        logging.info("DB connection committed and closed.")
