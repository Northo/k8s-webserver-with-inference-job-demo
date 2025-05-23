#!/bin/bash
set -e

# Configuration
IMAGE_NAME="k8s-webserver-with-inference-job-demo"
GITHUB_USER="northo"
REGISTRY="ghcr.io"
TAG="webserver-latest"

CONTEXT_DIR="$(dirname "$0")/../apps/webserver"

# Full image reference
IMAGE="$REGISTRY/$GITHUB_USER/$IMAGE_NAME:$TAG"

echo "Building image: $IMAGE"
podman build -t "$IMAGE" "$CONTEXT_DIR"

echo "Pushing image to GitHub Container Registry"
podman push "$IMAGE"

echo "Done."
