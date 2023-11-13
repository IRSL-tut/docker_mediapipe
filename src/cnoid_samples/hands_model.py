##
## using calibration parameters
##
exec(open('/choreonoid_ws/install/share/irsl_choreonoid/sample/irsl_import.py').read())
itm_ = ib.loadRobotItem('models/HandModel.body')
rb = RobotModel(itm_)

### set parameter from calibration (not required)
camera_matrix = np.array([[630.408201, 0.000000, 408.395562],
                          [0.000000, 628.574130, 296.839336],
                          [0.000000, 0.000000, 1.000000]], dtype='float64')
distortion = np.array([0.018656, 0.034678, 0.002943, -0.004527, 0.000000], dtype='float64')
projection_matrix = np.array([[647.145834, 0.000000, 404.360305, 0.000000],
                              [0.000000, 647.276761, 298.733318, 0.000000],
                              [0.000000, 0.000000, 1.000000, 0.000000]], dtype='float64')
#
cap = camera_capture.CvCapture(0) ## create instance without opening camera device
cap.set_camera_parameters(camera_matrix=camera_matrix, distortion=distortion, projection_matrix=projection_matrix)

img_und = cap.undistort_image(img) ## undistort image

pose_recog = mp_pose.MPPose(max_num_poses=1, running_mode='IMAGE')
pose_recog.set_image(img_und)

lmarks = pose_recog.get_landmarks()

uv_points = lmarks[0]
depth_list = [ p[2] for p in lmarks[0] ]

3dpoints = cap.unproject_points(up_points, depth_list)

### cnoid_samples/calc_angle.py

setModelAngleFrom3Dpoints(3dpoints, rb)
