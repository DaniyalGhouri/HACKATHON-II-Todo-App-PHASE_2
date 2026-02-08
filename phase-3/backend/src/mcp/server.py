from mcp.server.fastmcp import FastMCP

# Initialize the MCP server
# This server will host the tools that the OpenAI Agent will call
mcp = FastMCP("TodoMCP")

# Tools will be registered here in subsequent steps
# Example:
# @mcp.tool()
# def my_tool(): ...
