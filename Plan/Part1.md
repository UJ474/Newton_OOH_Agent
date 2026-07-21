# Newton Ads AI Media Planning Platform

Version: 1.0

Author:
Utkarsh Jain

---

# 1. Vision

This project is not an inventory management system.

It is an AI-powered media planning platform for Out-of-Home (OOH) advertising.

The inventory database is only one component.

The real objective is to enable users to search inventory using natural language and receive intelligent recommendations rather than simple database results.

Example:

Instead of asking

> Show all Tech Parks in Bangalore.

Users should be able to ask

• Where can I target software engineers?
• Find premium audiences.
• Show locations suitable for fintech campaigns.
• Find high-income working professionals.
• Recommend locations for launching an electric vehicle.
• Where can I target decision makers?
• Find places where Gen Z spends time.
• Suggest inventory for luxury brands.

The system should understand intent, enrich inventory with semantic knowledge, and recommend the best locations.

---

# 2. Core Philosophy

The project is based on five principles.

## Principle 1

Raw inventory should never be modified.

Original data is preserved exactly as received.

Every semantic enhancement should be added separately.

Never overwrite source information.

---

## Principle 2

Search should be semantic.

Users should not need exact keywords.

Searching

"Tech Savvy"

should return

Google
Microsoft
Amazon
Tech Parks
Coworking Spaces

even if the phrase "Tech Savvy" never appears in the database.

---

## Principle 3

Everything should be reusable.

Every module should be usable by

• Inventory Ingestion
• Search Agent
• Recommendation Agent
• Campaign Planner
• Dashboard APIs

No duplicated logic.

---

## Principle 4

Every enrichment should be explainable.

The system should be able to explain WHY it recommended a location.

Example

"This location contains software engineers, receives
120,000 monthly visitors, and has a premium corporate
audience."

---

## Principle 5

LLMs generate intelligence.

Traditional code performs execution.

The LLM should never decide business logic.

Instead

LLM

↓

Structured JSON

↓

Validation

↓

Database

↓

Search

This makes the system deterministic.

---

# 3. High Level Architecture

                    User
                      │
                      ▼
               Search Agent
                      │
             Query Planner
                      │
         ┌────────────┴────────────┐
         ▼                         ▼
 Structured Filters          Semantic Query
         │                         │
         ▼                         ▼
 MongoDB Query             Vector Search
         │                         │
         └────────────┬────────────┘
                      ▼
            Recommendation Engine
                      │
                      ▼
                Ranked Results

Inventory ingestion follows a different path.

Excel

↓

Parser

↓

Normalizer

↓

Enrichment Pipeline

↓

Embedding Builder

↓

MongoDB

---

# 4. Overall Folder Structure

newton-ad-analysis-agent-platform/

    config/

    data/

        company_profiles/

        taxonomy/

        venue_defaults/

    enrichment/

        __init__.py

        models.py

        taxonomy.py

        normalizer.py

        cache.py

        llm_generator.py

        company_service.py

        venue_service.py

        location_service.py

        environment_service.py

        recommendation_service.py

        embedding_builder.py

        enricher.py

    memory/

        embeddings.py

        vector_search.py

    ooh_agent/

        ingest_inventory.py

        search_agent.py

        planner_agent.py

        recommendation_agent.py

    prompts/

        company_prompt.txt

        venue_prompt.txt

        query_planner.txt

    tests/

    docs/

    README.md

---

# 5. Technology Stack

Python 3.12

MongoDB Atlas

Motor

FastAPI

Pydantic v2

OpenAI

Sentence Embeddings (future optional)

Atlas Vector Search

Playwright (future)

pytest

No ORM.

MongoDB should be accessed directly through Motor.

---

# 6. MongoDB Collections

inventory

Stores enriched inventory.

company_profiles

Stores semantic company intelligence.

venue_profiles

Stores venue intelligence.

query_logs

Stores user searches.

recommendation_logs

Stores generated recommendations.

embedding_cache

Stores reusable embeddings.

taxonomy

Stores master taxonomy.

---

# 7. Inventory Lifecycle

Excel

↓

Parser

↓

InventoryRecord

↓

Normalizer

↓

Company Enrichment

↓

Venue Enrichment

↓

Environment Enrichment

↓

Recommendation Generation

↓

Embedding Text

↓

Embedding Vector

↓

MongoDB

At no stage should raw inventory fields be overwritten.

Every stage only appends information.

---

# 8. Coding Standards

Every module must have one responsibility.

Never mix parsing with enrichment.

Never mix LLM calls with MongoDB operations.

Never directly call OpenAI inside business services.

Only llm_generator.py may call an LLM.

Every service returns Pydantic models.

No dictionaries should leave service boundaries.

Every module must be independently testable.

No hidden global state.

Every enrichment function should be deterministic after validation.

---

# 9. Project Development Order

Phase 1

Foundation

✓ models.py

✓ taxonomy.py

✓ normalizer.py

---

Phase 2

Knowledge

company_service.py

venue_service.py

location_service.py

---

Phase 3

Intelligence

environment_service.py

recommendation_service.py

---

Phase 4

Embeddings

embedding_builder.py

cache.py

---

Phase 5

Pipeline

enricher.py

ingest_inventory.py

---

Phase 6

Search

query_planner.py

vector_search.py

ranking_engine.py

---

Phase 7

Agents

search_agent.py

planner_agent.py

recommendation_agent.py

---

End Goal

Natural language AI media planner capable of recommending the best OOH inventory across India.