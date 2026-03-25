import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.srv import TeleportAbsolute
from turtlesim.msg import Pose
import math
import time


class GoToGoalTurtle(Node):
    def __init__(self):
        super().__init__('go_to_goal_turtle')

        # ── Publisher for turtle1 ──────────────────────────────────────────
        self.pub = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)

        # ── Pose subscriber ────────────────────────────────────────────────
        self.current_pose = None
        self.create_subscription(Pose, 'turtle1/pose', self.pose_callback, 10)

        # ── Teleport service (fallback if pose unavailable) ────────────────
        self.teleport_client = self.create_client(
            TeleportAbsolute, '/turtle1/teleport_absolute'
        )
        self.get_logger().info('Waiting for teleport service...')
        self.teleport_client.wait_for_service(timeout_sec=5.0)

        # ── Controller gains ───────────────────────────────────────────────
        self.Kp_linear  = 1.5   # proportional gain for distance
        self.Kp_angular = 4.0   # proportional gain for angle
        self.tolerance  = 0.1   # stop when within this distance of goal

        # ── Speed limits ───────────────────────────────────────────────────
        self.max_linear  = 2.0
        self.max_angular = 2.0

        # ── Run Task 3 ─────────────────────────────────────────────────────
        self.run_task3()

    # ══════════════════════════════════════════════════════════════════════
    #  CALLBACK
    # ══════════════════════════════════════════════════════════════════════

    def pose_callback(self, msg):
        self.current_pose = msg

    # ══════════════════════════════════════════════════════════════════════
    #  HELPERS
    # ══════════════════════════════════════════════════════════════════════

    def stop(self):
        msg = Twist()
        msg.linear.x  = 0.0
        msg.angular.z = 0.0
        self.pub.publish(msg)

    def get_distance(self, goal_x, goal_y):
        dx = goal_x - self.current_pose.x
        dy = goal_y - self.current_pose.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def get_angle_error(self, goal_x, goal_y):
        dx = goal_x - self.current_pose.x
        dy = goal_y - self.current_pose.y
        angle_to_goal = math.atan2(dy, dx)
        angle_error   = angle_to_goal - self.current_pose.theta
        # Normalise to [-π, π]
        return math.atan2(math.sin(angle_error), math.cos(angle_error))

    def teleport(self, x, y, theta=0.0):
        """Fallback: instantly teleport turtle1 to (x, y)."""
        req = TeleportAbsolute.Request()
        req.x     = float(x)
        req.y     = float(y)
        req.theta = float(theta)
        future = self.teleport_client.call_async(req)
        rclpy.spin_until_future_complete(self, future, timeout_sec=5.0)
        self.get_logger().info(f'Teleported turtle1 to ({x}, {y})')

    # ══════════════════════════════════════════════════════════════════════
    #  GO-TO-GOAL CONTROLLER
    # ══════════════════════════════════════════════════════════════════════

    def go_to_goal(self, goal_x, goal_y):
        """
        Proportional controller:
        - Steers turtle1 toward (goal_x, goal_y)
        - Stops when within self.tolerance of the goal
        """
        self.get_logger().info(
            f'Moving turtle1 to goal: ({goal_x}, {goal_y})'
        )

        # Wait until first pose is received
        self.get_logger().info('Waiting for pose data...')
        timeout = time.time() + 5.0
        while self.current_pose is None and time.time() < timeout:
            rclpy.spin_once(self, timeout_sec=0.1)

        if self.current_pose is None:
            self.get_logger().warn(
                'No pose received! Using teleport as fallback.'
            )
            self.teleport(goal_x, goal_y)
            return

        self.get_logger().info(
            f'Starting position: '
            f'({self.current_pose.x:.2f}, {self.current_pose.y:.2f})'
        )

        # Control loop
        while True:
            rclpy.spin_once(self, timeout_sec=0.05)

            if self.current_pose is None:
                continue

            distance    = self.get_distance(goal_x, goal_y)
            angle_error = self.get_angle_error(goal_x, goal_y)

            # ── Goal reached ──────────────────────────────────────────────
            if distance < self.tolerance:
                self.stop()
                self.get_logger().info(
                    f'Goal reached! '
                    f'Final position: '
                    f'({self.current_pose.x:.2f}, {self.current_pose.y:.2f})'
                )
                break

            # ── Compute velocities ────────────────────────────────────────
            linear_vel  = self.Kp_linear  * distance
            angular_vel = self.Kp_angular * angle_error

            # ── Clamp to safe limits ──────────────────────────────────────
            linear_vel  = min(linear_vel,  self.max_linear)
            angular_vel = max(
                min(angular_vel, self.max_angular), -self.max_angular
            )

            # ── Publish command ───────────────────────────────────────────
            msg = Twist()
            msg.linear.x  = linear_vel
            msg.angular.z = angular_vel
            self.pub.publish(msg)

            # ── Log progress every ~1 second ──────────────────────────────
            self.get_logger().info(
                f'Distance to goal: {distance:.2f} | '
                f'Angle error: {math.degrees(angle_error):.1f}° | '
                f'Linear: {linear_vel:.2f} | Angular: {angular_vel:.2f}'
            )

    # ══════════════════════════════════════════════════════════════════════
    #  TASK 3 - MAIN
    # ══════════════════════════════════════════════════════════════════════

    def run_task3(self):
        self.get_logger().info('=== TASK 3: Go-To-Goal Controller ===')

        time.sleep(1.0)  # Short delay to let everything settle

        # ── Goal 1 ────────────────────────────────────────────────────────
        self.go_to_goal(goal_x=7.0, goal_y=7.0)
        time.sleep(1.0)

        # ── Goal 2 (optional second goal) ─────────────────────────────────
        self.go_to_goal(goal_x=3.0, goal_y=8.0)
        time.sleep(1.0)

        # ── Goal 3 (optional third goal) ──────────────────────────────────
        self.go_to_goal(goal_x=5.5, goal_y=2.0)

        self.get_logger().info('=== TASK 3 COMPLETE ===')


# ══════════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════════

def main(args=None):
    rclpy.init(args=args)
    node = GoToGoalTurtle()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
