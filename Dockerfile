FROM python:3.11-slim AS base

RUN apt-get update && apt-get install -y \
    git \
    wget \
    flex \
    bison \
    gperf \
    cmake \
    ninja-build \
    ccache \
    libffi-dev \
    libssl-dev \
    dfu-util \
    libusb-1.0-0 \
    gosu \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install toml

# Cache layer: clone lvgl_micropython and fetch heavy deps
FROM base AS deps
WORKDIR /cache
RUN git clone --depth 1 https://github.com/lvgl-micropython/lvgl_micropython.git && \
    cd lvgl_micropython && \
    python3 make.py esp32 --help || true

# Build stage
FROM base AS builder
WORKDIR /build

# Copy cached repo
COPY --from=deps /cache/lvgl_micropython /build/lvgl_micropython

# Entrypoint handles uid/gid and builds
COPY scripts/docker-entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["build"]
