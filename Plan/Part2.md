# PART 2 — Module Specifications

This document defines the responsibility of every module in the project.

Every module must have exactly one responsibility.

No module should perform work belonging to another module.

---

# 1. models.py

## Purpose

This module defines every object used throughout the system.

It is the single source of truth for data structures.

No business logic should exist in this module.

---

## Responsibilities

- Define InventoryRecord
- Define CompanyProfile
- Define VenueProfile
- Define LocationProfile
- Define QueryIntent
- Define RecommendationResult (future)
- Define SearchResult (future)

---

## Rules

Use Pydantic v2.

Never use dataclasses.

Every service should return Pydantic models.

Never return dictionaries.

---

## Used By

Parser

Enrichment Pipeline

Search

Recommendation Engine

API

Tests

---

# 2. taxonomy.py

## Purpose

The taxonomy is the project's knowledge backbone.

Every enrichment service uses it.

Every search query expands using it.

Every company profile is normalized using it.

---

## Responsibilities

Maintain the master vocabulary.

Example

Industries

Technology

Healthcare

Finance

Retail

Education

Manufacturing

Entertainment

Automobile

Real Estate

Hospitality

Telecommunication

etc.

---

Professions

Software Engineer

AI Engineer

Data Scientist

Doctor

Lawyer

Teacher

CA

Sales Manager

Product Manager

Marketing

Designer

Founder

CXO

Trader

Banker

etc.

---

Interests

Gaming

Fitness

Investing

Travel

Luxury

Technology

Food

Shopping

Fashion

Sports

Education

Parenting

Finance

Automobiles

Photography

etc.

---

Lifestyle

Corporate

Premium

Luxury

Budget

Student

Urban

Family

Business

Fitness

Travel

Professional

Young Adult

Affluent

Middle Income

etc.

---

Environment

Corporate

Transit

Residential

Shopping

Education

Healthcare

Entertainment

Business District

Tourist

Airport

Metro

Tech Park

Mall

Gym

Coworking

etc.

---

Advertiser Categories

Fintech

Insurance

Banking

Luxury Cars

SUV

Motorcycles

Real Estate

Education

Food Delivery

Beverages

Coffee

Fashion

Gaming

OTT

Electronics

AI SaaS

Cybersecurity

Cloud Computing

Investment Apps

Health Supplements

etc.

---

Responsibilities

Provide

validation

lookup

synonyms

query expansion

normalization

No database calls.

---

Used By

Every enrichment module.

---

# 3. normalizer.py

## Purpose

Convert inconsistent data into canonical values.

The entire project depends on normalization.

---

Examples

GOOGLE INDIA

↓

Google

---

Google Pvt Ltd

↓

Google

---

Alphabet Inc

↓

Google

---

Infosys Ltd

↓

Infosys

---

BENGALURU

↓

Bangalore

---

Bengaluru Urban

↓

Bangalore

---

Responsibilities

Normalize

Company names

Cities

Venue Categories

Screen Types

Media Formats

Industries

Tags

Remove duplicates.

Trim whitespace.

Fix capitalization.

Handle abbreviations.

---

No LLM.

No database.

Pure Python.

---

Used By

Everything.

---

# 4. cache.py

## Purpose

Avoid repeated expensive work.

---

Responsibilities

Cache

Company Profiles

Venue Profiles

Embeddings

LLM Responses

Taxonomy

Future Geo Results

---

Supported Cache Layers

Memory Cache

↓

Mongo Cache

↓

LLM

---

Flow

Request

↓

Memory

↓

Mongo

↓

Generate

↓

Save

↓

Return

---

No business logic.

Only caching.

---

# 5. llm_generator.py

Purpose

The ONLY module allowed to call OpenAI.

No other module may directly call an LLM.

---

Responsibilities

Generate

Company Profile

Venue Profile

Location Intelligence

Audience Intelligence

Recommendations

Query Expansion

Structured JSON only.

Never free-form text.

---

Every prompt must request

strict JSON

confidence score

reasoning

source assumptions

---

Returned JSON must be validated before use.

---

No MongoDB.

No embedding.

No search.

No parser.

---

# 6. company_service.py

Purpose

Generate semantic understanding of companies.

---

Input

Google

Output

CompanyProfile

---

Responsibilities

Normalize company name.

Check memory cache.

Check Mongo cache.

If profile missing

↓

Ask LLM

↓

Validate JSON

↓

Store Mongo

↓

Return CompanyProfile

---

Should understand

Industry

Professions

Income

Audience

Interests

Lifestyle

Advertiser Suitability

Decision Makers

Technology Level

Company Description

---

Never call embedding builder.

Never call search.

Never access inventory.

---

# 7. venue_service.py

Purpose

Generate intelligence about venue types.

Example

Mall

Tech Park

Metro

Airport

Hospital

Gym

Cafe

Cinema

RWA

Coworking

---

Input

Venue Category

Output

VenueProfile

---

Responsibilities

Predict

Audience

Environment

Lifestyle

Interests

Recommended Advertisers

Traffic Pattern

Peak Hours

Visit Duration

Purchase Intent

---

Example

Tech Park

↓

Software Engineers

Corporate

High Income

Technology

Weekday Heavy

Morning Peak

Evening Peak

Suitable for SaaS

Fintech

Coffee

EV

Premium Phones

---

No company intelligence.

No embeddings.

---

# 8. location_service.py

Purpose

Understand geographical context.

---

Input

Address

Coordinates

City

Output

LocationProfile

---

Responsibilities

Business District

Micro Market

Nearby Companies

Nearby Landmarks

Nearby Attractions

Nearby Transport

Commercial Importance

Walkability (future)

Accessibility (future)

---

No recommendations.

Only location intelligence.

---

# 9. environment_service.py

Purpose

Combine

Venue

Company

Location

↓

Environment Tags

---

Example

Google Office

Tech Park

Bangalore

↓

Corporate

Premium

Technology

Professional

Young Workforce

Innovation Hub

---

Produces

environment_tags

Only.