from mcp.server import MCPServer

mcp = MCPServer("toy")

@mcp.tool()
def adding(a: int, b: int) -> int:
    """
    Add 2 numbers

    Args:
        a (int)
        b (int): Description.

    Returns:
        int
    """
    return a + b

@mcp.tool()
def subtract(a: int, b:int) -> int:
    """
    Subtract 2 numbers.

    Args:
        a (int): Description.
        b (int): Description.

    Returns:
        int: Description.
    """
    return a - b

@mcp.resource("greeting://{name}")
def greeting(name: str) -> str:
    """Greet someone by name."""
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")   # http://127.0.0.1:8000/mcp