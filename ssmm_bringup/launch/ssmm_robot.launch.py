from launch import LaunchDescription
from launch.actions import RegisterEventHandler, DeclareLaunchArgument,IncludeLaunchDescription
from launch.event_handlers import OnProcessExit
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():

    arg_show_rviz = DeclareLaunchArgument(
        "start_rviz",
        default_value="false",
        description="start RViz automatically with the launch file",
    )

    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution(
                [FindPackageShare("ssmm_robot_description"), "urdf", "ssmm_robot.urdf.xacro"]
            ),
        ]
    )

    robot_description = {"robot_description": robot_description_content}


    ssmm_robot_diff_drive_controllers = PathJoinSubstitution(
        [
            FindPackageShare("ssmm_bringup"),
            "config",
            "ssmm_robot_controller.yaml",
        ]
    )
    
    robot_state_pub_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[robot_description],
        remappings=[
            ("/ssmm_base_controller/cmd_vel_unstamped", "/cmd_vel"),
        ],
    )

    control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[robot_description, ssmm_robot_diff_drive_controllers],
        output={
            "stdout": "screen",
            "stderr": "screen",
        },
    )

    spawn_dd_controller = Node(
        package="controller_manager",
        executable="spawner.py",
        arguments=["ssmm_base_controller"],
        output="screen",
    )

    spawn_jsb_controller = Node(
        package="controller_manager",
        executable="spawner.py",
        arguments=["joint_state_broadcaster"],
        output="screen",
    )

    rviz_config_file = PathJoinSubstitution(
        [FindPackageShare("ssmm_robot_description"), "config", "ssmm_robot.rviz"]
    )
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_config_file],
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
    )

    robot_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["ssmm_base_controller", "-c", "/controller_manager"],
    )

    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher'
    )

    # joint_state_publisher_gui_node = Node(
    #     package='joint_state_publisher_gui',
    #     executable='joint_state_publisher_gui',
    #     name='joint_state_publisher_gui'
    # )

    # Delay rviz start after `joint_state_broadcaster`
    delay_rviz_after_joint_state_broadcaster_spawner = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=joint_state_broadcaster_spawner,
            on_exit=[rviz_node],
        )
    )

    # Delay start of robot_controller after `joint_state_broadcaster`
    delay_robot_controller_spawner_after_joint_state_broadcaster_spawner = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=joint_state_broadcaster_spawner,
            on_exit=[robot_controller_spawner],
        )
    )

    gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('gazebo_ros'),
                'launch',
                'gzserver.launch.py'
            ])
        ]),
        launch_arguments={
            'pause': 'true'
        }.items()
    )
    gazebo_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('gazebo_ros'),
                'launch',
                'gzclient.launch.py'
            ])
        ])
    )

    urdf_spawn_node = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'ssmm_robot',
            '-topic', 'robot_description',
            '-x', str(0),
            '-y', str(0),
            '-z',str(0.1),
            '-R', str(0),
            '-P', str(0),
            '-Y', str(0)
        ],
        output='screen'
    )

    nodes = [
        arg_show_rviz,
        robot_state_pub_node,
        joint_state_publisher_node,
        # joint_state_publisher_gui_node,
        spawn_dd_controller,
        # spawn_jsb_controller,
        delay_rviz_after_joint_state_broadcaster_spawner,
        delay_robot_controller_spawner_after_joint_state_broadcaster_spawner,
        rviz_node,
        control_node,
        # gazebo_server,
        # gazebo_client,
        # urdf_spawn_node,
    ]

    return LaunchDescription(nodes)