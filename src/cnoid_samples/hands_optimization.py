## 最適化計算プログラム for Hand（SciPy）
exec(open('/choreonoid_ws/install/share/irsl_choreonoid/sample/irsl_import.py').read())
import scipy
exec(open('src/cnoid_samples/optimize.py').read())

itm_ = ib.loadRobotItem('src/cnoid_samples/HandModel.body')
rb = RobotModel(itm_)
cam_cds, fov = ib.getCameraCoords()
cam_matrix = ib.getCameraMatrix()
di=DrawInterface()

## make projected points generator
op = ObjectPoints(rb.robot, lst)

## make initial parameter
x0 = np.zeros(26)
op.setParam(x0)
rb.revert(); rb.hook() ## for RobotModel

## make problem parameter to be solved
x_p = np.zeros(26)
x_p[0] = 0.2
x_p[1] = 0.3
x_p[2] = 0.1
op.setParam(x_p)
rb.revert(); rb.hook() ## for RobotModel
pts_p = mkshapes.makePoints(op.getPoints(camera_coords=cam_cds)) ## view on choreonoid
di.addObject(pts_p) ## view on choreonoid
img_pt_org = op.getProjectedPoints(camera_matrix=cam_matrix, camera_coords=cam_cds)

def evalfunc(x, *args, **kwargs):
    ## set parameter
    op.setParam(x)
    ## making projected points
    img_pt = op.getProjectedPoints(camera_matrix=cam_matrix, camera_coords=cam_cds)
    res = []
    for a, b in zip(img_pt, img_pt_org):
        res.append(np.linalg.norm(a - b))
    return res

result = scipy.optimize.least_squares(evalfunc, x0, xtol=1e-15, loss='linear', method='dogbox')

## check result
## result.x should be qeual to x_p
op.setParam(result.x)
rb.revert(); rb.hook() ## for RobotModel
pts_p_res = mkshapes.makePoints(op.getPoints(camera_coords=cam_cds), colors=[[1,0,0]]) ## view on choreonoid
di.addObject(pts_p_res) ## view on choreonoid
