import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import time

class mysubscriber(Node):
    def __init__(self, _nodename, **kwargs):
        Node.__init__(self, _nodename, **kwargs)
    def callback(self, msg):
        # print(self)
        # print(msg)
        print('sub: ' +  msg.data)
        robot_gesture(msg.data, self.robot)
    def sub(self):
        self.subscription = self.create_subscription(String, 'action', self.callback, 10)

basedir='/home/irsl/src/docker_mediapipe'
exec(open(basedir+'/gesture/myScene.py').read())

rclpy.init(args=None)

sub=mysubscriber('mysubscriber')
sub.robot = robot
sub.sub()

while rclpy.ok():
    rclpy.spin_once(sub, timeout_sec=0.0001)
    time.sleep(0.01)
