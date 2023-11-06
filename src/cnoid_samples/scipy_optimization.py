## 最適化計算プログラム（scipy）
## scipy version
exec(open('/choreonoid_ws/install/share/irsl_choreonoid/sample/irsl_import.py').read())
import scipy
###
def makeObjectPoints(cds):
    pts = [ npa([-0.5, -0.5, 0 ]),
            npa([-0.5,  0.5, 0 ]),
            npa([ 0.5,  0.5, 0 ]),
            npa([ 0.5, -0.5, 0 ]) ]
    return [ cds.transform_vector(pt) for pt in pts ]

cam_matrix = ib.getCameraMatrix()
obj_pt = makeObjectPoints(coordinates())

## answer coordinates
world_obj = coordinates(npa([0.6, -0.3, 0.2]))
world_obj.setRPY(0.1, 0.2, 0.3)

## uv-points on image(answer coordinates)
img_pt_org = ib.projectPoints(makeObjectPoints(world_obj))

##
def paramToCoords(x):
    cds = coordinates(npa([x[0], x[1], x[2]]))
    cds.setRPY(x[3], x[4], x[5])
    return cds

def evalfunc(x, *args, **kwargs):
    cds = paramToCoords(x)
    ## coords to uv-points
    img_pt = ib.projectPoints(makeObjectPoints(cds))
    ## diff on uv-points(x) between img_pt_org
    res = []
    for a, b in zip(img_pt, img_pt_org):
        res.append(np.linalg.norm(a - b))
    return res

x0 = npa([0., 0., 0., 0, 0, 0], dtype='float64')

## minimize | evalfunc(param) |
result = scipy.optimize.least_squares(evalfunc, x0, xtol=1e-15, loss='linear', method='dogbox')

## check result
# world_obj equal to paramToCoords(result.x)
paramToCoords(result.x)
world_obj
