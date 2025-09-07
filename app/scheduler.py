from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.services.send import run_sending_cycle

_scheduler: BackgroundScheduler | None = None


def _tick():
	# Run one send cycle periodically
	db: Session = SessionLocal()
	try:
		run_sending_cycle(db)
	except Exception:
		# Best-effort background; avoid crashing scheduler
		pass
	finally:
		db.close()


def start_scheduler():
	global _scheduler
	if _scheduler is not None:
		return
	_scheduler = BackgroundScheduler()
	_scheduler.add_job(_tick, IntervalTrigger(seconds=10), max_instances=1, coalesce=True)
	_scheduler.start()
