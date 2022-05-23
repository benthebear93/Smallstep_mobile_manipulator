import os
from ament_index_python.packages import get_package_share_path
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.actions import ExecuteProcess, IncludeLaunchDescription, TimerAction
from launch.substitutions import Command, LaunchConfiguration

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    rviz_file = "skidbot.rviz"
    package_name = "ssmm_gazebo"
    robot_file = "3dof.urdf"

    pkg_path = get_package_share_path('ssmm_gazebo')
    default_model_path = pkg_path / 'urdf/3dof.urdf'
    default_rviz_config_path = pkg_path / 'rviz/urdf.rviz'

    # gui_arg = DeclareLaunchArgument(name='gui', default_value='true', choices=['true', 'false'],
    #                                 description='Flag to enable joint_state_publisher_gui')
    # model_arg = DeclareLaunchArgument(name='model', default_value=str(default_model_path),
    #                                   description='Absolute path to robot urdf file')
    urdf = os.path.join(get_package_share_directory(package_name), "urdf", robot_file)
    rviz_config = os.path.join(pkg_path, "rviz", default_rviz_config_path)
    
    robot_desc = open(urdf, "r").read()

    # double quotes need to be with escape sequence
    xml = robot_desc.replace('"', '\\"')

    # this is argument format for spwan_entity service
    spwan_args = '{name: "skidbot", xml: "' + xml + '" }'
    
    # robot_description = ParameterValue(Command(['xacro ', LaunchConfiguration('model')]),
    #                                    value_type=str)

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
         parameters=[{'use_sim_time': use_sim_time, 'robot_description': robot_desc}],
        arguments=[urdf],
    )


    # # Depending on gui parameter, either launch joint_state_publisher or joint_state_publisher_gui
    # joint_state_publisher_node = Node(
    #     package='joint_state_publisher',
    #     executable='joint_state_publisher',
    #     condition=UnlessCondition(LaunchConfiguration('gui'))
    # )

    # joint_state_publisher_gui_node = Node(
    #     package='joint_state_publisher_gui',
    #     executable='joint_state_publisher_gui',
    #     condition=IfCondition(LaunchConfiguration('gui'))
    # )

    # rviz_node = Node(
    #     package='rviz2',
    #     executable='rviz2',
    #     name='rviz2',
    #     output='screen',
    #     arguments=['-d', LaunchConfiguration('rviz_config')],
    # )
    rviz_start = ExecuteProcess(
        cmd=["ros2", "run", "rviz2", "rviz2", "-d", rviz_config], output="screen"
    )
    return LaunchDescription([
        # gui_arg,
        # model_arg,
        # rviz_arg,
        # joint_state_publisher_node,
        # joint_state_publisher_gui_node,
        # robot_state_publisher_node,
        rviz_start
    ])

    return LaunchDescription(
        [
            # robot state publisher allows robot model spawn in RVIZ
            robot_state_publisher_node,
            # start gazebo, notice we are using libgazebo_ros_factory.so instead of libgazebo_ros_init.so
            # That is because only libgazebo_ros_factory.so contains the service call to /spawn_entity
            ExecuteProcess(
                cmd=["gazebo", "--verbose", world, "-s", "libgazebo_ros_factory.so"],
                output="screen",
            ),
            # tell gazebo to spwan your robot in the world by calling service
            ExecuteProcess(
                cmd=[ "ros2", "service", "call", "/spawn_entity", "gazebo_msgs/SpawnEntity", spwan_args ],
                output="screen",
            ),
            rviz_start
        ]
    )