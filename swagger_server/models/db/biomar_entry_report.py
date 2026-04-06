from swagger_server.models.db import Base
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    Sequence,
    String,
    Text,
    Time,
    ForeignKey,
    func
)


class BiomarEntryReport(Base):
    __tablename__ = 'biomar_entry_report'
    __table_args__ = {'schema': 'public'}

    id_entry_report = Column(
        Integer,
        primary_key=True,
        nullable=False
    )

    name = Column(Text)
    
    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )