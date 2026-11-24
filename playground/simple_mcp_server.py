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

@mcp.tool()
def greeting_formal(name: str) -> str:
    """Greet someone by name."""
    return f"Hello, {name}!"


@mcp.tool()
def greeting_street_style(name: str) -> str:
    """Greet someone by name."""
    return f"Eyyyy, watsup {name}!!!"


@mcp.prompt()
def greeting(name: str) -> str:
    """Generates a message asking for a greeting"""
    return f"""
        Return a greeting message for a user called '{name}'. 
        if the user is called 'Laurent', use a formal style, else use a street style.
        """

if __name__ == "__main__":
    # mcp.run(transport="streamable-http")   # http://127.0.0.1:8000/mcp
    mcp.run(transport="stdio")