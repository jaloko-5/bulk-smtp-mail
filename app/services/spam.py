import re
from typing import Tuple

SPAM_WORDS = {
	"free", "win", "winner", "prize", "urgent", "guarantee", "act now",
	"risk-free", "100%", "credit", "loan", "cash", "$$$", "viagra",
}


def analyze_spam(text: str) -> float:
	if not text:
		return 0.0
	lower = text.lower()
	count = 0
	for w in SPAM_WORDS:
		if re.search(rf"\b{re.escape(w)}\b", lower):
			count += 1
	length = max(len(text), 1)
	url_count = len(re.findall(r"https?://", text))
	all_caps_ratio = sum(1 for c in text if c.isupper()) / max(sum(1 for c in text if c.isalpha()), 1)

	# Heuristic scoring 0..1
	score = min(1.0, (count * 0.08) + (url_count * 0.05) + (all_caps_ratio * 0.4))
	return round(score, 3)


def optimize_sending_pattern(spam_score: float) -> Tuple[float, float]:
	# Return multipliers (send_volume_multiplier, delay_jitter_multiplier)
	if spam_score < 0.2:
		return 1.0, 1.0
	if spam_score < 0.4:
		return 0.9, 1.1
	if spam_score < 0.6:
		return 0.8, 1.25
	return 0.6, 1.5
