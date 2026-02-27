 ROS2 Lab Answers

1. Definitions

Node:  
A node is an executable program in ROS2 that performs a specific task, such as publishing or subscribing to data.

Topic:  
A topic is a named communication channel used by nodes to exchange messages asynchronously.

Package:  
A package is an organized folder that contains ROS2 code, configuration files, and dependencies needed for a specific functionality.

Workspace:

A workspace is a directory that contains one or more ROS2 packages and allows them to be built and managed together.

2. Why is Sourcing Required?

Sourcing (using `source install/setup.bash`) updates the terminal environment so ROS2 can find the packages and executables in your workspace.

If you do not source the workspace, ROS2 will not recognize your package, and commands like `ros2 run my_first_pkg simple_node` will fail with "package not found" or "executable not found".

 3. Purpose of `colcon build`

`colcon build` compiles and builds all packages in a workspace so they can be executed in ROS2.

It generates three main folders:

- **build/** – Contains build files and intermediate compilation data  
- **install/** – Contains installed executables and setup files  
- **log/** – Contains build log files  

4. Purpose of entry_points in setup.py

The `entry_points` console script links a terminal command (like `ros2 run my_first_pkg simple_node`) to the Python file and its `main()` function so ROS2 knows which node to execute.

 5. Publisher-subscriber
[Publisher Node] ---> (/topic_name) ---> [Subscriber Node]
