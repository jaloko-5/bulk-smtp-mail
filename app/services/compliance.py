from urllib.parse import urlencode


def build_unsubscribe_link(base_url: str, recipient_id: int) -> str:
	params = urlencode({"rid": recipient_id})
	return f"{base_url.rstrip('/')}\/unsubscribe?{params}"


def append_compliance_footer(body: str, sender_identity: str, unsub_link: str) -> str:
	footer = f"\n\n—\nYou are receiving this because we thought it might be relevant.\nSender: {sender_identity}\nUnsubscribe: {unsub_link}"
	return body.rstrip() + footer
