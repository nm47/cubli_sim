from ament_index_python.packages import get_package_share_path
from ament_index_python.packages import get_package_share_directory

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import Command, LaunchConfiguration

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    package_path = get_package_share_path('cubli_description')
    default_cubli_xacro = os.path.join(package_path, 'model/xacro/cubli.xacro')
    default_rviz_config = os.path.join(package_path,'config/cubli.rviz')

    cubli_xacro = DeclareLaunchArgument(name='cubli_xacro', default_value=str(default_cubli_xacro),
                                 description='Absolute path to cubli xacro file')
    rviz_config = DeclareLaunchArgument(name='rviz_config', default_value=str(default_rviz_config),
                                     description='Absolute path to rviz config file')
    robot_description = ParameterValue(Command(['xacro ', LaunchConfiguration('cubli_xacro')]),
                                       value_type=str)
    publisher_gui = DeclareLaunchArgument(name='publisher_gui', default_value="False",
                                 description='Whether to use the robot state publisher gui')


    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}]
    )

    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        condition=UnlessCondition(LaunchConfiguration('publisher_gui'))
    )

    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        condition=IfCondition(LaunchConfiguration('publisher_gui'))
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', LaunchConfiguration('rviz_config')],
    )

    return LaunchDescription([
        publisher_gui,
        cubli_xacro,
        rviz_config,
        joint_state_publisher_gui_node,
        joint_state_publisher_node,
        robot_state_publisher_node,
        rviz_node
    ])
