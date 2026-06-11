from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm  import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
import uuid

from app.db.database import Base

class VerificationCode(Base):
    __tablename__ = "codes"
    
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )
    
    user_email: Mapped[str] = mapped_column(
        ForeignKey("users.email", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    
    code: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    
    user: Mapped["User"] = relationship( # type: ignore
        back_populates="codes"
    )