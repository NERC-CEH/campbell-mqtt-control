# Build virtualenv
FROM python:3.12-slim as build
WORKDIR /app
COPY pyproject.toml README.md /app/
COPY src /app/src
COPY .git /app/.git
RUN pip install --upgrade pip pdm
# Installs the codebase in editable mode into .venv
RUN pdm install

# Build production containerdocker
# Only the ./.venv ./src ./tests are present in the production image
FROM python:3.12-slim as prod
WORKDIR /app
RUN groupadd -g 999 python && \
    useradd -m -r -u 999 -g python python
RUN chown python:python /app
COPY --chown=python:python --from=build /app/.venv /app/.venv
COPY --chown=python:python --from=build /app/src /app/src
COPY --chown=python:python tests/ /app/tests

USER python
ENV PATH="/app/.venv/bin:$PATH"
ENV VIRTUAL_ENV="/app/.venv"
CMD ["python", "-m", "mypackage"]