import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import sys
from pathlib import Path
import logging

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import setup_logging

# Set up logging
LOG_FILE = "logs/mcpserver.log"
setup_logging(log_dir=LOG_FILE)
logger = logging.getLogger(__name__)

async def main():
    # Define server paramters
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "mcpserver/server.py"]
    )

    # Connect to server using STDIO transport
    async with stdio_client(server_params) as (read_stream, write_stream):
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