from datetime import datetime
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db import Base


class SenderAccount(Base):
	__tablename__ = "sender_accounts"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
	email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
	provider: Mapped[str] = mapped_column(String(50), default="generic")
	active: Mapped[bool] = mapped_column(Boolean, default=True)
	warmup_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
	warmup_level: Mapped[int] = mapped_column(Integer, default=0)
	last_sent_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
	reputation_score: Mapped[float] = mapped_column(Float, default=0.5)

	sent_emails: Mapped[list["EmailSend"]] = relationship("EmailSend", back_populates="sender")


class Recipient(Base):
	__tablename__ = "recipients"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
	email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
	name: Mapped[str | None] = mapped_column(String(255), nullable=True)
	role: Mapped[str | None] = mapped_column(String(255), nullable=True)
	company: Mapped[str | None] = mapped_column(String(255), nullable=True)
	industry: Mapped[str | None] = mapped_column(String(255), nullable=True)
	unsubscribed: Mapped[bool] = mapped_column(Boolean, default=False)
	created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

	events: Mapped[list["EngagementEvent"]] = relationship("EngagementEvent", back_populates="recipient")
	sends: Mapped[list["EmailSend"]] = relationship("EmailSend", back_populates="recipient")


class Campaign(Base):
	__tablename__ = "campaigns"

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
	subject_template: Mapped[str] = mapped_column(String(255), nullable=False)
	body_template: Mapped[str] = mapped_column(Text, nullable=False)
	active: Mapped[bool] = mapped_column(Boolean, default=True)
	created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

	sends: Mapped[list["EmailSend"]] = relationship("EmailSend", back_populates="campaign")


class EmailSend(Base):
	__tablename__ = "email_sends"

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	sender_id: Mapped[int] = mapped_column(Integer, ForeignKey("sender_accounts.id"))
	recipient_id: Mapped[int] = mapped_column(Integer, ForeignKey("recipients.id"))
	campaign_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("campaigns.id"), nullable=True)
	subject: Mapped[str] = mapped_column(String(255))
	body: Mapped[str] = mapped_column(Text)
	personalization_score: Mapped[float] = mapped_column(Float, default=0.0)
	spam_score: Mapped[float] = mapped_column(Float, default=0.0)
	inbox_placement: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
	sent_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

	sender: Mapped[SenderAccount] = relationship("SenderAccount", back_populates="sent_emails")
	recipient: Mapped[Recipient] = relationship("Recipient", back_populates="sends")
	campaign: Mapped[Campaign | None] = relationship("Campaign", back_populates="sends")
	events: Mapped[list["EngagementEvent"]] = relationship("EngagementEvent", back_populates="send")


class EngagementEvent(Base):
	__tablename__ = "engagement_events"

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	send_id: Mapped[int] = mapped_column(Integer, ForeignKey("email_sends.id"))
	recipient_id: Mapped[int] = mapped_column(Integer, ForeignKey("recipients.id"))
	type: Mapped[str] = mapped_column(String(50))
	details: Mapped[str | None] = mapped_column(Text, nullable=True)
	created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

	send: Mapped[EmailSend] = relationship("EmailSend", back_populates="events")
	recipient: Mapped[Recipient] = relationship("Recipient", back_populates="events")
