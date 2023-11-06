## 最適化計算プログラム（OpenCV）
## opencv version
exec(open('/choreonoid_ws/install/share/irsl_choreonoid/sample/irsl_import.py').read())

### 物体上の点を作る
def makeObjectPoints(cds):
    pts = [ npa([-0.5, -0.5, 0 ]),
            npa([-0.5,  0.5, 0 ]),
            npa([ 0.5,  0.5, 0 ]),
            npa([ 0.5, -0.5, 0 ]) ]
    return [ cds.transform_vector(pt) for pt in pts ]

cam_cds, fov = ib.getCameraCoords()
### カメラマトリックス
cam_matrix = ib.getCameraMatrix()
### 対象物体上の点
obj_pt = makeObjectPoints(coordinates())

### 対象物体モデル
world_obj = coordinates(npa([0.6, -0.3, 0.2]))
world_obj.setRPY(0.1, 0.2, 0.3)

### 対象物体モデルにおける投影点
img_pt_org = ib.projectPoints(makeObjectPoints(world_obj))

### 対応点の最適化問題を解く
import cv2
res, rvec, tvec = cv2.solvePnP(npa(obj_pt), npa(img_pt), cam_matrix, npa([0, 0, 0, 0, 0], dtype='float64'), )
mat, jac = cv2.Rodrigues(rvec)
obj_on_cam = coordinates(tvec, mat)
obj_on_world = cam_cds.copy().transform(obj_on_cam)

## check result
# world_obj equal to obj_on_world
world_obj
obj_on_world
