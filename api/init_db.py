import asyncio
import asyncpg
import os

async def run():
    # URI format asyncpg expects: postgresql://user:password@host:port/database
    url = "postgresql://qsentra_admin:QS3ntr@PNB2026!@localhost:5432/qsentra"
    try:
        conn = await asyncpg.connect(url)
        with open('schema.sql', 'r') as f:
            schema = f.read()
        await conn.execute(schema)
        print("Schema created successfully.")
        await conn.close()
    except Exception as e:
        print("Error:", e)

if __name__ == '__main__':
    asyncio.run(run())
