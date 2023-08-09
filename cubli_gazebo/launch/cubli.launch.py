from ament_index_python.packages import get_package_share_path
from ament_index_python.packages import get_package_share_directory

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import Command, LaunchConfiguration

from launch_ros.actions import Node, PushRosNamespace
from launch_ros.parameter_descriptions import ParameterValue
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    cubli_xacro = os.path.join(get_package_share_path('cubli_gazebo'), 'xacro/cubli.xacro')
    gazebo_params_path = os.path.join(get_package_share_path('cubli_gazebo'), 'config/gazebo.yaml')
    gazebo_world = os.path.join(get_package_share_path('cubli_gazebo'), 'worlds/flat.world')
    robot_description = ParameterValue(Command(['xacro ', LaunchConfiguration('cubli_xacro')]),
                                       value_type=str)

    return LaunchDescription([
        DeclareLaunchArgument(name='gazebo_world', default_value=str(gazebo_world),
            description='Abxolute path to gazebo world file'),

        DeclareLaunchArgument(name='rviz', default_value='false',
            description='Launch rviz as well as gazebo'),

        Node(package='gazebo_ros', executable='spawn_entity.py',
            arguments=['-topic', 'robot_description',
                '-entity', 'cubli', '-R 0.785398 ', '-z 0.054' ],
            output='screen'),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory('cubli_description'), 'launch'), '/cubli_description.launch.py']),
            launch_arguments = {'cubli_xacro': cubli_xacro}.items()
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory('gazebo_ros'), 'launch'), '/gazebo.launch.py']),
            launch_arguments = {'world': gazebo_world, 'pause':'true', 'extra_gazebo_args': '--ros-args --params-file ' + gazebo_params_path }.items()
        ),
        Node(
            package="controller_manager",
            executable="spawner",
            arguments=["joint_state_controller"],
            output='screen'
            ),
        Node(
            package="controller_manager",
            executable="spawner",
            arguments=["flywheel_velocity_controller"],
            output='screen'
            )
    ])
