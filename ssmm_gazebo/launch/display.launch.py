#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory

import launch
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

import xacro


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    package_name = "ssmm_gazebo"
    robot_file = "ssmm_gazebo.urdf"
    world_file_name = "gcamp_world.world"

    #rviz_file = "test.rviz"
    pkg_path = os.path.join(get_package_share_directory(package_name))
    pkg_gazebo_ros = FindPackageShare(package='gazebo_ros').find('gazebo_ros')  

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(get_package_share_directory("gazebo_ros"), "launch"),
                "/gazebo.launch.py",
            ]
        ),
    )

    urdf_file = os.path.join(get_package_share_directory(package_name), "urdf", robot_file)
    world_path = os.path.join(pkg_path, "worlds", world_file_name)

    # rviz = os.path.join(get_package_share_directory(package_name), "rviz", rviz_file)

    # Start Gazebo server
    start_gazebo_server_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py'))
        # launch_arguments={'world': world_path}.items()
    )

    # Start Gazebo client    
    start_gazebo_client_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py'))
    )

    xml = open(urdf_file, "r").read()
    xml = xml.replace('"', '\\"')

    xacro_file = os.path.join(
        get_package_share_directory(package_name), "urdf_file", robot_file
    )
    doc = xacro.parse(open(urdf_file))
    xacro.process_doc(doc)
    robot_description = {'robot_description': doc.toxml()}


    # node_robot_state_publisher = Node(
    #     package="robot_state_publisher",
    #     executable="robot_state_publisher",
    #     output="screen",
    #     parameters=[params],
    # )

    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'use_sim_time': use_sim_time, 'robot_description': robot_desc}],
        arguments=[urdf_file],
        # parameters=[{'robot_description': Command(['xacro ', LaunchConfiguration('model')])}]
    )

    # joint_state_publisher_node = Node(
    #     package='joint_state_publisher',
    #     executable='joint_state_publisher',
    #     name='joint_state_publisher',
    #     condition=launch.conditions.UnlessCondition(LaunchConfiguration('gui'))
    # )

    # joint_state_publisher_gui_node = Node(
    #     package='joint_state_publisher_gui',
    #     executable='joint_state_publisher_gui',
    #     name='joint_state_publisher_gui',
    #     condition=launch.conditions.IfCondition(LaunchConfiguration('gui'))
    # )

    # rviz_node = Node(
    #     package='rviz2',
    #     executable='rviz2',
    #     name='rviz2',
    #     arguments=['-d', LaunchConfiguration('rvizconfig')],
    # )

    spawn_entity = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=["-topic", "robot_description", "-entity", "ssmm"],
        output="screen",
    )

    return LaunchDescription(
        [
            # DeclareLaunchArgument(name='gui', default_value='True',
            #                             description='Flag to enable joint_state_publisher_gui'),
            # DeclareLaunchArgument(name='rvizconfig', default_value=rviz,
            #                             description='Absolute path to rviz config file')
            start_gazebo_server_cmd,
            start_gazebo_client_cmd,
            robot_state_publisher_node,
            #joint_state_publisher_node,
            # joint_state_publisher_gui_node,
            # rviz_node,
            # gazebo,
            spawn_entity,
        ]
    )
