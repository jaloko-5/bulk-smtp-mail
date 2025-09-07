from __future__ import annotations
from dataclasses import dataclass
from random import random, choice
from typing import Dict, Any


@dataclass
class PersonalizationResult:
	personalized_subject: str
	personalized_body: str
	score: float


def _interpolate(template: str, fields: Dict[str, Any]) -> str:
	text = template
	for key, value in fields.items():
		text = text.replace(f"{{{{{key}}}}}", str(value) if value is not None else "")
	return text


def generate_variation(subject_template: str, body_template: str, fields: Dict[str, Any]) -> PersonalizationResult:
	variants = ["Hi", "Hello", "Hey", "Greetings"]
	greetings = choice(variants)
	augmented_fields = {**fields, "greeting": greetings}

	personalized_subject = _interpolate(subject_template, augmented_fields)
	personalized_body = _interpolate(body_template, augmented_fields)

	# Simple scoring: completeness of key fields + small randomness
	required = ["name", "role", "company", "industry"]
	filled = sum(1 for k in required if augmented_fields.get(k))
	score = min(1.0, 0.15 * filled + 0.1 + random() * 0.15)
	return PersonalizationResult(personalized_subject, personalized_body, round(score, 3))
