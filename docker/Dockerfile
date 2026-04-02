FROM python:3.12-slim@sha256:3d5ed973e45820f5ba5e46bd065bd88b3a504ff0724d85980dcd05eab361fcf4 AS cache-stage

# uv binaries: https://github.com/astral-sh/uv/pkgs/container/uv
# pinned by version tag + linux/amd64 manifest digest
COPY --from=ghcr.io/astral-sh/uv:0.11.1@sha256:b6ca5767729b57719f1edf206123c8cb474a4b3a198cc28e1fd92eee3d3898fe /uv /usr/local/bin/uv

WORKDIR /workspace

COPY pyproject.toml uv.lock README.md ./

# mount cache: uv finds the cached wheels and only downloads what changed
# cleanup: strip .pyc files and __pycache__ dirs to reduce layer size
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project --python-platform linux && \
    find /workspace/.venv -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true && \
    find /workspace/.venv -name "*.pyc" -delete 2>/dev/null || true

FROM python:3.12-slim@sha256:3d5ed973e45820f5ba5e46bd065bd88b3a504ff0724d85980dcd05eab361fcf4 AS build-stage

# vars defined before use
ENV VENV_PATH="/opt/airflow/.venv"
ENV AIRFLOW_HOME="/opt/airflow"
ENV PATH="${VENV_PATH}/bin:${PATH}"
ENV PYTHONPATH="${AIRFLOW_HOME}/src:${VENV_PATH}/lib/python3.12/site-packages"


# nonroot + uid=50000 && default shell for the user
RUN useradd -ms /bin/bash -u 50000 airflow

# official airflow helm-chart relies on /entrypoint script at the root path
# https://hub.docker.com/layers/apache/airflow/slim-3.1.8-python3.12
COPY --from=apache/airflow:slim-3.1.8-python3.12@sha256:20c7b26028bae6a4cec6da874568b10a19422df431abec6fa08ebbd5d8a7e0fa \
    /entrypoint /entrypoint

COPY --from=cache-stage /workspace/.venv ${VENV_PATH}

# $ cat $VENV_PATH/bin/airflow | head -1
# the shebang line is pointing into /workspace/.venv/bin/python [--from=cache-stage]
# but in the [build-stage] the venv lives at /opt/airflow/.venv; rewrite the shebangs after copying the .venv
RUN find ${VENV_PATH}/bin -type f | xargs sed -i 's|#!/workspace/.venv|#!/opt/airflow/.venv|g' 2>/dev/null || true

# mkdirs && sets ownership before user switch
RUN mkdir -p ${AIRFLOW_HOME}/dags ${AIRFLOW_HOME}/logs ${AIRFLOW_HOME}/plugins && \
    chown -R airflow: ${AIRFLOW_HOME}

USER airflow

COPY --chown=airflow:airflow src/btc_flow/ ${AIRFLOW_HOME}/src/btc_flow/
COPY --chown=airflow:airflow src/conf/ ${AIRFLOW_HOME}/src/conf/
COPY --chown=airflow:airflow dags/ ${AIRFLOW_HOME}/dags/
