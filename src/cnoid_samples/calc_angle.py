import math
import numpy as np

# normalize 0->17 / x-axis (0->5)
def normalizeCoords(p0, px, p_ext):
    xaxis = px - p0
    xaxis /= np.linalg.norm(xaxis)
    ##
    yaxis = p_ext - p0
    yaxis /= np.linalg.norm(yaxis)
    ##
    zaxis = np.cross(xaxis, yaxis)
    zaxis /= np.linalg.norm(zaxis)
    yaxis = np.cross(zaxis, xaxis)
    yaxis /= np.linalg.norm(yaxis)
    rot = np.transpose(np.array([xaxis, yaxis, zaxis]))
    cds = coordinates(p0, rot)
    return cds

## p1<- p2 ->p3, angle(p1.p2.p3)
def calcAngle3P(p1, p2, p3, eps=1e-6):
    u = p2 - p1
    ln_u = np.linalg.norm(u)
    v = p3 - p2
    ln_v = np.linalg.norm(v)
    ##
    if ln_u < eps:
        if ln_v < eps:
            return 0.0
        else:
            return math.acos(np.dot(p2/np.linalg.norm(p2), v/ln_v))
    elif ln_v < eps:
        if ln_u < eps:
            return 0.0
        else:
            return math.acos(np.dot(u/ln_u, p2/np.linalg.norm(p2)))
    else:
        u /= ln_u
        v /= ln_v
        res = np.cross(u, v)
        ang_s = math.asin(np.linalg.norm(res))
        ang_c = math.acos(np.dot(u, v))
        #return ang_s
        sign = 1.0
        if np.dot(res, coordinates.Z) < 0:
            sign = -1.0
        return sign * ang_s

def calcAngle2Line(l1_st, l1_ed, l2_st, l2_ed, eps=1e-6):
    u = l1_ed - l1_st
    ln_u = np.linalg.norm(u)
    v = l2_ed - l2_st
    ln_v = np.linalg.norm(v)
    ##
    if ln_u < eps:
        if ln_v < eps:
            return 0.0
        else:
            return math.acos(np.dot(p2/np.linalg.norm(p2), v/ln_v))
    elif ln_v < eps:
        if ln_u < eps:
            return 0.0
        else:
            return math.acos(np.dot(u/ln_u, p2/np.linalg.norm(p2)))
    else:
        u /= ln_u
        v /= ln_v
        res = np.cross(u, v)
        ang_s = math.asin(np.linalg.norm(res))
        ang_c = math.acos(np.dot(u, v))
        sign = 1.0
        if np.dot(res, coordinates.Z) < 0:
            sign = -1.0
        return sign * ang_c

def calcAngleFromPlane(st, ed):
    vec = ed - st
    vec /= np.linalg.norm(vec)
    ang = math.acos(np.dot(vec, coordinates.Z))
    #if vec[2] > 0:
    #    pass
    #else:
    #    pass
    if math.fabs(vec[0]) > math.fabs(vec[1]):
        if vec[0] < 0:
            return math.pi - ang
    else:
        if vec[1] < 0:
            return math.pi - ang
    return ang

def setModelAngleFrom3DPoints(pt_lst, rbmodel): ## pt_lst is 3D points
    cds = normalizeCoords(pt_lst[0], pt_lst[17], pt_lst[5])
    inv = cds.inverse_transformation()
    npt_lst = [ inv.transform_vector(pt) for pt in pt_lst ]
    rbmodel.newcoords(cds)
    rbmodel.rotate(PI, coordinates.Z)
    rbmodel.rotate(-PI/2, coordinates.Y)
    #rbmodel.jointAngle('thumb0', calcAngle3P(npt_lst[0], npt_lst[1], npt_lst[2]) - PI/4)
    #rbmodel.jointAngle('thumb1', PI/2 - calcAngleFromPlane(npt_lst[1], npt_lst[2]))
    #rbmodel.jointAngle('thumb2', -calcAngle3P(npt_lst[1], npt_lst[3], npt_lst[3]))
    #rbmodel.jointAngle('thumb3', -calcAngle3P(npt_lst[2], npt_lst[3], npt_lst[4]))
    #rbmodel.jointAngle('index_finger_0', PI/12 - PI/2 + calcAngle2Line(npt_lst[5], npt_lst[17], npt_lst[5], npt_lst[6]))
    #rbmodel.jointAngle('index_finger_1', PI/2 - calcAngleFromPlane(npt_lst[6], npt_lst[5]))
    #rbmodel.jointAngle('index_finger_2', -calcAngle3P(npt_lst[5], npt_lst[6], npt_lst[7]))
    #rbmodel.jointAngle('index_finger_3', -calcAngle3P(npt_lst[6], npt_lst[7], npt_lst[8]))
    #rbmodel.jointAngle('middle_finger_0', PI/12 - PI/2 + calcAngle2Line(npt_lst[5], npt_lst[17], npt_lst[9], npt_lst[10]))
    #rbmodel.jointAngle('middle_finger_1', PI/2 - calcAngleFromPlane(npt_lst[10], npt_lst[9]))
    #rbmodel.jointAngle('middle_finger_2', -calcAngle3P(npt_lst[ 9], npt_lst[10], npt_lst[11]))
    #rbmodel.jointAngle('middle_finger_3', -calcAngle3P(npt_lst[10], npt_lst[11], npt_lst[12]))
    #rbmodel.jointAngle('ring_finger_0', PI/12 - PI/2 + calcAngle2Line(npt_lst[5], npt_lst[17], npt_lst[13], npt_lst[14]))
    #rbmodel.jointAngle('ring_finger_1', PI/2 - calcAngleFromPlane(npt_lst[14], npt_lst[13]))
    #rbmodel.jointAngle('ring_finger_2', -calcAngle3P(npt_lst[13], npt_lst[14], npt_lst[15]))
    #rbmodel.jointAngle('ring_finger_3', -calcAngle3P(npt_lst[14], npt_lst[15], npt_lst[16]))
    #rbmodel.jointAngle('pinky_0', PI/12 - PI/2 + calcAngle2Line(npt_lst[5], npt_lst[17], npt_lst[17], npt_lst[18]))
    #rbmodel.jointAngle('pinky_1', PI/2 - calcAngleFromPlane(npt_lst[18], npt_lst[17]))
    #rbmodel.jointAngle('pinky_2', -calcAngle3P(npt_lst[17], npt_lst[18], npt_lst[19]))
    #rbmodel.jointAngle('pinky_3', -calcAngle3P(npt_lst[18], npt_lst[19], npt_lst[20]))
    av = npa([
        PI/2 - calcAngleFromPlane(npt_lst[1], npt_lst[2]) ,
        -calcAngle3P(npt_lst[0], npt_lst[1], npt_lst[2]) + PI/4 ,
        -calcAngle3P(npt_lst[1], npt_lst[3], npt_lst[3]) ,
        -calcAngle3P(npt_lst[2], npt_lst[3], npt_lst[4]) ,
        PI/12 - PI/2 + calcAngle2Line(npt_lst[5], npt_lst[17], npt_lst[5], npt_lst[6]) ,
        PI/2 - calcAngleFromPlane(npt_lst[6], npt_lst[5]) ,
        -calcAngle3P(npt_lst[5], npt_lst[6], npt_lst[7]) ,
        -calcAngle3P(npt_lst[6], npt_lst[7], npt_lst[8]) ,
        PI/12 - PI/2 + calcAngle2Line(npt_lst[5], npt_lst[17], npt_lst[9], npt_lst[10]) ,
        PI/2 - calcAngleFromPlane(npt_lst[10], npt_lst[9]) ,
        -calcAngle3P(npt_lst[ 9], npt_lst[10], npt_lst[11]) ,
        -calcAngle3P(npt_lst[10], npt_lst[11], npt_lst[12]) ,
        PI/12 - PI/2 + calcAngle2Line(npt_lst[5], npt_lst[17], npt_lst[13], npt_lst[14]) ,
        PI/2 - calcAngleFromPlane(npt_lst[14], npt_lst[13]) ,
        -calcAngle3P(npt_lst[13], npt_lst[14], npt_lst[15]) ,
        -calcAngle3P(npt_lst[14], npt_lst[15], npt_lst[16]) ,
        PI/12 - PI/2 + calcAngle2Line(npt_lst[5], npt_lst[17], npt_lst[17], npt_lst[18]) ,
        PI/2 - calcAngleFromPlane(npt_lst[18], npt_lst[17]) ,
        -calcAngle3P(npt_lst[17], npt_lst[18], npt_lst[19]) ,
        -calcAngle3P(npt_lst[18], npt_lst[19], npt_lst[20]) ,
    ])
    return rbmodel.angleVector(av)
