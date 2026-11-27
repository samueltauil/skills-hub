# syntax=docker/dockerfile:1

# --- Build stage ---
FROM golang:1.23-alpine AS build
WORKDIR /src

# Cache dependency downloads; bind-mount the manifest since go mod download doesn't rewrite it
RUN --mount=type=bind,source=go.mod,target=go.mod \
    --mount=type=bind,source=go.sum,target=go.sum \
    --mount=type=cache,target=/go/pkg/mod \
    go mod download

# Build the binary
COPY . .
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    CGO_ENABLED=0 go build -ldflags="-s -w" -o /app/server ./cmd/server

# --- Runtime stage ---
FROM gcr.io/distroless/static-debian12:nonroot AS runtime
WORKDIR /app

COPY --from=build --link /app/server .

USER nonroot:nonroot
EXPOSE 8080

LABEL org.opencontainers.image.source="<source-repository-url>"

ENTRYPOINT ["./server"]
