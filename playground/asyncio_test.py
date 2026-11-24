import asyncio

async def task(name):
    await asyncio.sleep(1)
    return f"Task {name} done"

async def main():
    results = await asyncio.gather(
        task("A"),
        task("B"),
        task("C")
    )
    print(results)

asyncio.run(main())   