import asyncio

from bg.app import bg_app


async def main():
    await bg_app()


if __name__ == "__main__":
    asyncio.run(main())
