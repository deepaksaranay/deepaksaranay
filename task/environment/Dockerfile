FROM public.ecr.aws/docker/library/python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc g++ \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    shapely==2.0.7 \
    pyproj==3.7.1 \
    pytest==8.3.4

RUN mkdir -p /app/data /logs/verifier
COPY data/ /app/data/
WORKDIR /app
