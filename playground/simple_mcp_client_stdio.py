import asyncio
from mcp import ClientSession, StdioServerParameters, Client
from mcp.client.stdio import stdio_client

params = StdioServerParameters(
    command="uv",
    args=["run", "python3", "playground/simple_mcp_server.py"]
)

async def test_client() -> None:
    async with stdio_client(params) as (read, write): #transport layer
        async with ClientSession(read, write) as session: #protocol layer
            await session.initialize()
            tools = await session.list_tools()
            print([t.name for t in tools.tools])

            sum_result = await session.call_tool("adding", {"a": 10, "b": 16})
            print(sum_result)
            print(sum_result.structured_content)

asyncio.run(test_client())