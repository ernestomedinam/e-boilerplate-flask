from app_name.db import db, ModelBase
from datetime import datetime, timezone
from enum import Enum

# ticked status enums
class TicketStatus(Enum):
    OPEN = "open"
    CLOSED = "closed"

# support ticket simple class
class BasicSupportTicket(ModelBase):
    """
        a basic ticket for client support.
            nametag: client's nametag
            status: ["open", "closed"]
            created_at: timestamp for ticket creation
            closed_ad: timestamp for ticket resolution
    """
    id = db.Column(db.Integer, primary_key=True)
    nametag = db.Column(db.String(120), nullable=False)
    status = db.Column(db.Enum(TicketStatus), nullable=False, default="open")
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)
    closed_at = db.Column(db.DateTime(timezone=True))

    def __init__(self, nametag):
        self.nametag = nametag.strip()
        self.created_at = datetime.now(timezone.utc)
    
    @classmethod
    def create(cls, nametag):
        new_ticket = cls(nametag)
        try:
            db.session.add(new_ticket)
            db.session.commit()
            return new_ticket
        except:
            db.session.rollback()
            return {
                "text": "something went wrong on db",
                "status_code": 500
            }

    def close(self):
        self.status = "closed"
        self.closed_at = datetime.now(timezone.utc)
        try:
            db.session.commit()
            return True
        except Exception as error:
            db.session.rollback()
            return {
                "text": error,
                "status_code": 500
            }
    def serialize(self):
        return {
            "id": self.id,
            "nametag": self.nametag,
            "status": self.status.value,
            "created_at": self.created_at.isoformat() + "Z" if self.created_at is not None else "",
            "closed_at": self.closed_at.isoformat() + "Z" if self.closed_at is not None else ""
        }
