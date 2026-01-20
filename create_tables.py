import asyncio
from database import engine, Base
import models  # MUHIM: model import qilinmasa jadval yaratilmaydi

async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tables created")

if __name__ == "__main__":
    asyncio.run(main())
