# PART 5 — Production Architecture & Engineering Standards

---

# 31. Overall Philosophy

This project should be treated as an AI Platform, not as a Python project.

Everything should be replaceable.

Everything should be versioned.

Everything should be observable.

Everything should be testable.

Every module should be independently deployable in the future.

---

# 32. Domain-Driven Design

Instead of organizing by file type, organize mentally by domains.

Inventory Domain

Company Domain

Venue Domain

Location Domain

Audience Domain

Campaign Domain

Recommendation Domain

Knowledge Domain

Search Domain

Embedding Domain

The codebase should reflect business concepts rather than technical implementation.

---

# 33. Data Ownership

Every module owns only one type of data.

Inventory Service

Owns InventoryRecord

Company Service

Owns CompanyProfile

Venue Service

Owns VenueProfile

Location Service

Owns LocationProfile

Embedding Builder

Owns embedding_text

Query Planner

Owns QueryIntent

Ranking Engine

Owns SearchScore

No module should edit another module's owned fields directly.

---

# 34. Knowledge Provider Architecture

Instead of tightly coupling services together, every knowledge source should implement a common interface.

Example

KnowledgeProvider

↓

CompanyProvider

VenueProvider

LocationProvider

AudienceProvider

CampaignProvider

POIProvider

TrafficProvider

WeatherProvider

DemographicsProvider

Every provider returns structured knowledge.

The pipeline merges knowledge from all providers.

---

# Provider Interface

Input

InventoryRecord

Output

KnowledgeContribution

Each provider only contributes the fields it owns.

It should never overwrite existing knowledge.

---

# Example

CompanyProvider

Returns

industry_tags

profession_tags

income_tags

audience_tags

VenueProvider

Returns

environment_tags

peak_hours

visit_duration

LocationProvider

Returns

business_district

micro_market

nearby_landmarks

nearby_companies

The pipeline merges all of them.

---

# 35. Pipeline Architecture

The enrichment pipeline should be configurable.

Instead of

Company

↓

Venue

↓

Location

↓

Environment

↓

Recommendation

Hardcoded

The pipeline should read configuration.

Example

pipeline.yaml

CompanyProvider

VenueProvider

LocationProvider

EnvironmentProvider

RecommendationProvider

EmbeddingProvider

Then changing the pipeline requires configuration only.

---

# 36. Configuration

All configuration should live outside the code.

Environment Variables

API Keys

Mongo URI

Embedding Model

LLM Model

Temperature

Timeouts

Retry Counts

Batch Size

Cache TTL

Pipeline Order

Nothing should be hardcoded.

---

# 37. Prompt Management

Never place prompts inside Python files.

Recommended

prompts/

company_profile.md

venue_profile.md

location_profile.md

campaign_profile.md

query_planner.md

recommendation.md

Prompts become versioned assets.

---

# 38. Prompt Versioning

Every generated object should store

generator_version

prompt_version

model_name

generation_timestamp

This allows regeneration later.

Example

Company Profile

Generated

Prompt v3

GPT-5.5

2026-07-20

Later

Prompt v4

↓

Regenerate only outdated profiles.

---

# 39. Validation Layer

Never trust LLM output.

Every response must pass

JSON validation

↓

Schema validation

↓

Taxonomy validation

↓

Business validation

↓

Database

If validation fails

Retry

or

Fallback

Never store invalid data.

---

# 40. Observability

Every important action should be logged.

Examples

Company generated

Venue generated

Embedding created

Mongo updated

Search executed

Recommendation produced

LLM latency

Embedding latency

Cache hit

Cache miss

This is essential for debugging production systems.

---

# 41. Error Strategy

Never fail the entire ingestion.

If

Company generation fails

↓

Continue

If

Location intelligence fails

↓

Continue

If

Recommendation generation fails

↓

Continue

Only embedding creation should block insertion if embeddings are required.

Partial enrichment is better than no enrichment.

---

# 42. Retry Strategy

LLM Failure

↓

Retry

JSON Parse Failure

↓

Retry

Timeout

↓

Retry

Validation Failure

↓

Regenerate

Maximum retries should be configurable.

---

# 43. Idempotency

Running ingestion twice should never duplicate records.

Every inventory item should have a stable unique identifier.

Upserts should replace the same logical record rather than creating duplicates.

---

# 44. Batch Processing

Never call the LLM for every row without batching or caching.

Preferred flow

Normalize

↓

Collect unique companies

↓

Generate missing company profiles

↓

Cache

↓

Reuse

The same applies to

Venue types

Cities

Business districts

Landmarks

---

# 45. Performance Goals

Target

100,000 inventory records

without architectural changes.

Requirements

Concurrent enrichment

Batch embeddings

Bulk Mongo writes

Connection pooling

Async throughout

---

# 46. Testing Strategy

Unit Tests

Every module independently.

Integration Tests

Entire enrichment pipeline.

Golden Tests

Known input should always produce expected output.

Regression Tests

Prompt changes should not break previous behaviour.

Performance Tests

Large inventory datasets.

---

# 47. Security

Never log

API keys

Mongo URI

User credentials

Never expose

Internal prompts

Internal embeddings

Raw LLM responses

Sanitize user input before prompts.

---

# 48. Future Knowledge Sources

Demographics

Traffic Density

Weather

Crime Rate

Festivals

Sporting Events

Election Schedule

College Calendar

Corporate Events

Public Holidays

Metro Timings

Airport Passenger Volume

Ride-sharing Density

EV Charging Locations

Parking Availability

These should be added as providers, not by modifying existing modules.

---

# 49. Future AI Features

Campaign Budget Optimization

Coverage Optimization

Frequency Optimization

Route Planning

Audience Overlap Detection

Inventory Deduplication

Competitor Analysis

Creative Recommendation

Campaign Forecasting

Media Mix Optimization

ROI Prediction

All should consume the same knowledge graph.

---

# 50. Final System Vision

This platform should eventually answer questions such as

"I have ₹50 lakh.
Launch an AI coding platform.
Target software engineers in Bengaluru and Hyderabad.
Avoid audience overlap.
Maximize unique reach.
Recommend inventory with explanations."

The system should

Understand intent

↓

Plan the campaign

↓

Retrieve relevant inventory

↓

Rank inventory

↓

Estimate reach

↓

Explain recommendations

↓

Generate a media plan

The user should never need to know where the data came from.

The platform should feel like an experienced media planner rather than a database search engine.

---

# Core Engineering Principles

- Raw data is immutable.
- Knowledge is additive.
- Every module has one responsibility.
- Every expensive operation is cached.
- LLMs generate structured knowledge, not business logic.
- All outputs are validated.
- Search is hybrid (structured + semantic).
- Recommendations are explainable.
- The architecture is provider-based and extensible.
- The end product is an AI Media Planner, not a vector search application.




Now that we’ve completed the architecture, here’s what I would change before writing any more code

Looking back over the entire design, there are three architectural improvements I’d make.

1. Introduce an Orchestrator

Instead of enricher.py directly calling providers, create a central PipelineOrchestrator:

InventoryRecord
        │
        ▼
Pipeline Orchestrator
        │
 ┌──────┼──────┐
 ▼      ▼      ▼
Company Venue Location

The orchestrator manages execution order, dependencies, retries, parallelism, and error handling.




2. Introduce a Knowledge Graph (logical, not necessarily Neo4j)

Rather than treating company, venue, and location as isolated objects, think of them as connected entities:


Google
   │ employs
   ▼
Software Engineers
   │ frequent
   ▼
Tech Parks
   │ located in
   ▼
Whitefield


Even if stored in MongoDB, designing around relationships will make recommendations much richer.


3. Separate “Knowledge Generation” from “Knowledge Storage”

Instead of providers writing directly to MongoDB:


Provider
   │
   ▼
Knowledge Object
   │
   ▼
Validator
   │
   ▼
Repository
   │
   ▼
MongoDB



This makes storage replaceable (MongoDB today, another database tomorrow) and keeps providers focused on generating knowledge rather than persistence.