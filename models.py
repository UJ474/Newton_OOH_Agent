"""
models.py
---------
Single source of truth for every object used across the system.
No business logic here — validation and structure only.

Rules (Part 2):
- Pydantic v2 only, never dataclasses.
- Every service returns these models, never raw dicts.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class _Base(BaseModel):
    model_config = ConfigDict(extra="ignore", validate_assignment=True)


# ═══════════════════════════════════════════════════════════════════════════
# 1. INVENTORY
# ═══════════════════════════════════════════════════════════════════════════

class VenueCategory(str, Enum):
    RESIDENTIAL = "residential"
    COWORKING = "coworking"
    TECH_PARK = "tech_park"
    MALL = "mall"
    CINEMA = "cinema"
    METRO = "metro"
    GYM = "gym"
    OFFICE_MEDIA = "office_media"


class InventoryRecord(_Base):
    """One physical OOH screen/site — the canonical unit of inventory."""

    media_site_id: str | None = None
    venue_name: str | None = None
    venue_category: VenueCategory | str | None = None

    city: str | None = None
    zone: str | None = None
    locality: str | None = None
    address: str | None = None
    pin_code: str | None = None
    latitude: float | None = None
    longitude: float | None = None

    no_of_screens: int | None = None
    screen_size: str | None = None
    screen_type: str | None = None
    pixel_ratio: str | None = None
    dimensions: str | None = None

    monthly_footfall: int | None = None
    monthly_impressions: int | None = None

    audience_tags: list[str] = Field(default_factory=list)
    environment_tags: list[str] = Field(default_factory=list)
    screen_placement_raw: str | None = None

    cost_per_month: float | None = None
    slot_and_loop: str | None = None
    media_formats: list[str] = Field(default_factory=list)
    creative_formats: list[str] = Field(default_factory=list)

    # sheet-specific extras
    no_of_households: int | None = None
    no_of_employees: int | None = None
    facility_type: str | None = None
    employee_strength: int | None = None
    real_estate_allowed: str | None = None
    client_name: str | None = None

    source_dataset: str | None = None
    embedding_vector: list[float] | None = None


# ═══════════════════════════════════════════════════════════════════════════
# 2. KNOWLEDGE-LAYER PROFILES
# ═══════════════════════════════════════════════════════════════════════════

class CompanyProfile(_Base):
    company_name: str
    normalized_name: str
    industry: str | None = None
    professions: list[str] = Field(default_factory=list)
    income_level: str | None = None
    audience: list[str] = Field(default_factory=list)
    interests: list[str] = Field(default_factory=list)
    lifestyle: list[str] = Field(default_factory=list)
    advertiser_suitability: list[str] = Field(default_factory=list)
    decision_makers: list[str] = Field(default_factory=list)
    technology_level: str | None = None
    description: str | None = None
    confidence: float = 0.0
    reasoning: str | None = None
    source: str = "llm"
    generated_at: datetime = Field(default_factory=datetime.utcnow)


class VenueProfile(_Base):
    venue_category: str
    audience: list[str] = Field(default_factory=list)
    environment: list[str] = Field(default_factory=list)
    lifestyle: list[str] = Field(default_factory=list)
    interests: list[str] = Field(default_factory=list)
    recommended_advertisers: list[str] = Field(default_factory=list)
    traffic_pattern: str | None = None
    peak_hours: list[str] = Field(default_factory=list)
    visit_duration: str | None = None
    purchase_intent: str | None = None
    confidence: float = 0.0
    reasoning: str | None = None
    source: str = "llm"
    generated_at: datetime = Field(default_factory=datetime.utcnow)


class LocationProfile(_Base):
    city: str
    locality: str | None = None
    business_district: str | None = None
    micro_market: str | None = None
    nearby_companies: list[str] = Field(default_factory=list)
    nearby_landmarks: list[str] = Field(default_factory=list)
    nearby_attractions: list[str] = Field(default_factory=list)
    nearby_transport: list[str] = Field(default_factory=list)
    commercial_importance: str | None = None
    walkability: str | None = None
    accessibility: str | None = None
    confidence: float = 0.0
    reasoning: str | None = None
    source: str = "llm"
    generated_at: datetime = Field(default_factory=datetime.utcnow)


class EnvironmentTags(_Base):
    """Output of environment_service — venue + company + location combined."""

    tags: list[str] = Field(default_factory=list)


# ═══════════════════════════════════════════════════════════════════════════
# 3. QUERY / SEARCH
# ═══════════════════════════════════════════════════════════════════════════

class QueryIntent(_Base):
    raw_query: str
    expanded_query: str | None = None
    city_filter: str | None = None
    venue_category_filter: str | None = None
    audience_filters: list[str] = Field(default_factory=list)
    interest_filters: list[str] = Field(default_factory=list)
    budget_max: float | None = None
    confidence: float = 0.0


class SearchResult(_Base):
    """One ranked inventory hit returned to the caller."""

    record: InventoryRecord
    vector_score: float
    rank_score: float | None = None
    explanation: str | None = None


class RecommendationResult(_Base):
    query_intent: QueryIntent
    results: list[SearchResult] = Field(default_factory=list)
    summary: str | None = None