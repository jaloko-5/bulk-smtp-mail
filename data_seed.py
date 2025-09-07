from sqlalchemy.orm import Session
from app.db import Base, engine, SessionLocal
from app.models import SenderAccount, Recipient, Campaign


def seed():
	Base.metadata.create_all(bind=engine)
	db: Session = SessionLocal()
	try:
		if db.query(SenderAccount).count() == 0:
			db.add_all([
				SenderAccount(email="alice.sender@example.com", provider="gmail", reputation_score=0.6),
				SenderAccount(email="bob.sender@example.com", provider="outlook", reputation_score=0.55),
			])
			print("Seeded sender accounts")

		if db.query(Recipient).count() == 0:
			recs = []
			for i in range(1, 501):
				recs.append(Recipient(
					email=f"prospect{i}@example.org",
					name=f"Prospect {i}",
					role="Operations Manager" if i % 3 == 0 else "Marketing Lead",
					company=f"Company {i}",
					industry="SaaS" if i % 2 == 0 else "E-commerce",
				))
			db.add_all(recs)
			print("Seeded recipients")

		if db.query(Campaign).count() == 0:
			db.add(Campaign(
				name="Intro Sequence",
				subject_template="{{greeting}} {{name}}, quick idea for {{company}}",
				body_template=(
					"{{greeting}} {{name}},\n\n"
					"I help {{industry}} teams like {{company}}'s {{role}} hit goals faster by reducing manual outreach.\n"
					"Would it be crazy to share a 3-line idea tailored to {{company}}?\n\n"
					"Best,\nAlex"
				),
				active=True,
			))
			print("Seeded campaign")

		db.commit()
	finally:
		db.close()


if __name__ == "__main__":
	seed()
