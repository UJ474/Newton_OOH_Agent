Yes. After thinking about the entire project, there are quite a few things I’d tell you before you write a single additional line of code. Most of these are lessons learned from building large AI systems rather than traditional software.

These are not required for version 1, but they will save you from having to rewrite the project later.

⸻

1. Don’t think of this as a RAG project

This is probably the biggest mindset change.

Most people build:

User
↓
Embedding
↓
Vector Search
↓
LLM

Your project should instead be:

Knowledge
↓
Reasoning
↓
Planning
↓
Search
↓
Ranking
↓
Recommendation

The vector database is only one component.

⸻

2. Build a Knowledge Graph, even if you never use Neo4j

Your data already has relationships.

Google
↓
Technology
↓
Software Engineers
↓
Tech Park
↓
Whitefield
↓
Bangalore

Or

Metro
↓
Commuters
↓
Working Professionals
↓
UPI
↓
Fintech

Don’t think in rows.

Think in relationships.

Even if everything stays in MongoDB.

⸻

3. Every AI-generated object should have metadata

Instead of

{
    "industry": ["Technology"]
}

store

{
    "industry": ["Technology"],
    "generated_by": "gpt-5.5",
    "prompt_version": 3,
    "generator_version": 2,
    "confidence": 0.94,
    "generated_at": "...",
    "validated": true
}

Six months later you’ll thank yourself.

⸻

4. Don’t make embeddings your source of truth

This is the biggest mistake I see.

Wrong

Embedding
↓
Search
↓
Done

Correct

Knowledge
↓
Embedding
↓
Search
↓
Knowledge
↓
Ranking

Embeddings help retrieval.

They should never replace knowledge.

⸻

5. Don’t overuse the LLM

Your first instinct will be

“Let’s ask GPT.”

Instead ask

“Can deterministic code solve this?”

Example

Google Pvt Ltd
↓
Google

That’s normalization.

Don’t ask GPT.

Example

Tech Park
↓
Corporate

This can be deterministic.

⸻

Only use the LLM where you genuinely need inference.

⸻

6. Version absolutely everything

Prompt

Embedding model

Taxonomy

Company profile

Venue profile

Recommendation logic

Ranking weights

Everything.

Otherwise you’ll never know why results changed.

⸻

7. Search should become a planner

Imagine this query

I have ₹1 crore. Launch a premium electric SUV in Bangalore.

Don’t search.

Plan.

The system should think

Campaign Type
↓
Luxury
↓
Income
↓
Working Professionals
↓
Technology Audience
↓
Premium Malls
↓
Tech Parks
↓
Airport
↓
Rank

That’s planning.

⸻

8. Think in entities, not tables

Instead of

inventory

think

Venue
Company
Audience
Campaign
Location
Industry
Brand
Media Format

Those are your real objects.

⸻

9. Explainability is more important than accuracy

If the AI says

Similarity 0.93

No marketer cares.

Instead say

Chosen because
• 180k monthly professionals
• Strong fintech audience
• Technology-heavy workforce
• Premium spending behaviour
• Fits budget

Trust matters more than cosine similarity.

⸻

10. Your biggest asset will become the company database

Today you have

500 companies

Later you’ll have

5000 companies

That database will become incredibly valuable.

You’ll never regenerate Google again.

You’ll simply reuse it.

⸻

11. Your taxonomy will become your moat

Most competitors rely only on embeddings.

You’ll have

Industry
↓
Profession
↓
Interest
↓
Lifestyle
↓
Advertiser Category
↓
Campaign
↓
Audience

That hierarchy will make your recommendations much better.

⸻

12. Think about confidence everywhere

Instead of

Audience
Software Engineers

store

Audience
Software Engineers
Confidence
0.82

Some knowledge is inferred.

Represent that uncertainty.

⸻

13. Add provenance

Every enriched field should answer

Where did this come from?

Example:

{
  "audience_tags": {
    "value": ["Software Engineers"],
    "source": "company_profile",
    "confidence": 0.96
  }
}

Later you can trace why something was added.

⸻

14. Separate facts from inferences

For example:

Facts:

Venue: Google Office
City: Bangalore
Footfall: 45,000

Inferences:

High Income
Technology Audience
Premium
AI Professionals

Never mix them.

⸻

15. Build an evaluation framework from day one

Eventually you’ll ask

“Is GPT-6 better than GPT-5.5?”

You need a way to answer that.

Create benchmark queries such as:

* “Find locations for fintech.”
* “Target software engineers.”
* “Reach affluent families.”

Save the expected outputs and compare new versions.

⸻

16. Every recommendation should answer five questions

Instead of only returning inventory:

What?
Why?
Who?
Trade-offs?
Alternatives?

Example:

Recommended:
Embassy Tech Village
Why?
Highest concentration of software engineers.
Who?
Premium corporate professionals.
Trade-off?
Higher cost than comparable locations.
Alternative?
Manyata Tech Park offers slightly lower audience quality but 25% lower cost.

⸻

17. Build for multiple data sources

Right now:

Excel

Tomorrow:

Excel
CSV
API
Google Sheets
Partner Feed
Web Scraping

Design ingestion so the source doesn’t matter.

⸻

18. Think of the final product

Don’t picture a MongoDB collection.

Picture a conversation like this:

User: I have ₹35 lakh. I want to promote an AI-powered coding platform in Bengaluru and Hyderabad.

AI: Based on your budget and audience, I recommend 42 digital screens across 18 locations. These locations have a high concentration of software engineers, AI professionals, and technology decision-makers. The recommended mix balances premium office environments with high-reach transit locations, maximizing exposure while keeping audience overlap low. Estimated monthly reach is approximately 1.8 million relevant impressions.

If your architecture can support that experience, you’re building the right system.

⸻

Finally, the one thing I would add that we haven’t discussed

I would introduce a Simulation Engine.

Before recommending inventory, the system should be able to simulate outcomes.

Example:

Campaign
↓
Selected Inventory
↓
Audience Overlap
↓
Estimated Reach
↓
Budget Utilization
↓
Frequency
↓
Coverage
↓
Predicted Performance

That would let a planner compare multiple strategies:

* Strategy A: Premium tech parks only.
* Strategy B: Tech parks + metro stations.
* Strategy C: Tech parks + malls.

The AI could then explain the trade-offs in reach, cost, and audience quality. That moves the platform beyond retrieval into decision support, which is where the greatest long-term value lies.