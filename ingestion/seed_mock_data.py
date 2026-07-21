import asyncio
import logging
import os
import certifi
from motor.motor_asyncio import AsyncIOMotorClient

# Sample mock data based on the unified_inventory schema
MOCK_INVENTORY_DATA = [
    {
        "venue_name": "Inorbit Mall Hyderabad",
        "city": "Hyderabad",
        "locality": "Madhapur",
        "venue_category": "mall",
        "audience_tags": ["shoppers", "tech_workers", "high_income"],
        "environment_tags": ["indoor", "premium", "ac"],
        "screen_placement_raw": "Main Atrium facing escalators",
        "total_screens": 4,
        "daily_footfall": 45000,
        "reach_estimate": 120000,
        "dimensions": "10x15 ft"
    },
    {
        "venue_name": "DLF Cyber City Tech Park",
        "city": "Hyderabad",
        "locality": "Gachibowli",
        "venue_category": "tech_park",
        "audience_tags": ["it_professionals", "millennials", "corporate"],
        "environment_tags": ["outdoor", "corporate", "food_court"],
        "screen_placement_raw": "Food court entrance",
        "total_screens": 2,
        "daily_footfall": 25000,
        "reach_estimate": 60000,
        "dimensions": "8x12 ft"
    },
    {
        "venue_name": "Gold's Gym Jubilee Hills",
        "city": "Hyderabad",
        "locality": "Jubilee Hills",
        "venue_category": "gym",
        "audience_tags": ["fitness_enthusiasts", "health_conscious", "hni"],
        "environment_tags": ["indoor", "fitness", "ac"],
        "screen_placement_raw": "Cardio section wall",
        "total_screens": 3,
        "daily_footfall": 1200,
        "reach_estimate": 3000,
        "dimensions": "55 inch TV"
    },
    {
        "venue_name": "WeWork Koramangala",
        "city": "Bangalore",
        "locality": "Koramangala",
        "venue_category": "coworking",
        "audience_tags": ["startups", "freelancers", "tech_workers"],
        "environment_tags": ["indoor", "office", "cafeteria"],
        "screen_placement_raw": "Community bar area",
        "total_screens": 2,
        "daily_footfall": 800,
        "reach_estimate": 2500,
        "dimensions": "65 inch TV"
    }
]

async def seed_data():
    mongo_uri = os.environ.get("MONGODB_URI")
    if not mongo_uri:
        print("MONGODB_URI not set. Please set it to your Utkarsh_test cluster.")
        return
        
    client = AsyncIOMotorClient(mongo_uri, tlsCAFile=certifi.where())
    db = client.get_database()
    
    collection = db["utkarsh_test"]
    
    print("Clearing existing mock data...")
    # Optional: Clear existing data for a clean slate during testing
    # await collection.delete_many({}) 
    
    print(f"Inserting {len(MOCK_INVENTORY_DATA)} mock screens into MongoDB...")
    await collection.insert_many(MOCK_INVENTORY_DATA)
    
    print("Data seeded successfully!")
    print("Next step: Run `python ooh_agent/ingestion/vectorize_inventory.py` to embed this data.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(seed_data())
