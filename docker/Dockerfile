FROM python:3.12-slim AS builder

# builds the UV-binary from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# copy only the dependency files: --uv sync needs README
COPY pyproject.toml uv.lock README.md ./

# install dependencies:
# --skips dev-group --skips installing the project --sync for Linux
RUN uv sync --frozen --no-dev --no-install-project --python-platform linux

FROM python:3.12-slim AS final

# all vars defined before use: --venv is injected into PATH
ENV VENV_PATH="/opt/airflow/.venv"
ENV AIRFLOW_HOME="/opt/airflow"
ENV PATH="${VENV_PATH}/bin:${PATH}"
ENV PYTHONPATH="${AIRFLOW_HOME}/src:${VENV_PATH}/lib/python3.12/site-packages"

RUN apt-get update && apt-get install -y \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# create a non-root `airflow` user for security
RUN useradd -ms /bin/bash airflow

COPY --from=builder /app/.venv ${VENV_PATH}
# $ cat $VENV_PATH/bin/airflow | head -1
# the shebang line is pointing into /app/.venv/bin/python (--from=builder)
# but in the final image the venv lives at /opt/airflow/.venv.
# rewrite the shebangs after copying the venv
RUN find ${VENV_PATH}/bin -type f | xargs sed -i 's|#!/app/.venv|#!/opt/airflow/.venv|g' 2>/dev/null || true

# creates Airflow dirs and sets ownership before switching user
RUN mkdir -p ${AIRFLOW_HOME}/dags ${AIRFLOW_HOME}/logs ${AIRFLOW_HOME}/plugins \
    && chown -R airflow: ${AIRFLOW_HOME}

# all subsequent commands run as non-root
USER airflow

COPY --chown=airflow:airflow src/btc_flow/ ${AIRFLOW_HOME}/src/btc_flow/
COPY --chown=airflow:airflow src/conf/ ${AIRFLOW_HOME}/src/conf/
COPY --chown=airflow:airflow dags/ ${AIRFLOW_HOME}/dags/