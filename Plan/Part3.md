# PART 3 — Intelligence Pipeline & Search Architecture

---

# 10. recommendation_service.py

## Purpose

The Recommendation Service determines which types of advertisers are best suited for a location.

It does NOT recommend inventory to users.

Instead, it answers:

> "Given this location, which advertisers would benefit most from advertising here?"

It generates advertiser suitability.

---

## Inputs

InventoryRecord

CompanyProfile(s)

VenueProfile

LocationProfile

Environment Tags

---

## Outputs

recommended_ad_categories

recommended_campaign_types

confidence_score

reasoning

---

## Example

Input

Google Office
Bangalore

Audience

Software Engineers

Product Managers

AI Engineers

Corporate Professionals

↓

Output

Recommended Advertisers

AI SaaS

Cloud Services

Cybersecurity

Premium Laptops

Investment Apps

Luxury Cars

Coffee Brands

Health Insurance

Premium Credit Cards

Protein Supplements

---

Another Example

Metro Station

↓

Audience

Daily Commuters

Office Workers

Students

↓

Recommended

Food Delivery

UPI Apps

Telecom

OTT

Banking

Travel Apps

Quick Commerce

Snacks

Beverages

---

Rules

Never perform search.

Never generate embeddings.

Only infer advertiser suitability.

---

# 11. embedding_builder.py

## Purpose

Create one semantic document representing the entire inventory location.

This document becomes the vector embedding.

---

Input

InventoryRecord

Company Profiles

Venue Profile

Environment

Recommendations

---

Output

embedding_text

embedding_vector

---

IMPORTANT

Do NOT embed individual fields.

Build one complete semantic document.

---

Example

Venue Name

Google Bangalore

Category

Tech Park

Companies

Google

Microsoft

Amazon

Audience

Software Engineers

AI Engineers

Cloud Architects

Product Managers

Technology Leaders

Environment

Corporate

Innovation

Premium

Technology

Professional

Recommended Advertisers

Cloud Computing

AI SaaS

Cybersecurity

Luxury Cars

Coffee

Investment Platforms

Location

Whitefield Bangalore

Business District

High monthly footfall

Premium working professionals

---

That entire document is embedded.

Not individual fields.

---

Advantages

Searching

Tech Savvy

matches.

Searching

Developers

matches.

Searching

AI

matches.

Searching

Early Adopters

matches.

Searching

High Income Professionals

matches.

---

Responsibilities

Generate semantic text.

Clean duplicate concepts.

Maintain readability.

Generate embedding.

Store embedding.

---

No search.

No ranking.

---

# 12. enricher.py

Purpose

Central pipeline coordinator.

This is the heart of inventory ingestion.

---

Flow

InventoryRecord

↓

Normalize

↓

Company Service

↓

Venue Service

↓

Location Service

↓

Environment Service

↓

Recommendation Service

↓

Embedding Builder

↓

Return enriched record

---

Responsibilities

Call modules in order.

Merge outputs.

Validate outputs.

Handle failures.

Return final InventoryRecord.

---

The enricher should know NOTHING about Excel.

It only accepts InventoryRecord.

---

# 13. ingest_inventory.py

Purpose

Read inventory.

Nothing else.

---

Responsibilities

Read Excel.

Detect sheet.

Call parser.

Create InventoryRecord.

Pass record to enricher.

Store Mongo.

Done.

---

Flow

Excel

↓

Parser

↓

InventoryRecord

↓

Enricher

↓

MongoDB

---

Never contain business logic.

Never contain LLM prompts.

Never contain embeddings.

Never contain recommendations.

---

# 14. parser/

Purpose

Convert every inventory sheet into InventoryRecord.

Each sheet gets its own parser.

---

Recommended Structure

parser/

rwa.py

mall.py

metro.py

gym.py

airport.py

techpark.py

coworking.py

hospital.py

chaipoint.py

cinema.py

etc.

---

Every parser returns

InventoryRecord

Nothing else.

---

# SEARCH SYSTEM

This is completely separate from ingestion.

---

# 15. query_planner.py

Purpose

Understand user intent.

Convert English into structured search.

---

Example

User

Find premium locations where software engineers work in Bangalore under ₹80,000.

↓

Output

{
    city

    Bangalore

    max_budget

    80000

    professions

    Software Engineer

    lifestyle

    Premium

    semantic_query

    Software Engineers AI Developers Technology Professionals Premium Corporate Audience
}

---

Responsibilities

Extract

Cities

Budget

Audience

Industries

Venue

Environment

Advertiser Category

Media Format

Time Constraints (future)

Campaign Goals

Generate semantic query.

---

No search.

Only planning.

---

# 16. vector_search.py

Purpose

Semantic retrieval.

---

Input

Embedding

↓

Atlas Vector Search

↓

Top K

---

Returns

Candidate Inventory

Similarity Score

Nothing else.

---

No ranking.

---

# 17. filter_engine.py

Purpose

Apply structured filters.

---

Filters

City

Budget

Media Type

Footfall

Venue Category

Audience

Screen Type

Availability (future)

---

No embeddings.

---

# 18. ranking_engine.py

Purpose

Combine everything into one final score.

---

Inputs

Vector Score

Audience Match

Industry Match

Budget Match

Footfall

Commercial Score

Campaign Match

Environment Match

---

Output

Ranked Inventory

---

Example Formula

Final Score

=

40%

Vector Similarity

+

20%

Audience Match

+

15%

Industry Match

+

10%

Commercial Fit

+

10%

Budget Fit

+

5%

Business Rules

---

Ranking should be configurable.

Never hardcode weights.

---

# 19. recommendation_agent.py

Purpose

Generate the final response.

---

Input

Ranked Inventory

↓

LLM

↓

Natural Language Report

---

Example

Instead of

20 inventory rows

Generate

"The best locations for your fintech campaign are..."

Explain

Why selected

Expected audience

Tradeoffs

Estimated reach

Strengths

---

The LLM never searches.

It only summarizes ranked results.

---

# COMPLETE SEARCH FLOW

User

↓

Query Planner

↓

Semantic Query

↓

Embedding

↓

Vector Search

↓

Candidate Results

↓

Filter Engine

↓

Ranking Engine

↓

Top Inventory

↓

Recommendation Agent

↓

Natural Language Response

---

# COMPLETE INGESTION FLOW

Excel

↓

Parser

↓

InventoryRecord

↓

Normalizer

↓

Company Service

↓

Venue Service

↓

Location Service

↓

Environment Service

↓

Recommendation Service

↓

Embedding Builder

↓

MongoDB

---

# DESIGN PRINCIPLES

Every module has exactly one responsibility.

Every module should be independently testable.

No circular dependencies.

No module directly calls another module unless required by the pipeline.

No LLM calls outside llm_generator.py.

No parser contains enrichment logic.

No enrichment module knows Excel exists.

Search and ingestion are completely independent systems.

Every service returns Pydantic models.

Every database write happens only after validation.

Every expensive operation should be cached.

Every semantic decision should be explainable.