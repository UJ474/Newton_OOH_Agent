import logging
from typing import Any, Dict, List

from memory.embeddings import get_embedding_provider

logger = logging.getLogger(__name__)

async def search_ooh_mongodb(
    db: Any, 
    query_text: str, 
    city_filter: str = None, 
    venue_category_filter: str = None, 
    limit: int = 5
) -> List[Dict[str, Any]]:
    """
    Performs a MongoDB $vectorSearch on the unified_inventory collection.
    """
    if db is None:
        logger.error("No database connection provided for OOH search.")
        return []

    # 1. Generate embedding for the search query
    provider = get_embedding_provider(db)
    vectors = await provider.embed([query_text])
    
    if not vectors or not vectors[0]:
        logger.warning("Failed to generate embedding for search query.")
        return []
        
    query_vector = vectors[0]

    # 2. Construct the metadata filter (pre-filter)
    filter_stage = {}
    if city_filter or venue_category_filter:
        filter_conditions = []
        if city_filter:
            # Case-insensitive exact match or simple regex could be used. 
            # Atlas Vector Search requires exact match on scalar fields if using filter in $vectorSearch
            filter_conditions.append({"city": {"$eq": city_filter}})
        if venue_category_filter:
            filter_conditions.append({"venue_category": {"$eq": venue_category_filter}})
            
        if filter_conditions:
            if len(filter_conditions) > 1:
                filter_stage = {"$and": filter_conditions}
            else:
                filter_stage = filter_conditions[0]

    # 3. Construct the Atlas Vector Search pipeline
    # NOTE: You MUST create an index named 'vector_index' in Atlas on the 'embedding_vector' field.
    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index", # The name of the index in Atlas
                "path": "embedding_vector",
                "queryVector": query_vector,
                "numCandidates": 100,
                "limit": limit,
                **({"filter": filter_stage} if filter_stage else {})
            }
        },
        {
            "$project": {
                "_id": 0,
                "embedding_vector": 0, # Exclude the large vector from results
                "score": {"$meta": "vectorSearchScore"}
            }
        }
    ]

    try:
        collection = db.utkarsh_test
        cursor = collection.aggregate(pipeline)
        results = await cursor.to_list(length=limit)
        
        logger.info(f"OOH Vector Search returned {len(results)} results for query: '{query_text}'")
        return results
    except Exception as e:
        logger.error(f"Error executing OOH Vector Search: {e}")
        return []
