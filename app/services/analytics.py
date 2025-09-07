from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import EmailSend, EngagementEvent


def record_event(db: Session, send: EmailSend, recipient_id: int, event_type: str, details: str | None = None) -> None:
	event = EngagementEvent(send_id=send.id, recipient_id=recipient_id, type=event_type, details=details)
	db.add(event)
	db.commit()


def compute_engagement_trend(db: Session, days: int = 14):
	cutoff = datetime.utcnow() - timedelta(days=days)
	rows = (
		db.query(EngagementEvent)
		.filter(EngagementEvent.created_at >= cutoff)
		.all()
	)
	counts: dict[str, int] = {}
	for r in rows:
		counts[r.type] = counts.get(r.type, 0) + 1
	return counts
