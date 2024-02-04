#!/bin/bash
# This script downloads the webui repo and starts it.
# Optional argument: manager server ip, placed directly as an argument to the script eg: ./run.sh 10.0.25.92

REPO=text-generation-webui
if [ -d "$REPO" ]; then
  echo "text-generation-webui present, continuing."
else
  echo "text-generation-webui not present, cloning."
  git clone https://github.com/oobabooga/text-generation-webui
fi

sh ./text-generation-webui/start_linux.sh --api --multi-user --trust-remote-code --disk --auto-devices