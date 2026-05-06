from datetime import datetime

from swagger_server.models.db import Base
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Table,
    Text,
    Time,
    ForeignKey,
    func
)

class HistoryDispatchStatus(Base):
    __tablename__ = 'history_dispatch_status'
    __table_args__ = {'schema': 'public'}

    id_history_status = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    dispatch_id = Column(
        Integer,
        ForeignKey('public.dispatch.id_dispatch', onupdate='NO ACTION', ondelete='NO ACTION'),
    )

    previous_status_id = Column(
        Integer,
        ForeignKey('public.dispatch_status.id_status', onupdate='NO ACTION', ondelete='NO ACTION'),
    )

    status_id = Column(
        Integer,
        ForeignKey('public.dispatch_status.id_status', onupdate='NO ACTION', ondelete='NO ACTION'),
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    created_by = Column(Text)

    def to_dict(self):
        result = {}
        for c in self.__table__.columns:
            value = getattr(self, c.name)

            if isinstance(value, datetime):
                value = value.isoformat()

            result[c.name] = value

        return result

