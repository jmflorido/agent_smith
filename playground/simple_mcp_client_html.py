from mcp import Client
import asyncio
from icecream import ic

async def test_server() -> None:
    async with Client("http://127.0.0.1:8000/mcp") as client:
        tools = await client.list_tools()
        print(f"Available tools: {[t.name for t in tools.tools]}")

        sum_result = await client.call_tool("adding", {
            "a": 5,
            "b": 3
        })
        ic(sum_result)
        ic((sum_result.structured_content["result"]))

asyncio.run(test_server())