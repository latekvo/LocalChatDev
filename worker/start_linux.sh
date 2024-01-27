REPO=text-generation-webui
if [ -d '$REPO']; then
  echo "text-generation-webui present, continuing."
else
  echo "text-generation-webui not present, cloning."
  git clone https://github.com/oobabooga/text-generation-webui
fi

sh ./text-generation-webui/start_linux.sh --api --no-webui