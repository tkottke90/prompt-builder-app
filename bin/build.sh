#! /bin/bash

# Set default values for options
APP_NAME="assistant-api"
SKIP=0
REGISTRY="10.0.0.11:12000"
REPOSITORY="tkottke"
TAG=""
VERBOSE=0

while getopts ":vs:r:t:u:" opt; do
  case $opt in
    h) usage;;
    r) REGISTRY="$OPTARG" ;;
    s) SKIP=1 ;;
    t) TAG="$OPTARG" ;;
    u) REPOSITORY="$OPTARG" ;;
    v) VERBOSE=1 ;;
    \?) echo "Invalid option: -$OPTARG" >&2 ;;
  esac
done

# Define the usage function
usage() {
  echo "Usage: $(basename $0) [-s] [-v|--verbose] [-r|--registry <registry>] [-u|--repository <repository>]" >&2
  exit 0
}

function log() {
  echo "> $1" >&2
}

function verbose() {
  if [[ $VERBOSE -eq 1 ]]; then
    log $1
  fi
}

function buildAndPush() {
  docker build -q -t $1 .

  if [[ $SKIP -eq 0 ]]; then
    docker push $TAG_IMAGE
  else
    verbose "Docker Push Skipping Enabled - $1"
  fi
}

if [[ $VERBOSE -eq 1 ]]; then
  verbose "Verbose mode is enabled"
fi

IMAGE="$REGISTRY/$REPOSITORY/$APP_NAME:latest"
log "Created Latest Image: $IMAGE"

buildAndPush $IMAGE

# Check if TAG is an empty string and prompt user for a tag
if [[ -n "$TAG" ]]; then
  TAG_IMAGE="$REGISTRY/$REPOSITORY/$APP_NAME:$TAG"
  log "Created Tagged Image: $TAG_IMAGE"

  buildAndPush $TAG_IMAGE
fi

log "Complete"
