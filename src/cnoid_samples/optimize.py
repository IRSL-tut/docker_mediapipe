import cnoid.Body
# ib
# coordinates
from numpy import array as npa
import numpy as np
# import math

lst = [['Root', None ],
       ['thumb0', None ],
       ['thumb2', None ],
       ['thumb3', None ],
       ['thumb3', npa([math.sqrt(0.5), 0., math.sqrt(0.5)]) * 0.0233 ],
       ['index_finger_1', None ],
       ['index_finger_2', None ],
       ['index_finger_3', None ],
       ['index_finger_3', npa([0., 0., 0.018]) ],
       ['middle_finger_1', None ],
       ['middle_finger_2', None ],
       ['middle_finger_3', None ],
       ['middle_finger_3', npa([0., 0., 0.0191]) ],
       ['ring_finger_1', None ],
       ['ring_finger_2', None ],
       ['ring_finger_3', None ],
       ['ring_finger_3', npa([0., 0., 0.0199]) ],
       ['pinky_1', None ],
       ['pinky_2', None ],
       ['pinky_3', None ],
       ['pinky_3', npa([0., 0., 0.0176])],
       ]

class ObjectPoints(object):
    def __init__(self, robot_model, settings):
        self.robot=robot_model
        self.robot.updateLinkTree()
        self.robot.initializePosition()
        self.update()
        res = []
        for l in settings:
            lk = self.robot.link(l[0])
            res.append(tuple([lk, l[1]]))
        self.point_settings = tuple(res)

    def update(self):
        self.robot.calcForwardKinematics()

    def setParam(self, vec):
        pos_ = vec[0:3] ## pos
        rot_ = vec[3:6] ## rot
        cds = coordinates(pos_)
        cds.setRPY(rot_)
        self.robot.rootLink.setPosition(cds.cnoidPosition)
        ang_ = vec[6:]  ## angles
        for idx, j in enumerate(self.robot.joints):
            j.q = ang_[idx]
        self.update()

    def getPoints(self, vec=None, camera_coords=None):
        if vec is not None:
            self.setParam(vec)
        pts=[]
        for p in self.point_settings:
            lk = p[0]
            p = p[1]
            cds = coordinates(lk.T)
            if p is None:
                pts.append(cds.pos)
            else:
                pts.append(cds.transform_vector(p))
        if camera_coords is not None:
            inv_cam = camera_coords.inverse_transformation()
            pts = [ inv_cam.transform_vector(p) for p in pts ]
        return pts

    def getProjectedPoints(self, vec=None, camera_matrix=None, camera_coords=None):
        pts = self.getPoints(vec=vec, camera_coords=camera_coords)
        if camera_matrix is not None:
            camera_matrix = ib.getCameraMatrix()
        res = []
        for pt in pts:
            uvs = camera_matrix.dot(pt)
            res.append( npa((uvs[0]/uvs[2], uvs[1]/uvs[2])) )
        return res
