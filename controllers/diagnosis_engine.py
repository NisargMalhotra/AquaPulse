"""
AquaPulse – Fish Disease Diagnosis Engine
==========================================
A rule-based expert system that matches free-text symptom descriptions
against the disease knowledge base and returns ranked diagnoses with
species-aware treatment recommendations.

Scoring algorithm
-----------------
1.  **Exact phrase match** – each keyword phrase found in the user input
    scores ``len(phrase.split())`` points (longer phrases = higher signal).
2.  **Individual word match** – each *unique, meaningful* word from the
    keyword list found in the input scores 0.5 points (lower weight to
    avoid false positives on common words).
3.  **Species boost** – if the selected fish species has a dedicated note
    for the disease, the total score is multiplied by 1.25.
4.  Results are normalised against the best match and sorted descending.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from utils.fish_data import DISEASE_DATABASE, FISH_PROFILES


# ── Stop-words to ignore during individual-word matching ─────────────────────
_STOP_WORDS = frozenset({
    "my", "the", "a", "an", "is", "are", "was", "were", "has", "have",
    "had", "be", "been", "being", "do", "does", "did", "will", "would",
    "shall", "should", "may", "might", "can", "could", "i", "me", "he",
    "she", "it", "we", "they", "you", "his", "her", "its", "our",
    "their", "this", "that", "these", "those", "and", "but", "or", "if",
    "in", "on", "at", "to", "for", "of", "with", "from", "by", "as",
    "into", "about", "very", "just", "also", "like", "so", "than",
    "too", "some", "any", "no", "not", "all", "each", "every",
    "fish", "tank", "aquarium", "water",  # domain stop-words
})


@dataclass
class MedicationInfo:
    """Single medication recommendation."""
    name: str
    dosage: str
    notes: str


@dataclass
class DiagnosisResult:
    """A single diagnosis match with treatments and confidence."""
    disease_id: str
    disease_name: str
    emoji: str
    severity: str
    confidence: str            # "Strong Match", "Good Match", "Possible Match"
    confidence_score: float    # 0.0 – 1.0 (internal)
    matched_keywords: List[str]
    description: str
    causes: List[str]
    treatment_steps: List[str]
    medications: List[MedicationInfo]
    species_advice: str        # species-specific note (or "")
    prevention: List[str]


class DiagnosisEngine:
    """Rule-based fish-disease diagnosis engine."""

    # ─── Public API ──────────────────────────────────────────────────────

    @classmethod
    def diagnose(
        cls,
        user_input: str,
        fish_species: str = "betta",
        max_results: int = 3,
    ) -> List[DiagnosisResult]:
        """
        Analyse free-text symptom description and return ranked diagnoses.

        Args:
            user_input:   Natural-language description of the problem.
            fish_species: Key from ``FISH_PROFILES`` (e.g. ``"betta"``).
            max_results:  Maximum number of diagnoses to return.

        Returns:
            Up to *max_results* :class:`DiagnosisResult` objects,
            sorted by descending confidence.
        """
        if not user_input or not user_input.strip():
            return []

        normalised = cls._normalise(user_input)
        scored: List[tuple[str, float, List[str]]] = []

        for disease_id, disease in DISEASE_DATABASE.items():
            score, matched = cls._score_disease(
                normalised, disease, fish_species,
            )
            if score > 0:
                scored.append((disease_id, score, matched))

        if not scored:
            return []

        # Normalise scores relative to the best match
        best = max(s[1] for s in scored)
        scored.sort(key=lambda s: s[1], reverse=True)

        results: List[DiagnosisResult] = []
        for disease_id, raw_score, matched in scored[:max_results]:
            disease = DISEASE_DATABASE[disease_id]
            norm_score = raw_score / best if best > 0 else 0

            # Confidence label
            if norm_score >= 0.7:
                confidence = "Strong Match"
            elif norm_score >= 0.4:
                confidence = "Good Match"
            else:
                confidence = "Possible Match"

            # Species-specific advice
            species_advice = disease.get("species_notes", {}).get(
                fish_species, ""
            )

            # Medications
            meds = [
                MedicationInfo(
                    name=m["name"],
                    dosage=m["dosage"],
                    notes=m["notes"],
                )
                for m in disease.get("medications", [])
            ]

            results.append(
                DiagnosisResult(
                    disease_id=disease_id,
                    disease_name=disease["name"],
                    emoji=disease.get("emoji", "🩺"),
                    severity=disease.get("severity", "Unknown"),
                    confidence=confidence,
                    confidence_score=round(norm_score, 2),
                    matched_keywords=matched,
                    description=disease["description"],
                    causes=disease.get("causes", []),
                    treatment_steps=disease.get("treatment_steps", []),
                    medications=meds,
                    species_advice=species_advice,
                    prevention=disease.get("prevention", []),
                )
            )

        return results

    # ─── Scoring Internals ───────────────────────────────────────────────

    @classmethod
    def _score_disease(
        cls,
        normalised_input: str,
        disease: Dict,
        fish_species: str,
    ) -> tuple[float, List[str]]:
        """Return (score, matched_keywords) for one disease."""
        keywords: List[str] = disease.get("keywords", [])
        score = 0.0
        matched: List[str] = []

        # ── Exact phrase matching (high weight) ──────────────────────
        for phrase in keywords:
            if phrase in normalised_input:
                score += len(phrase.split())  # multi-word → higher score
                matched.append(phrase)

        # ── Individual word matching (lower weight) ──────────────────
        input_words = set(normalised_input.split()) - _STOP_WORDS
        keyword_words: set[str] = set()
        for phrase in keywords:
            for w in phrase.split():
                if w not in _STOP_WORDS and len(w) > 2:
                    keyword_words.add(w)

        word_hits = input_words & keyword_words
        score += len(word_hits) * 0.5

        # ── Species boost ────────────────────────────────────────────
        if (
            score > 0
            and fish_species in disease.get("species_notes", {})
        ):
            score *= 1.25

        return score, matched

    @staticmethod
    def _normalise(text: str) -> str:
        """Lowercase, strip, and collapse whitespace."""
        import re
        text = text.lower().strip()
        text = re.sub(r"[^\w\s]", " ", text)  # remove punctuation
        text = re.sub(r"\s+", " ", text)       # collapse whitespace
        return text

    # ─── Utility ─────────────────────────────────────────────────────────

    @staticmethod
    def get_species_name(species_key: str) -> str:
        """Return the human-readable species name."""
        profile = FISH_PROFILES.get(species_key)
        return profile["name"] if profile else species_key.replace("_", " ").title()
