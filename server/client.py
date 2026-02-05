import asyncio
import sys
import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import setup_logging

# Set up logging
LOG_FILE = "logs/mcpchatbot.log"
setup_logging(log_dir=LOG_FILE)
logger = logging.getLogger(__name__)

async def run_memory_chat():
    # Load environment variables
    load_dotenv()
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

    # MCP server configuration
    config = "server/weather.json"

    logger.info("Initiating Chatbot...")

    # Create MCPClient from configuration dictionary
    client = MCPClient.from_config_file(config)

    # Define LLM
    llm = ChatGroq(model_name="openai/gpt-oss-20b", temperature=0)

    # Create agent with the client
    agent = MCPAgent(
        llm=llm, 
        client=client, 
        max_steps=10,
        memory_enabled=True
    )

    print("\n" + "-"*10 + " Interactive MCP Chatbot " + "-"*10 + "\n")
    print("Type 'exit', 'quit', or 'q' to exit.\n")
    print("Type 'clear' or 'cls' to clear conversation history.\n")
    print("-"*45 + "\n")

    try:
        while True:
            # Get user input
            user_query = input("You: ")

            # Check if user wants to exit the chat
            if user_query in ["exit", "quit", "q"]:
                logger.info("Ending chatbot...")
                break

            # Check if user wants to clear the conversation history
            if user_query in ["clear", "cls"]:
                agent.clear_conversation_history()
                logger.info("Conversation history cleared.")
                continue

            try:     
                # Run the query
                result = await agent.run(user_query)
                print(f"\nAssistant: {result}")
            except Exception as e:
                logger.exception("Error while running agent")
                print("\nAssistant: ⚠️ Something went wrong. Please try again.")
    finally:
        # Clean up
        if client and client.sessions:
            await client.close_all_sessions()

if __name__ == '__main__':
    asyncio.run(run_memory_chat())