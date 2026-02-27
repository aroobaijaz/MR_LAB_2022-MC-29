

1. Brief Description of Week 1 Lab

The purpose of this lab was to onboard students to the Linux environment and the ROS 2 (Humble) framework. Key objectives included setting up a dedicated ROS 2 development workspace (~/ros2_ws), creating a Python-based ROS 2 package (my_first_pkg), and developing a basic node (simple_node) that logs messages to the terminal.
2. Commands Used

Throughout the lab, the following primary commands were utilized:
Linux Navigation & File Management

    pwd: Print the current working directory.

    ls -l: List files in the current directory with detailed information.

    mkdir -p ~/ros2_ws/src: Create the workspace and source directory structure.

    chmod +x <file_path>: Make the Python node file executable.

ROS 2 & Build Commands

    source /opt/ros/humble/setup.bash: Source the global ROS 2 Humble environment.

    colcon build: Build the packages within the workspace.

    source install/setup.bash: Source the local workspace so ROS 2 can locate built packages.

    ros2 pkg create --build-type ament_python my_first_pkg: Create a new Python-based ROS 2 package.

    ros2 run my_first_pkg simple_node: Execute the developed node.
3. Problems Faced and Solutions
Problem	:	
ros2: command not found	
cause:
ROS 2 environment not sourced in the current terminal.
solution:	
Run source /opt/ros/humble/setup.bash.
Problem:
colcon: command not found	
Cause:
The colcon build tool is not installed.
solution:	
Install it using sudo apt install python3-colcon-common-extensions.
problem:
Package not found	
cause:
Workspace not sourced or build failed.
solution:	
Re-run colcon build and source install/setup.bash.
problem:
Executable not found	
cause:
Entry point not correctly registered in setup.py.
solution:	
Verify the console_scripts line in setup.py and rebuild.
REFLECTION:
"Participating in the Week 1 Mobile Robotics lab has been an engaging introduction to the ROS 2 Humble ecosystem. While transitioning to a terminal-centric workflow presented an initial learning curve, the process of building and sourcing a workspace provided a fundamental understanding of how distributed robotic software is organized. I encountered several environment-related errors, such as 'command not found' due to sourcing issues, but resolving these through the troubleshooting protocols helped solidify my grasp of the Linux environment. The experience of successfully registering an entry point in setup.py and seeing the node execute was highly rewarding. Overall, this lab underscored the importance of workspace management and academic persistence in developing robust robotic systems."
