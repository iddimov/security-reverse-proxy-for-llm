FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# 1. Disable the creation of a virtual environment entirely inside the container.
# This installs dependencies into the system site-packages, which is 
# standard practice for single-app containers and prevents pathing errors.
ENV UV_SYSTEM_PYTHON=1

# 2. Copy dependency files
COPY pyproject.toml uv.lock ./

# 3. Install dependencies directly into system Python
RUN uv pip install --system --no-cache -r pyproject.toml

# 4. Install the SpaCy model
RUN uv pip install --system https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl

# 5. Copy the application code
COPY . .

EXPOSE 8000

# 6. Start the application using the global uvicorn installed in the system
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]