from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.db import Base, engine, get_db
from app.models import SenderAccount, Recipient, Campaign, EmailSend, EngagementEvent
from app.config import DASHBOARD_TITLE
from app.scheduler import start_scheduler
from pathlib import Path

app = FastAPI(title=DASHBOARD_TITLE)

# Ensure database tables exist
Base.metadata.create_all(bind=engine)

# Templates
TEMPLATES_DIR = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@app.on_event("startup")
async def on_startup():
	start_scheduler()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db)):
	campaigns = db.query(Campaign).all()
	senders = db.query(SenderAccount).all()
	recipients_count = db.query(Recipient).count()
	sends = db.query(EmailSend).count()
	opens = db.query(EngagementEvent).filter(EngagementEvent.type == "opened").count()
	replies = db.query(EngagementEvent).filter(EngagementEvent.type == "replied").count()
	bounces = db.query(EngagementEvent).filter(EngagementEvent.type == "bounced").count()
	unsubs = db.query(EngagementEvent).filter(EngagementEvent.type == "unsubscribed").count()

	# Success % as inbox placement over total sends where placement known
	inbox_known = db.query(EmailSend).filter(EmailSend.inbox_placement != None).count()
	inbox_success = db.query(EmailSend).filter(EmailSend.inbox_placement == True).count()
	success_pct = round((inbox_success / inbox_known) * 100, 2) if inbox_known else None

	return templates.TemplateResponse(
		"index.html",
		{
			"request": request,
			"title": DASHBOARD_TITLE,
			"campaigns": campaigns,
			"senders": senders,
			"recipients_count": recipients_count,
			"sends": sends,
			"opens": opens,
			"replies": replies,
			"bounces": bounces,
			"unsubs": unsubs,
			"success_pct": success_pct,
		},
	)


@app.get("/health")
async def health():
	return {"status": "ok"}


@app.get("/unsubscribe")
async def unsubscribe(rid: int, db: Session = Depends(get_db)):
	rec = db.query(Recipient).filter(Recipient.id == rid).first()
	if not rec:
		return {"status": "not_found"}
	rec.unsubscribed = True
	db.commit()
	return {"status": "unsubscribed", "recipient": rec.email}
