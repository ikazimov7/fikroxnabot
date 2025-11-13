\
        import asyncio
        from config import AUTO_DELETE_SECONDS

        async def cleanup_worker():
            while True:
                await asyncio.sleep(AUTO_DELETE_SECONDS)
