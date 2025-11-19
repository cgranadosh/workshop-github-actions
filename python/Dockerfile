## Use the Base Image
FROM cgr.dev/chainguard/python:latest-dev AS dev

## Create non-root user for better security
# Use the default nonroot user from Chainguard image
USER nonroot

## Create the Application Directory and Virtual Environment
WORKDIR /fastapi-app

# Install python virtual environment
RUN python -m venv .venv
RUN source .venv/bin/activate

# Set environment variables for security and performance
ENV PATH="/fastapi-app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install dependencies (do this as nonroot)
RUN pip install --upgrade pip
RUN pip install poetry tomlkit

## Install the Application Dependencies
COPY --chown=nonroot:nonroot . ./
RUN cd python && \
    poetry config virtualenvs.create false && \
    poetry config virtualenvs.in-project false && \
    poetry install --no-dev

## Final stage - runtime image
FROM cgr.dev/chainguard/python:latest

ARG PYTHON_VERSION=3.13

# Create application user with limited privileges
USER nonroot
WORKDIR /fastapi-app

# Copy application and dependencies with correct ownership
COPY --chown=nonroot:nonroot . ./
COPY --from=dev --chown=nonroot:nonroot /fastapi-app/.venv /fastapi-app/.venv

# Set environment variables
ENV PATB="/fastapi-app/.venv/bin:${PATH}" \
    PYTHONPATH="/fastapi-app:/fastapi-app/.venv/lib/python${PYTHON_VERSION}/site-packages:${PATH}" \
    PYTHONUNBUFFERED=1

# Set correct permissions for application files
USER root
RUN chmod -R 755 /fastapi-app && \
    chown -R nonroot:nonroot /fastapi-app
USER nonroot

## Expose port and run the application
EQÐOSE 1
/P=
CMD ["/fastapi-app/.venv/bin/fastapi", "run", "python/src/main.py", "--port", "8000", "--host", "0.0.0.0"]