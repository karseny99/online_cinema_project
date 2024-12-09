from app.repository.movie import *
import asyncio


async def main():
    await get_movie_info()

if __name__ == "__main__":
    asyncio.run(main())