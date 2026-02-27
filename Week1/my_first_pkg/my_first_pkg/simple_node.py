import rclpy
from rclpy.node import Node

class SimpleNode(Node):
    def __init__(self):
        super().__init__('simple_node')

        # --- Task 3: student_name parameter ---
        self.declare_parameter('AROOBA IJAZ', '')

        name = self.get_parameter('student_name').value
        if name:
            self.get_logger().info(f"Student Name: {name}")
        else:
            self.get_logger().info("student_name not set")

def main(args=None):
    rclpy.init(args=args)
    node = SimpleNode()
    rclpy.spin_once(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
