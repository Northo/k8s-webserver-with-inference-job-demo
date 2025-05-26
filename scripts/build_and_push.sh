#!/bin/bash

set -e

# Set image config
DOCKER_REGISTRY="ghcr.io"
IMAGE_NAME="job-submitter"
DOCKER_USER="northo"
TAG="latest"
FULL_IMAGE="$DOCKER_REGISTRY/$DOCKER_USER/$IMAGE_NAME:$TAG"

# Resolve the directory this script is in
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCKER_CONTEXT="$SCRIPT_DIR/../apps/api"

echo "🔨 Building Docker image: $FULL_IMAGE"
echo "📁 Docker context: $DOCKER_CONTEXT"

podman build -t "$FULL_IMAGE" "$DOCKER_CONTEXT"

 #echo "🔐 Logging in to Docker Hub"
 #docker login

echo "📤 Pushing Docker image to Docker Hub"
podman push "$FULL_IMAGE"

echo "✅ Successfully pushed: $FULL_IMAGE"

