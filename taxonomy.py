"""
taxonomy.py
-----------
The project's knowledge backbone: master vocabulary + pure lookup/synonym/
expansion helpers. Every enrichment service, normalizer, and query planner
depends on this module.

No database calls. No LLM calls. Pure Python.
"""

from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════
# MASTER VOCABULARY
# ═══════════════════════════════════════════════════════════════════════════

INDUSTRIES: list[str] = [
    "Technology", "Healthcare", "Finance", "Retail", "Education",
    "Manufacturing", "Entertainment", "Automobile", "Real Estate",
    "Hospitality", "Telecommunication",
]

PROFESSIONS: list[str] = [
    "Software Engineer", "AI Engineer", "Data Scientist", "Doctor", "Lawyer",
    "Teacher", "CA", "Sales Manager", "Product Manager", "Marketing",
    "Designer", "Founder", "CXO", "Trader", "Banker",
]

INTERESTS: list[str] = [
    "Gaming", "Fitness", "Investing", "Travel", "Luxury", "Technology",
    "Food", "Shopping", "Fashion", "Sports", "Education", "Parenting",
    "Finance", "Automobiles", "Photography",
]

LIFESTYLES: list[str] = [
    "Corporate", "Premium", "Luxury", "Budget", "Student", "Urban",
    "Family", "Business", "Fitness", "Travel", "Professional",
    "Young Adult", "Affluent", "Middle Income",
]

ENVIRONMENTS: list[str] = [
    "Corporate", "Transit", "Residential", "Shopping", "Education",
    "Healthcare", "Entertainment", "Business District", "Tourist",
    "Airport", "Metro", "Tech Park", "Mall", "Gym", "Coworking",
]

ADVERTISER_CATEGORIES: list[str] = [
    "Fintech", "Insurance", "Banking", "Luxury Cars", "SUV", "Motorcycles",
    "Real Estate", "Education", "Food Delivery", "Beverages", "Coffee",
    "Fashion", "Gaming", "OTT", "Electronics", "AI SaaS", "Cybersecurity",
    "Cloud Computing", "Investment Apps", "Health Supplements",
]

VOCABULARIES: dict[str, list[str]] = {
    "industries": INDUSTRIES,
    "professions": PROFESSIONS,
    "interests": INTERESTS,
    "lifestyles": LIFESTYLES,
    "environments": ENVIRONMENTS,
    "advertiser_categories": ADVERTISER_CATEGORIES,
}

# ═══════════════════════════════════════════════════════════════════════════
# SYNONYMS  (lowercase variant → canonical term)
# ═══════════════════════════════════════════════════════════════════════════

SYNONYMS: dict[str, str] = {
    # industries
    "it": "Technology", "tech": "Technology", "fintech": "Finance",
    "banking": "Finance", "edtech": "Education", "pharma": "Healthcare",
    "medical": "Healthcare", "auto": "Automobile", "realty": "Real Estate",
    "telecom": "Telecommunication",
    # professions
    "swe": "Software Engineer", "developer": "Software Engineer",
    "programmer": "Software Engineer", "ml engineer": "AI Engineer",
    "founder/ceo": "Founder", "ceo": "CXO", "cto": "CXO", "cfo": "CXO",
    "chartered accountant": "CA",
    # interests
    "video games": "Gaming", "esports": "Gaming", "working out": "Fitness",
    "gym": "Fitness", "stocks": "Investing", "trading": "Investing",
    # lifestyle
    "high income": "Affluent", "rich": "Affluent", "wealthy": "Affluent",
    "students": "Student", "families": "Family",
    # environment / venue categories
    "residential society": "Residential", "apartment": "Residential",
    "society": "Residential", "coworking space": "Coworking",
    "co-working": "Coworking", "office space": "Coworking",
    "techpark": "Tech Park", "it park": "Tech Park",
    "shopping mall": "Mall", "cinema hall": "Entertainment",
    "movie theatre": "Entertainment", "metro station": "Metro",
    "subway": "Metro", "fitness center": "Gym", "fitness centre": "Gym",
    "airport terminal": "Airport",
    # advertiser categories
    "food delivery app": "Food Delivery", "streaming": "OTT",
    "ott platform": "OTT", "cyber security": "Cybersecurity",
    "cloud": "Cloud Computing", "investing app": "Investment Apps",
    "supplements": "Health Supplements",
}

# City canonicalization lives in normalizer.py; taxonomy only tracks the
# controlled vocabulary above (industries/professions/interests/etc).


# ═══════════════════════════════════════════════════════════════════════════
# LOOKUP / VALIDATION
# ═══════════════════════════════════════════════════════════════════════════

def _canonical_index(vocab: list[str]) -> dict[str, str]:
    return {term.lower(): term for term in vocab}


_CANONICAL_BY_VOCAB: dict[str, dict[str, str]] = {
    name: _canonical_index(terms) for name, terms in VOCABULARIES.items()
}
_ALL_CANONICAL: dict[str, str] = {}
for _idx in _CANONICAL_BY_VOCAB.values():
    _ALL_CANONICAL.update(_idx)


def is_valid_term(term: str, vocab: str | None = None) -> bool:
    """Check whether `term` (any casing) exists in a given vocab, or any vocab."""
    key = term.strip().lower()
    if vocab:
        return key in _CANONICAL_BY_VOCAB.get(vocab, {})
    return key in _ALL_CANONICAL


def canonicalize_term(term: str, vocab: str | None = None) -> str | None:
    """
    Resolve `term` to its canonical taxonomy form.
    Checks synonyms first, then exact (case-insensitive) vocab match.
    Returns None if no match is found.
    """
    key = term.strip().lower()

    if key in SYNONYMS:
        canonical = SYNONYMS[key]
        if not vocab or is_valid_term(canonical, vocab):
            return canonical

    index = _CANONICAL_BY_VOCAB.get(vocab, _ALL_CANONICAL) if vocab else _ALL_CANONICAL
    return index.get(key)


def get_synonyms(canonical_term: str) -> list[str]:
    """Reverse lookup: all known synonym phrases mapping to a canonical term."""
    return [alias for alias, term in SYNONYMS.items() if term == canonical_term]


def list_vocab(vocab: str) -> list[str]:
    return list(VOCABULARIES.get(vocab, []))


# ═══════════════════════════════════════════════════════════════════════════
# QUERY EXPANSION
# ═══════════════════════════════════════════════════════════════════════════

def expand_terms(raw_terms: list[str]) -> list[str]:
    """
    Map free-text terms to canonical taxonomy terms where possible, keeping
    unmatched terms as-is. Deduplicates while preserving order.
    """
    seen: set[str] = set()
    expanded: list[str] = []
    for term in raw_terms:
        canonical = canonicalize_term(term) or term.strip()
        if canonical and canonical.lower() not in seen:
            seen.add(canonical.lower())
            expanded.append(canonical)
    return expanded


def expand_query(query: str) -> str:
    """
    Expand a free-text search query by appending canonical terms found for
    any recognizable word/phrase, enriching it for embedding/semantic search.
    Pure string matching — no LLM.
    """
    words = [w.strip(",.") for w in query.split()]
    additions = expand_terms(words)
    extra = [t for t in additions if t.lower() not in query.lower()]
    return f"{query} {' '.join(extra)}".strip() if extra else query