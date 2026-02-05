import asyncio
import nest_asyncio # patches the asyncio module to enable nested event loops
from mcp import ClientSession
from mcp.client.sse import sse_client

nest_asyncio.apply() # For interactive environment where an event loop is already running

import logging
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import setup_logging

# Set up logging
LOG_FILE = "logs/mcpserver.log"
setup_logging(log_dir=LOG_FILE)
logger = logging.getLogger(__name__)

"""
Initial Checks:
1. The server is already running before executing this scirpt.
2. The server is configured to SSE transport.
3. The server is listening on port 8050.

>>> uv run mcpserver/server.py
"""

async def main():
    # Connect server using SSE
    async with sse_client("http://localhost:8000/sse") as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()

            # List available tools
            tools_result = await session.list_tools()
            logger.info("Avaible tools")
            for tool in tools_result.tools:
                logger.info(f"  - {tool.name}: {tool.description}")
            
            # Call the Weather tool
            result = await session.call_tool("get_alerts", arguments={"state": "CA"})
            logger.info(f"Here are the weather alerts: {result.content[0].text}")

if __name__ == "__main__":
    asyncio.run(main())