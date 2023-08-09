from ament_index_python.packages import get_package_share_path
from ament_index_python.packages import get_package_share_directory

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    package_path = get_package_share_path('cubli_description')
    default_cubli_xacro = os.path.join(package_path, 'model/xacro/cubli.xacro')

    cubli_xacro = DeclareLaunchArgument(name='cubli_xacro', default_value=str(default_cubli_xacro),
                                 description='Absolute path to cubli xacro file')
    robot_description = ParameterValue(Command(['xacro ', LaunchConfiguration('cubli_xacro')]),
                                       value_type=str)
    
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}]
    )

    return LaunchDescription([
        cubli_xacro,
        robot_state_publisher_node,
    ])
