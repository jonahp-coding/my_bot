import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

def generate_launch_description():

    # Include the robot_state_publisher launch file, provided by our own packages. Force sim timw to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    package_name='my_bot'

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name), 'launch', 'rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    # Include the Gazebo launch file, provided by the ros_gz_sim package
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')]),
                    launch_arguments={'gz_args': ['-r -v4 ', '/home/ubuntu/dev_ws/src/my_bot/worlds/empty.world'], 'on_exit_shutdown': 'true'}.items()
             )

    # Run the spawner node from te ros_gz_sim_package. The entity name doesn't really matter if you only have...
    spawn_entity = Node(package='ros_gz_sim', executable='create',
                        arguments=['-topic', 'robot_description',
                                   '-name', 'jonah_bot',
                                   '-z', '0.1'],
                        output='screen')
    
    # Launch them all!
    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity,
    ])
