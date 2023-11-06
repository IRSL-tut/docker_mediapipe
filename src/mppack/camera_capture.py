import cv2
import numpy as np
import time

class CvCapture(object):
    def __init__(self, camID=0, width=800, height=600, buffersize=1):
        """
        """
        self.zero_dist = np.array([0, 0, 0, 0, 0], dtype='float64')
        self.zero3 = np.array([0, 0, 0], dtype='float64')
        ##
        if camID >= 0:
            self.cap = cv2.VideoCapture(camID)   # カメラのID指定
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, buffersize)
            self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')) ## BGR3??
            self.setSize(width=width, height=height)
        else:
            self.width=width
            self.height=height
        ##
        self.mapxy = None

    def set_camera_parameters(self, distortion=None, camera_matrix=None, projection_matrix=None, new_camera_matrix=None):
        """Setting camera parameters

        Args:
            distortion (numpy.array, optional) : 1x5 vector, distortion parameters
            camera_matrix (numpy.array, optional) : 3x3 matrix, camera original matrix
            projection_matrix (numpy.array, optional) : 3x4 matrix, projection matrix of undistorted image
            new_camera_matrix (numpy.array, optional) : 3x3 matrix, camera matrix of undistorted image
        """
        self.distortion = distortion
        self.camera_matrix = camera_matrix
        self.projection_matrix = projection_matrix
        if new_camera_matrix is not None:
            self.new_camera_matrix = new_camera_matrix
        elif self.projection_matrix is not None:
            self.new_camera_matrix = self.projection_matrix[:3,:3]
        if self.camera_matrix is not None and self.distortion is not None and self.new_camera_matrix is not None:
            self.mapxy = cv2.initUndistortRectifyMap(self.camera_matrix, self.distortion, None,
                                                     self.new_camera_matrix, (self.width, self.height), cv2.CV_32FC1)

    def undistort_points(self, points):
        """Undistorting points on image

        Args:
            points ( list[numpy.array] ) : list of 2D points on original image

        Retuns:
            numpy.array : 2D points in undistorted image
        """
        return cv2.undistortPoints(np.array(points), self.camera_matrix, self.distortion, P=self.new_camera_matrix)

    def undistort_image(self, img):
        """Generating undistorted image

        Args:
            img ( numpy.array ) : Original image
        Retuns:
            numpy.array : Undistorted image

        """
        if self.mapxy is not None:
            return cv2.remap(img, self.mapxy[0], self.mapxy[1], cv2.INTER_AREA)

    def project_points(self, points):
        """Projecting 3D points to the original image plane

        Args:
            points( list [numpy.array] ) : List of 3D points (camera coordinates)

        Retuns:
            numpy.array : Projected 2D points
        """
        if self.camera_matrix is not None and self.distortion is not None:
            return cv2.projectPoints(np.array(points), self.zero3, self.zero3, self.camera_matrix, self.distortion)

    def project_points_new(self, points):
        """Projecting 3D points to undistorted image plane

        Args:
            points( list [numpy.array] ) : List of 3D points (camera coordinates)

        Retuns:
            numpy.array : Projected 2D points
        """
        if self.new_camera_matrix is not None:
            return cv2.projectPoints(points, self.zero3, self.zero3, self.new_camera_matrix, self.zero_dist)

    def unproject_points(self, uv_list, depth=1.0, depth_list=None):
        """Unproject 2D points to 3D points using given depth

        Args:
            uv_list ( list[numpy.array] ) : List of 2D points (undistorted image plane)
            depth (float, default=1.0) : Depth for using unproject
            depth_list (list[float], optional) : Depth for using unproject, corresponding to each point
        """
        cmat = self.new_camera_matrix
        fx = cmat[0][0]
        fy = cmat[1][1]
        cx = cmat[0][2]
        cy = cmat[1][2]
        if depth_list is None:
            return [ np.array([(pt[0] - cx)*depth/fx, (pt[1] - cy)*depth/fy, depth]) for pt in uv_list ]
        else:
            return [ np.array([(pt[0] - cx)*dp/fx, (pt[1] - cy)*dp/fy, dp]) for pt, dp in zip(uv_list, depth_list) ]

    def setSize(self, width=800, height=600):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,  width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.width=int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height=int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def isOpened(self):
        return self.cap.isOpened()

    def close(self):
        self.cap.release()

    def capture(self, delay=None, size=None, flip=False, grab=True):
        """Capturing camera image

        Args:
            delay (float, optional) :
            size ( tuple[int], optional) : resize (width, height)
            flip (bool, default=False) :
            grab (bool, default=True) :

        Retuns:
            numpy.array : Image of OpenCV python-binding
        """
        if delay is not None:
            time.sleep(delay)

        if self.cap.isOpened():
            if grab:
                self.cap.grab()
                success, img = self.cap.read()
            # カメラから画像取得
            success, img = self.cap.read()
            if not success:
                return None

            if size is not None:
                img = cv2.resize(img, size) # リサイズ
            if flip:
                img = cv2.flip(img, 1)      # 画像を左右反転

            return img

    def show(self, img, wait=10, title='IRSLCap', flip=False):
        if flip:
            img = cv2.flip(img, 1)      # 画像を左右反転
        cv2.imshow(title, img)
        key = cv2.waitKey(wait)
        return key
