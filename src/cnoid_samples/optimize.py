import cnoid.Body
# ib
# coordinates
from numpy import array as npa
import numpy as np
# import math

lst_all = [['Root', None ],
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

### fixed point for PnP
lst_fixed = [['Root', None ],
             ['thumb0', None ],
             ['index_finger_0', None ],
             ['middle_finger_0', None ],
             ['ring_finger_0', None ],
             ['pinky_0', None ]
             ]

class ObjectPoints(object):
    def __init__(self, robot_model, settings, camera_matrix=None, offset_coordinates=None):
        self.robot=robot_model
        self.robot.updateLinkTree()
        self.robot.initializePosition()
        self.update()
        res = []
        for l in settings:
            lk = self.robot.link(l[0])
            res.append(tuple([lk, l[1]]))
        self.point_settings = tuple(res)

        self._camera_matrix = camera_matrix
        if offset_coordinates is not None:
            self.setModelOffset(offset_coordinates)
        else:
            self._offset_coords = None
            self._offset_inv_coords = None

    def setCameraMatrix(self, cam_mat):
        self._camera_matrix = cam_mat

    def setModelOffset(self, offset_coordinates):
        self._offset_coords = offset_coordinates
        self._offset_inv_coords = offset_coordinates.inverse_transformation()

    def update(self):
        self.robot.calcForwardKinematics()

    def getObjectPoints(self):
        base_cds = coordinates(self.robot.rootLink.T)
        pts=[]
        for p in self.point_settings:
            lk = p[0]
            p  = p[1]
            cds = base_cds.transformation( coordinates(lk.T) )
            if p is None:
                pts.append(cds.pos)
            else:
                pts.append(cds.transform_vector(p))
        return pts

    def setParam(self, vec):
        pos_ = vec[0:3] ## pos
        rot_ = vec[3:6] ## rot
        cds = coordinates(pos_)
        cds.setRPY(rot_)
        if self._offset_coords is not None:
            cds = self._offset_coords.get_transformed(cds)
        self.robot.rootLink.setPosition(cds.cnoidPosition)
        ang_ = vec[6:]  ## angles
        for idx, j in enumerate(self.robot.joints):
            j.q = ang_[idx]
        self.update()

    def getParam(self):
        cds = coordinates(self.robot.rootLink.T)
        if self._offset_inv_coords is not None:
            cds.transform(self._offset_inv_coords)
        pos_ = cds.pos
        rpy_ = cds.getRPY()
        res = [ pos_[0], pos_[1], pos_[2], rpy_[0], rpy_[1], rpy_[2] ]
        for j in self.robot.joints:
            res.append(j.q)
        return np.array(res)

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
        if camera_matrix is None:
            if self._camera_matrix is not None:
                camera_matrix = self._camera_matrix
            else:
                camera_matrix = ib.getCameraMatrix()
        res = []
        for pt in pts:
            uvs = camera_matrix.dot(pt)
            res.append( npa((uvs[0]/uvs[2], uvs[1]/uvs[2])) )
        return res

    def evalMethod(self, vec, points_on_image, weight=None, inputFilter=None, camera_coords=None):
        points_from_obj = self.getProjectedPoints(vec, camera_coords=camera_coords)

        if inputFilter is not None:
            points_from_obj = [ points_from_obj[idx] for idx in inputFilter ]
            points_on_image = [ points_on_image[idx] for idx in inputFilter ]

        if weight is not None:
            return np.array( [ w * np.linalg.norm(p_obj - p_img)  for p_obj, p_img, w in zip(points_from_obj, points_on_image, weight) ] )
        else:
            return np.array( [ np.linalg.norm(p_obj - p_img)  for p_obj, p_img in zip(points_from_obj, points_on_image) ] )

    def makeBounds(self, x=2.0, y=2.0, min_z=0.2, max_z=4.0, roll=PI/2, pitch=PI/2, yaw=PI/2, ratio=1.0, inputFilter=None):
        upper_bound = [  x,   y,  max_z,  roll,  pitch,  yaw ]
        lower_bound = [ -x,  -y,  min_z, -roll, -pitch, -yaw ]
        for j in self.robot.joints:
            upper_bound.append(j.q_upper)
            lower_bound.append(j.q_lower)

        if inputFilter is not None:
            upper_bound = [ upper_bound[idx] for idx in inputFilter ]
            lower_bound = [ lower_bound[idx] for idx in inputFilter ]

        return scipy.optimize.Bounds(lb=lower_bound, ub=upper_bound)

