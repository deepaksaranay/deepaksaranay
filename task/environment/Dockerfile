FROM public.ecr.aws/docker/library/python@sha256:90d88379d643208ec661e80b2faf07aa0272656a16dea7412428e57eb8921932

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
