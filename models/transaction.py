from sqlalchemy import Integer, String, DateTime, func, ForeignKey, DECIMAL, Column
from sqlalchemy.orm import relationship

from models.base import Base
# from models.account import Account

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    from_account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"))
    to_account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"))
    amount = Column(DECIMAL(10,2), nullable=False)
    type = Column(String(255), nullable= False)
    description = Column(String(255))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    # Relationship list
    from_account = relationship("Account", foreign_keys=[from_account_id])
    to_account = relationship("Account", foreign_keys=[to_account_id])

    def __repr__(self):
        return f'<Transaction {self.id} - {self.type}>'