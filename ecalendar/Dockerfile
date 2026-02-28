# Stage 1: Build frontend
FROM node:20-alpine AS frontend
WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Stage 2: Runtime - Home Assistant addon base
ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:3.15
FROM ${BUILD_FROM}

RUN apk add --no-cache nginx python3 py3-pip \
    && rm -f /etc/nginx/http.d/default.conf

COPY backend/requirements.txt /tmp/
RUN apk add --no-cache --virtual .build-deps gcc musl-dev python3-dev \
    && pip3 install --no-cache-dir -r /tmp/requirements.txt \
    && apk del .build-deps

WORKDIR /app
COPY backend/app ./app
COPY --from=frontend /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/http.d/default.conf

ENV PYTHONUNBUFFERED=1
ENV DATA_DIR=/data

RUN mkdir -p /data

EXPOSE 8099

COPY run.sh /
RUN chmod +x /run.sh
CMD ["/run.sh"]
