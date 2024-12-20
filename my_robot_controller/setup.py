from setuptools import find_packages, setup

package_name = 'my_robot_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),  # Exclude test folder if needed
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/spawn_robot.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jojodido',
    maintainer_email='jojodido@todo.todo',
    description='Description of the robot controller package',  # Provide a proper description
    license='TODO: License declaration',  # Replace with actual license if possible
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # Ensure that these functions are defined in the corresponding files
            "test_node = my_robot_controller.first_node:main",
            "drawcircle = my_robot_controller.draw_circle:main",
            "pose_sub = my_robot_controller.pose_sub:main",
        ],
    },
)
