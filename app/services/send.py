from __future__ import annotations
import math
import random
from datetime import datetime, timedelta
from typing import List
from sqlalchemy.orm import Session

from app.models import SenderAccount, Recipient, Campaign, EmailSend
from app.config import DAILY_WARMUP_START, DAILY_WARMUP_MAX, WARMUP_RAMP_DAYS
from app.services.spam import analyze_spam, optimize_sending_pattern
from app.services.personalize import generate_variation
from app.services.analytics import record_event
from app.services.compliance import build_unsubscribe_link, append_compliance_footer


def _current_warmup_cap(days_active: int) -> int:
	if days_active >= WARMUP_RAMP_DAYS:
		return DAILY_WARMUP_MAX
	increment = (DAILY_WARMUP_MAX - DAILY_WARMUP_START) / max(WARMUP_RAMP_DAYS, 1)
	return int(DAILY_WARMUP_START + increment * days_active)


def _select_sender_accounts(db: Session) -> List[SenderAccount]:
	return db.query(SenderAccount).filter(SenderAccount.active == True).all()


def _eligible_recipients(db: Session, limit: int) -> List[Recipient]:
	return db.query(Recipient).filter(Recipient.unsubscribed == False).limit(limit).all()


def _estimated_days_active(sender: SenderAccount) -> int:
	# Simulate warmup progression using reputation and last_sent timestamps
	base = 10 if sender.warmup_enabled else WARMUP_RAMP_DAYS
	boost = int(sender.reputation_score * 10)
	return min(WARMUP_RAMP_DAYS, base + boost)


def run_sending_cycle(db: Session) -> None:
	senders = _select_sender_accounts(db)
	if not senders:
		return

	campaign = db.query(Campaign).filter(Campaign.active == True).first()
	if not campaign:
		return

	# Determine global spam score from template to adjust volumes
	base_spam = analyze_spam(campaign.subject_template + "\n" + campaign.body_template)
	volume_mul, jitter_mul = optimize_sending_pattern(base_spam)

	for sender in random.sample(senders, len(senders)):
		days_active = _estimated_days_active(sender)
		cap = _current_warmup_cap(days_active)
		cap = max(1, int(cap * volume_mul))

		# Randomize actual sends this cycle
		cycle_quota = max(1, int(cap / 12))  # roughly per-hour in 12 ticks/day
		cycle_quota = max(1, int(random.uniform(0.6, 1.2 * jitter_mul) * cycle_quota))

		recipients = _eligible_recipients(db, cycle_quota)
		if not recipients:
			continue

		for r in recipients:
			fields = {
				"name": r.name,
				"role": r.role,
				"company": r.company,
				"industry": r.industry,
			}
			p = generate_variation(campaign.subject_template, campaign.body_template, fields)
			spam_score = analyze_spam(p.personalized_subject + "\n" + p.personalized_body)

			unsub_link = build_unsubscribe_link("/", r.id)
			body_with_footer = append_compliance_footer(p.personalized_body, sender.email, unsub_link)

			send = EmailSend(
				sender_id=sender.id,
				recipient_id=r.id,
				campaign_id=campaign.id,
				subject=p.personalized_subject,
				body=body_with_footer,
				personalization_score=p.score,
				spam_score=spam_score,
				inbox_placement=None,
				sent_at=datetime.utcnow(),
			)
			db.add(send)
			db.commit()

			# Simulate deliverability based on spam and personalization
			deliver_prob = max(0.05, 0.9 - spam_score * 0.7 + p.score * 0.4 + sender.reputation_score * 0.2)
			placed_in_inbox = random.random() < deliver_prob
			send.inbox_placement = placed_in_inbox
			db.commit()

			# Engagement simulation
			if placed_in_inbox:
				record_event(db, send, r.id, "delivered")
				open_prob = min(0.85, 0.25 + p.score * 0.5)
				if random.random() < open_prob:
					record_event(db, send, r.id, "opened")
					reply_prob = max(0.01, 0.03 + p.score * 0.2)
					if random.random() < reply_prob:
						record_event(db, send, r.id, "replied")
			else:
				record_event(db, send, r.id, "bounced")

			# Occasional unsubscribe
			if random.random() < 0.002:
				record_event(db, send, r.id, "unsubscribed")
