from mcp import Client
import asyncio

async def test_server() -> None:
    async with Client("http://127.0.0.1:8000/mcp") as client:
        tools = await client.list_tools()
        print(f"Available tools: {[t.name for t in tools.tools]}")

asyncio.run(test_server())