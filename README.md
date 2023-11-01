
# Using Mediapipe

## Docker imageのビルド

```
$git clone --recursive https://github.com/IRSL-tut/docker_mediapipe
$ cd docker_mediapipe
$ ./build.sh
```

## Docker image の実行

### Jupyterの実行(docker_mediapipeディレクトリで)

```
 ./run.sh jupyter --no-gpu -w $(pwd) --image docker_mediapipe
```

### Jupyterの実行 / ライブラリのローカル変更を使う

```
 ./run.sh jupyter --no-gpu -w $(pwd) --image docker_mediapipe --mount " -v $(pwd)/src/mppack:/IRSL_PYTHONPATH/mppack"
```

### Jupyter実行して以下のリンクをブラウザで開く

[ http://localhost:8888 ](http://localhost:8888)

### コンソールで開く

```
 ./run.sh --no-gpu -w $(pwd) --image docker_mediapipe
```

### コンソールで開く / ライブラリのローカル変更を使う

```
 ./run.sh --no-gpu -w $(pwd) --image docker_mediapipe --mount " -v $(pwd)/src/mppack:/IRSL_PYTHONPATH/mppack"
```

## Camera calibration

```
roslaunch launch/cv_cam.launch device:=/dev/video0
```

```
rosrun camera_calibration cameracalibrator.py --no-service-check -p circles -s 8x7 -q 0.03 image:=/cv_camera/image_raw
```
