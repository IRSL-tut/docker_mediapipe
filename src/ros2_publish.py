
# source /opt/ros/galactic/setup.bash
# export ROS_DOMAIN_ID=31
# export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
# sudo apt install ros-galactic-ros-core
# sudo apt install ros-galactic-rmw-fastrtps-cpp

# ROS_DOMAIN_ID=31 RMW_IMPLEMENTATION=rmw_fastrtps_cpp python3 ros2_publish.py

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

#rclpy.init(args=None)
#node=Node('hogehoge')
#node.publisher_ = node.create_publisher(String, 'action', 10)
#action_str = String()
#action_str.data = 'key'

### ROS2 version
class action_trigger(Node):
   def __init__(self, **kwargs):
       rclpy.init(args=None, **kwargs)
       super().__init__('action_trriger')
       # rospy.init_node('action_trriger') # ノードの生成
       # self.pub = rospy.Publisher('action', String, queue_size=10) # chatterという名前のTopicを生成し型やらを定義
       self.publisher_ = self.create_publisher(String, 'action', 10)
       #self.rate = rospy.Rate(100) # 10Hzで動かすrateというクラスを生成
       print("Conection started...")
   def trigger(self, key):
       ##
       # action_str = String() # Stringというクラスで送信するメッセージ、"hello_str"を生成
       # timestamp = rospy.get_time()
       # time = datetime.fromtimestamp(timestamp) # ここらへんはROSと関係ないです
       # action_str.data = key # 内容の書き込み
       # self.pub.publish(action_str) # hello_strを送信！
       # self.rate.sleep() # 先程定義したrateをここで動かす
       ##
       action_str = String() # Stringというクラスで送信するメッセージ、"hello_str"を生成
       action_str.data = key # 内容の書き込み
       self.publisher_.publish(action_str)
