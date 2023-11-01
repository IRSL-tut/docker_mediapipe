set -x

SUDO_STRING=`groups|grep docker`
SUDO=""
if [ -z "$SUDO_STRING" ]; then
  SUDO="sudo "
fi

DOCKER_BUILDKIT=1 $SUDO docker build --pull \
    --force-rm=true \
    -f Dockerfile.add_mediapipe \
    -t docker_mediapipe .
