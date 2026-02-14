# DEPRECATED: This Dockerfile has incorrect build context and CMD.
# Use phaseIV/backend/Dockerfile.mcp instead.
#
# Issues with this file:
# 1. Copies only mcp_server/ contents, breaking app.mcp_tools.* imports
# 2. Uses "uvicorn main:app" which fails with relative import errors
# 3. Only installs fastapi/uvicorn, missing mcp-use and other dependencies
#
# Correct usage:
#   docker build -f phaseIV/backend/Dockerfile.mcp -t mcp-server:latest phaseIV/backend/

FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir fastapi uvicorn

EXPOSE 8002

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
