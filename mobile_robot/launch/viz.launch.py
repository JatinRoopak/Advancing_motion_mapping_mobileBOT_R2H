import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time')
    
    # Process the URDF file
    pkg_path = os.path.join(get_package_share_directory('mobile_robot'))
    xacro_file = os.path.join(pkg_path, 'description', 'robot.urdf.xacro')
    print(f"Xacro file path: {xacro_file}")
    robot_description_config = xacro.process_file(xacro_file)
    
    # Create a robot_state_publisher node
    params = {'robot_description': robot_description_config.toxml(), 'use_sim_time': use_sim_time}
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )

    # Include the Gazebo launch file
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
    )

    gazebo = IncludeLaunchDescription(
    PythonLaunchDescriptionSource([os.path.join(
        get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
    launch_arguments={
        'world': os.path.join(pkg_path, 'worlds', 'museum.world'),
        'verbose': 'true'
    }.items()
    )

    # Node to spawn the robot in Gazebo
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description',
                  '-entity', 'robot'],
        output='screen'
    )

    # # Optional: Add joint_state_publisher_gui
    # joint_state_publisher_gui = Node(
    #     package='joint_state_publisher_gui',
    #     executable='joint_state_publisher_gui',
    #     name='joint_state_publisher_gui'
    # )

    # Launch!
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',  # Changed to true since we're using Gazebo
            description='Use sim time if true'),
        gazebo,
        node_robot_state_publisher,
        spawn_entity,
        #joint_state_publisher_gui
    ])