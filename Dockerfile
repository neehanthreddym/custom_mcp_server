FROM python:3.12-slim-bookworm

WORKDIR /app

# Install uv package manager
RUN pip install uv

# Copy dependency files first (for better caching)
COPY requirements.txt .

# Create virtual environment and install dependencies
RUN uv venv
RUN uv pip install -r requirements.txt

# Copy source code
COPY mcpserver/server.py .
COPY mcpserver/client-sse.py .
COPY logger.py .

# Set environment variables
ENV MCP_TRANSPORT=sse
ENV PORT=8000

# Expose the port
EXPOSE 8000

# Run the server
CMD ["uv", "run", "server.py"]