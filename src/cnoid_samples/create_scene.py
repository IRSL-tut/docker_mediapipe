
## 便利関数
def makeListInterpolation(start, end, size=10):
    res = [ start ]
    for i in range(size-1):
        rb_ = (i + 1)/size
        ra_ = (size - i -1)/size
        lst_=[]
        for a, b in zip(start, end):
            lst_.append(ra_ * a + rb_ * b)
        res.append(lst_)
    res.append(end)
    return res

def makeVectorInterpolation(start, end, size=10):
    res = [ start ]
    for i in range(size-1):
        rb_ = (i + 1)/size
        ra_ = (size - i -1)/size
        res.append(ra_ * start + rb_ * end)
    res.append(end)
    return res

def makeCoordsInterpolation(start, end, size=10):
    res = [ start.copy() ]
    for i in range(size-1):
        ratio_ = (i + 1)/size
        res.append(start.mid_coords(ratio_, end))
    res.append(end.copy())
    return res

### カメラ位置の設定
def setCameraPosition2D(x, y, theta, z=0.0, eye_height=1.7, view_height=0.7, view_x=1.2, view_y=0.0, fov=None, robot=None, robotOffset=[0,0,0.8]):
    eye_ = npa([x, y, z + eye_height])
    up_ = coordinates.Z
    stand_cds = coordinates(npa([x, y, z])).rotate(theta, coordinates.Z)
    if robot is not None:
        rcds = stand_cds.copy().translate(npa(robotOffset))
        robot.rootCoords(rcds)
    at_ = stand_cds.transform_vector(npa([view_x, view_y, view_height]))
    cam_ = ib.cameraPositionLookingAt(eye_, at_, up_)
    ib.setCameraCoords(cam_, fov=fov, opencv=False)

### ロボット位置の設定
def setRobotPosition2D(x, y, theta, z=0.0, robot=None, robotOffset=[0,0,0.8]):
    stand_cds = coordinates(npa([x, y, z])).rotate(theta, coordinates.Z)
    if robot is not None:
        rcds = stand_cds.copy().translate(npa(robotOffset))
        robot.rootCoords(rcds)

### 位置の取得
def getCameraPosition2D():
    cds, fov = ib.getCameraCoords()
    zz=cds.z_axis
    return [ cds.pos[0], cds.pos[1], math.atan2(zz[1], zz[0]) ]

def getRobotPosition2D(robot):
    coords = robot.rootCoords()
    x = coords.pos[0]
    y = coords.pos[1]
    theta = coords.RPY[2]
    return [x, y, theta]

### データのセーブロード
import pickle
def writeData(fname, robot):
    cds_, fov_ = ib.getCameraCoords()
    data_ = (getCameraPosition2D(), getRobotPosition2D(robot=robot), robot.angleVector(),
             ru.make_coords_map(cds_), ru.make_coords_map(robot.rootCoords()), fov_)
    with open(fname, mode='wb') as f:
        pickle.dump(data_, f)

def readData(fname):
    res_ = None
    with open(fname, mode='rb') as f:
        res_ = pickle.load(f)
    return res_

def applyData(data_, robot):
    ib.setCameraCoords(ru.make_coordinates(data_[3]))
    robot.angleVector(data_[2])
    robot.rootCoords(ru.make_coordinates(data_[4]))

def applyData2D(data_, robot):
    setCameraPosition2D(*(data_[0]))
    setRobotPosition2D(*(data_[1]), robot=robot)
    robot.angleVector(data_[2])

def makeImages(lst, robot=None, rate=10, prefix='image'):
    if robot is None:
        robot = eval('robot')
    cntr = 0
    prev_data_ = readData(lst[0][0])
    mode_ = robot.setMode()
    robot.setMode(-1)## no update  mode
    for fname, tm in lst[1:]:
        data_ = readData(fname)
        size = int(tm * rate)
        # d0 = makeListInterpolation(prev_data_[0], data_[0], size=size)
        # d1 = makeListInterpolation(prev_data_[1], data_[1], size=size)
        d0 = makeCoordsInterpolation(ru.make_coordinates(prev_data_[3]),
                                     ru.make_coordinates(data_[3]), size=size)
        d1 = makeCoordsInterpolation(ru.make_coordinates(prev_data_[4]),
                                     ru.make_coordinates(data_[4]), size=size)
        d2 = makeVectorInterpolation(prev_data_[2], data_[2], size=size)
        for l0, l1, v0 in zip(d0, d1, d2):
            #setCameraPosition2D(l0*)
            #setRobotPosition2D(l0*, robot=robot)
            ib.setCameraCoords(l0, update=False)
            robot.rootCoords(l1)
            robot.angleVector(v0)
            robot.flush(updateGui=True)
            fname='{}{:0=6}.png'.format(prefix, cntr)
            cntr += 1
            ib.saveImageOfScene(fname)
        prev_data_ = data_
    robot.setMode(mode_)## revert mode

import time
def moveRobot(lst, robot=None, rate=10, moveCamera=False):
    if robot is None:
        robot = eval('robot')
    cntr = 0
    prev_data_ = readData(lst[0][0])
    mode_ = robot.setMode()
    # robot.setMode(-1)## no update mode
    for fname, tm in lst[1:]:
        data_ = readData(fname)
        size = int(tm * rate)
        # d0 = makeListInterpolation(prev_data_[0], data_[0], size=size)
        # d1 = makeListInterpolation(prev_data_[1], data_[1], size=size)
        d0 = makeCoordsInterpolation(ru.make_coordinates(prev_data_[3]),
                                     ru.make_coordinates(data_[3]), size=size)
        d1 = makeCoordsInterpolation(ru.make_coordinates(prev_data_[4]),
                                     ru.make_coordinates(data_[4]), size=size)
        d2 = makeVectorInterpolation(prev_data_[2], data_[2], size=size)
        ##
        for l0, l1, v0 in zip(d0, d1, d2):
            #setCameraPosition2D(l0*)
            #setRobotPosition2D(l0*, robot=robot)
            if moveCamera:
                ib.setCameraCoords(l0, update=False)
            robot.rootCoords(l1)
            robot.angleVector(v0)
            robot.flush(updateGui=True)
            #fname='{}{:0=6}.png'.format(prefix, cntr)
            #cntr += 1
            #ib.saveImageOfScene(fname)
            time.sleep(1.0/rate)
        prev_data_ = data_
    #robot.setMode(mode_)## revert mode

## set size of Image
# ib.currentSceneWidget().setScreenSize(800,600)
## make video file from images creating by makeImages
# ffmpeg -framerate 10 -i image%06d.jpg -vcodec libx264 -pix_fmt yuv420p -r 30 out.mp4
