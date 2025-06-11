from sqlalchemy import Column, String, Date, DECIMAL, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class InvoiceCompressedLines(Base):
    __tablename__ = "invoice_compressed_lines"

    Invoice_SF_Id = Column(String(50), ForeignKey("invoiceheader.SF_Id"))
    Invoice_Number = Column(String(50), nullable=False)
    Invoice_Date = Column(Date, nullable=False)
    Invoice_Line_SF_Id = Column(String(50), primary_key=True)
    Legacy_BT_CMF = Column(String(50))
    Legacy_ST_CMF = Column(String(50))
    blng_Start_Date = Column(Date)
    blng_End_Date = Column(Date)
    Ship_To_Account_SF = Column(String(50))
    Ship_To_Account_Number = Column(String(50))
    Ship_To_Account_Name = Column(String(100))
    blng_BillingFrequency = Column(String(50))
    Order_Product_SF_ID = Column(String(50))
    Contract_Line = Column(String(50))
    External_Order_Item_ID = Column(String(50))
    blng_Required_By = Column(String(50))
    blng_Notes = Column(Text)
    Product_SF_ID = Column(String(50))
    ProductCode = Column(String(50))
    Description = Column(String(255))
    blng_Charge_Type = Column(String(50))
    blng_Quantity = Column(DECIMAL(10,2), nullable=False)
    blng_Subtotal = Column(DECIMAL(10,2), nullable=False)
    blng_Tax_Amount = Column(DECIMAL(10,2), nullable=False)
    blng_Total_Amount = Column(DECIMAL(10,2), nullable=False)
    CreatedAt = Column(Date)
    UpdatedAt = Column(Date)
    CreatedBy = Column(String(100))
    UpdatedBy = Column(String(100))
    SystemUser = Column(String(100))
    DatabaseUser = Column(String(100))
