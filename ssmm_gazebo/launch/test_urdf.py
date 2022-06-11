import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():

    print("============1==============")
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    urdf_file_name = 'urdf/ssmm_gazebo.urdf'
    print("============2==============")
    urdf = os.path.join(
    get_package_share_directory('ssmm_gazebo'), # Changed package name
    urdf_file_name)
    print("============3==============")
    print("urdf :", urdf)

    with open(urdf, 'r') as infp:
        robot_desc = infp.read()
    print("============4==============")
    print("robot_desc :", robot_desc)
    return LaunchDescription([
    DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation (Gazebo) clock if true'),
    Node(
        package=    'robot_state_publisher',
        executable= 'robot_state_publisher',
        name=       'robot_state_publisher',
        output=     'screen',
        parameters=[{'use_sim_time': use_sim_time, 'robot_description': robot_desc}],
        arguments=[urdf]),
    # Node(
    #   package=    'ros2_tutorial_urdf', # Changed package name
    #   executable= 'r2d2_state_publisher',
    #   name=       'state_publisher',
    #   output=     'screen'),
    ])