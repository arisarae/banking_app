from sqlalchemy import Integer, String, DateTime, func, ForeignKey, DECIMAL, Column
from sqlalchemy.orm import relationship

from models.base import Base
# from models.transaction import Transaction

class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    account_type = Column(String(255), nullable=False)
    account_number = Column(String(255), nullable=False, unique=True)
    balance = Column(DECIMAL(10,2), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    
    # Relationship list
    user = relationship("User", back_populates="accounts")
    transactions_from = relationship("Transaction", foreign_keys="[Transaction.from_account_id]", back_populates="from_account", cascade="all, delete-orphan")
    transactions_to = relationship("Transaction", foreign_keys="[Transaction.to_account_id]", back_populates="to_account", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Account {self.account_number}>'