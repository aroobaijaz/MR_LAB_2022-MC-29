import rclpy
from rclpy.node import Node
import os

class SimpleNode(Node):
    def __init__(self):
        super().__init__('simple_node')

        # --- Task 2: Persistent counter ---
        # Path to counter.txt (in same folder as this script)
        script_path = os.path.dirname(os.path.realpath(__file__))
        counter_file = os.path.join(script_path, 'counter.txt')

        # Read current counter
        try:
            with open(counter_file, 'r') as f:
                count = int(f.read().strip())
        except:
            count = 0  # initialize if file doesn't exist

        count += 1  # increment

        # Save updated counter
        with open(counter_file, 'w') as f:
            f.write(str(count))

        self.get_logger().info(f"Run count: {count}")

def main(args=None):
    rclpy.init(args=args)
    node = SimpleNode()
    rclpy.spin_once(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
