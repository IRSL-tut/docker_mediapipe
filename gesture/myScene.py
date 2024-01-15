exec(open('/home/irsl/sandbox/choreonoid_ws/install/share/irsl_choreonoid/sample/irsl_import.py').read())
basedir='/home/irsl/src/docker_mediapipe'
exec(open(basedir+'/src/cnoid_samples/create_scene.py').read())

fname = basedir + '/models/JVRC-1/main.wrl'
rb = ib.loadRobotItem(fname, world=False) ## in choreonoid GUI
robot = RobotModel(rb)

gdir=basedir + '/gesture'
lstneck = [(gdir + "/data0000.pyc", 0.15),
           (gdir + "/data0001.pyc", 0.15),
           (gdir + "/data0002.pyc", 0.15),
           (gdir + "/data0003.pyc", 0.15),
           (gdir + "/data0004.pyc", 0.15),
           (gdir + "/data0005.pyc", 0.15),
           (gdir + "/data0006.pyc", 0.15),
           (gdir + "/data0000.pyc", 0.15)]

lstwalk = [(gdir + "/data0020.pyc", 0.1),
           (gdir + "/data0014.pyc", 0.1),
           (gdir + "/data0015.pyc", 0.1),
           (gdir + "/data0016.pyc", 0.1),
           (gdir + "/data0015.pyc", 0.1),
           (gdir + "/data0014.pyc", 0.1),
           (gdir + "/data0020.pyc", 0.1),
           (gdir + "/data0017.pyc", 0.1),
           (gdir + "/data0018.pyc", 0.1),
           (gdir + "/data0019.pyc", 0.1),
           (gdir + "/data0018.pyc", 0.1),
           (gdir + "/data0017.pyc", 0.1),
           (gdir + "/data0020.pyc", 0.1),
           (gdir + "/data0014.pyc", 0.1),
           (gdir + "/data0015.pyc", 0.1),
           (gdir + "/data0016.pyc", 0.1),
           (gdir + "/data0015.pyc", 0.1),
           (gdir + "/data0014.pyc", 0.1),
           (gdir + "/data0020.pyc", 0.1),
           (gdir + "/data0017.pyc", 0.1),
           (gdir + "/data0018.pyc", 0.1),
           (gdir + "/data0019.pyc", 0.1),
           (gdir + "/data0018.pyc", 0.1),
           (gdir + "/data0017.pyc", 0.1),
           (gdir + "/data0020.pyc", 0.1)]

lstbow = [(gdir + "/data0020.pyc", 0.3),
          (gdir + "/data0021.pyc", 0.3),
          (gdir + "/data0022.pyc", 0.3),
          (gdir + "/data0021.pyc", 0.3),
          (gdir + "/data0020.pyc", 0.3)]

lstRhand = [(gdir + "/data0020.pyc", 0.15),
            (gdir + "/data0023.pyc", 0.15),
            (gdir + "/data0024.pyc", 0.15),
            (gdir + "/data0025.pyc", 0.15),
            (gdir + "/data0024.pyc", 0.15),
            (gdir + "/data0023.pyc", 0.15),
            (gdir + "/data0020.pyc", 0.15)]

lstLhand = [(gdir + "/data0020.pyc", 0.15),
            (gdir + "/data0026.pyc", 0.15),
            (gdir + "/data0027.pyc", 0.15),
            (gdir + "/data0028.pyc", 0.15),
            (gdir + "/data0027.pyc", 0.15),
            (gdir + "/data0026.pyc", 0.15),
            (gdir + "/data0020.pyc", 0.15)]

lstsquat = [(gdir + "/data0009.pyc", 0.5),
            (gdir + "/data0010.pyc",0.5),
            (gdir + "/data0011.pyc",0.5),
            (gdir + "/data0012.pyc",0.5),
            (gdir + "/data0011.pyc",0.5),
            (gdir + "/data0012.pyc",0.5),
            (gdir + "/data0011.pyc",0.5),
            (gdir + "/data0010.pyc",0.5),
            (gdir + "/data0009.pyc",0.5)]

lstnod = [(gdir + "/data0020.pyc", 0.15),
          (gdir + "/data0032.pyc",0.15),
          (gdir + "/data0033.pyc",0.15),
          (gdir + "/data0034.pyc",0.15),
          (gdir + "/data0033.pyc",0.15),
          (gdir + "/data0032.pyc",0.15),
          (gdir + "/data0020.pyc",0.15)]

lstarm = [(gdir + "/data0029.pyc",0.15),
          (gdir + "/data0030.pyc",0.15),
          (gdir + "/data0031.pyc",0.15),
          (gdir + "/data0030.pyc",0.15),
          (gdir + "/data0029.pyc",0.15),
          (gdir + "/data0020.pyc",0.15)]

def robot_gesture(gesture_name, robot=None):
   ges = gesture_name.lower()
   if ges == 'neck':
      moveRobot(lstneck, robot=robot)
   elif ges == 'walk':
      moveRobot(lstwalk, robot=robot)
   elif ges == 'bow':
      moveRobot(lstbow, robot=robot)
   elif ges == 'rhand':
      moveRobot(lstRhand, robot=robot)
   elif ges == 'lhand':
      moveRobot(lstLhand, robot=robot)
   elif ges == 'squat':
      moveRobot(lstsquat, robot=robot)
   elif ges == 'nod':
      moveRobot(lstnod, robot=robot)
   elif ges == 'arm':
      moveRobot(lstarm, robot=robot)
