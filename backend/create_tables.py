import asyncio
from db import engine, Base

async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("tables created")

asyncio.run(main())
