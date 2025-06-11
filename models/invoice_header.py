from sqlalchemy import Column, String, Date, Boolean, DECIMAL, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class InvoiceHeader(Base):
    __tablename__ = "invoiceheader"

    SF_Id = Column(String(50), primary_key=True)
    Name = Column(String(50), nullable=False)
    FIN_Invoice_Date = Column(Date, nullable=False)
    Total_Amount = Column(DECIMAL(10, 2), nullable=False)
    FIN_Due_Date = Column(Date, nullable=False)
    Dispute_Comments = Column(Text)
    CID_Cancelled = Column(Boolean, nullable=False, default=False)
    blng_InvoiceBatches = Column(String(50))
    Bill_To_Account_SF_Id = Column(String(50))
    Bill_To_AccountNumber = Column(String(50))
    Bill_To_AccountName = Column(String(100))
    Billing_City = Column(String(100))
    Billing_State = Column(String(50))
    Billing_Postal_Code = Column(String(20))
    Billing_Street = Column(String(255))
    Billing_Country = Column(String(255))
    Email_List = Column(Text)
    FIN_Language = Column(String(50))
    FIN_Invoice_Delivery_Method = Column(String(50))
    Status = Column(String(50))
    Completion_Date = Column(Date)
    Comments = Column(Text)
    CreatedAt = Column(Date)
    UpdatedAt = Column(Date)
    CreatedBy = Column(String(100))
    UpdatedBy = Column(String(100))
    SystemUser = Column(String(100))
    DatabaseUser = Column(String(100))

    # Relationships can be added here if needed
