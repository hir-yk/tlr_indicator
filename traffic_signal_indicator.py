
import tkinter as tk
import rclpy
from rclpy.node import Node
from autoware_auto_perception_msgs.msg import LookingTrafficSignal

class TrafficLightExtractor(Node):
    def __init__(self, root):
        super().__init__('traffic_light_extractor')

        self.root = root
        self.root.title("Traffic Signal Indicator")
        self.canvas = tk.Canvas(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight(), bg='black')
        self.canvas.pack(fill="both", expand=True)

        self.subscription = self.create_subscription(
            LookingTrafficSignal,
            '/awapi/traffic_light/get/nearest_traffic_signal',
            self.listener_callback,
            10)

        self.root.bind("<Configure>", self.on_resize)
        self.judge = 0

    def on_resize(self, event):
        self.canvas.delete("all")
        self.canvas.config(width=event.width, height=event.height)

        # When resizing, keep a circular shape by using the minimum size among width and height.
        size = min(event.width, event.height)/5  # Decrease the size a bit
        self.size = size * 2  

        # Redraw current state
        self.update_display()

    def draw_circle(self, x, y, color):
        self.canvas.create_oval(x - self.size/2, y - self.size/2, x + self.size/2, y + self.size/2, fill=color)

    def listener_callback(self, msg):
        self.get_logger().info('Traffic Signal Judge: "%d"' % msg.result.judge)

        # Set the new state
        self.judge = msg.result.judge

        # Update the display
        self.update_display()

    def update_display(self):
        # Clear the canvas
        self.canvas.delete("all")

        dark_green = '#004D40'  # Even darker green, same as LED like green
        dark_yellow = '#404040'  # Even darker yellow
        dark_red = '#330000'  # Even darker red

        if self.judge == 0:
            self.draw_circle(self.canvas.winfo_width()/5, self.canvas.winfo_height()/2, dark_green)
            self.draw_circle(2.5*self.canvas.winfo_width()/5, self.canvas.winfo_height()/2, dark_yellow)
            self.draw_circle(4*self.canvas.winfo_width()/5, self.canvas.winfo_height()/2, dark_red)

        elif self.judge == 3:
            self.draw_circle(self.canvas.winfo_width()/5, self.canvas.winfo_height()/2, dark_green)
            self.draw_circle(2.5*self.canvas.winfo_width()/5, self.canvas.winfo_height()/2, dark_yellow)
            self.draw_circle(4*self.canvas.winfo_width()/5, self.canvas.winfo_height()/2, 'red')

        elif self.judge == 4:
            self.draw_circle(self.canvas.winfo_width()/5, self.canvas.winfo_height()/2, 'green')
            self.draw_circle(2.5*self.canvas.winfo_width()/5, self.canvas.winfo_height()/2, dark_yellow)
            self.draw_circle(4*self.canvas.winfo_width()/5, self.canvas.winfo_height()/2, dark_red)

def main(args=None):
    rclpy.init(args=args)

    root = tk.Tk()
    root.geometry("400x200")  # Set the initial window size to 400x200
    node = TrafficLightExtractor(root)

    def update():
        rclpy.spin_once(node)
        root.after(100, update)

    root.after(100, update)
    root.mainloop()

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


