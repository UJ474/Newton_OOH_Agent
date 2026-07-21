import json
import logging
from typing import Any

from claude_agent_sdk import tool
# from chat.tools import _ok

from ooh_agent.retriever import search_ooh_mongodb

import os
import logging
from motor.motor_asyncio import AsyncIOMotorClient

logger = logging.getLogger(__name__)

_db_client = None
def get_db():
    global _db_client
    if _db_client is None:
        _db_client = AsyncIOMotorClient(os.environ.get("MONGODB_URI"))
    return _db_client.get_database()

def _ok(payload: dict[str, Any]) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": json.dumps(payload, default=str)}]}

@tool(
    "search_ooh_inventory",
    "Search the Out-Of-Home (OOH) media inventory database using semantic search. Use this to find screens, malls, tech parks, or audience segments.",
    {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The natural language search query (e.g., 'malls popular with foodies' or 'screens near IT offices')."
            },
            "city_filter": {
                "type": "string",
                "description": "Optional city to filter by (e.g., 'Hyderabad')."
            },
            "venue_category_filter": {
                "type": "string",
                "enum": ["mall", "tech_park", "coworking", "residential", "gym", "office", "metro"],
                "description": "Optional category of venue to filter by."
            }
        },
        "required": ["query"],
    },
)
async def search_ooh_inventory(args: dict[str, Any]) -> dict[str, Any]:
    logger.debug(f"ooh_agent.tools.search_ooh_inventory args={args}")
    
    query = str(args.get("query", "")).strip()
    city_filter = args.get("city_filter")
    venue_category_filter = args.get("venue_category_filter")
    
    if not query:
        return _ok({"status": "error", "message": "query is required"})

    try:
        db = get_db() # Uses local get_db
        results = await search_ooh_mongodb(
            db=db,
            query_text=query,
            city_filter=city_filter,
            venue_category_filter=venue_category_filter
        )
        
        if not results:
            return _ok({"status": "success", "message": "No inventory found matching those criteria.", "data": []})
            
        return _ok({
            "status": "success",
            "count": len(results),
            "data": results
        })
        
    except Exception as exc:
        logger.exception("ooh_agent.tools.search_ooh_inventory.failed")
        return _ok({"status": "error", "message": str(exc)})
