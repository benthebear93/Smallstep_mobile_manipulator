import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

import xacro

# this is the function launch  system will look for
def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    urdf_file_name = "ssmm_gazebo.urdf"
    print("urdf file name : {}".format(urdf_file_name))

    urdf_file = os.path.join(
        get_package_share_directory('ssmm_description'), 
        "urdf", 
        urdf_file_name)

    # Robot State Publisher
    doc = xacro.parse(open(urdf_file))
    xacro.process_doc(doc)
    robot_description_params = {'robot_description': doc.toxml()}

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description_params]
    )

    return LaunchDescription(
        [
            robot_state_publisher_node,
        ]
    )
