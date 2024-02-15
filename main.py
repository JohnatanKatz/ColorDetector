import customtkinter as ctk
import win32gui
from pynput.mouse import Listener as Mouse_Listener
import threading

class ColorDetector(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Color Analyzer")
        self.geometry("300x300")
        self.attributes('-topmost', True)

        self.color_display = ctk.CTkFrame(self, width=100, height=100, corner_radius=10)
        self.color_display.pack(pady=20)

        self.rgb_entry = ctk.CTkEntry(self, placeholder_text="RGB Color")
        self.rgb_entry.pack()

        self.hex_entry = ctk.CTkEntry(self, placeholder_text="Hex Color")
        self.hex_entry.pack()

        # Add a start button to initiate the color picker
        self.toggle_button = ctk.CTkButton(self, text="Start", command=self.start_button_clicked)
        self.toggle_button.pack(pady=10)

        # Variables to control listener state
        self.color_picker_active = False
        self.mouse_listener = None

    def start_button_clicked(self):
        """Switches the color picker functionality."""
        if not self.color_picker_active:
            self.color_picker_active = True
            self.toggle_button.configure(text="Stop")
            threading.Thread(target=self.start_color_picker, daemon=True).start()
        else:
            self.color_picker_active = False
            self.toggle_button.configure(text="Start")
            if self.mouse_listener:
                self.mouse_listener.stop()


    def start_color_picker(self):
        self.mouse_listener = Mouse_Listener(on_click=self.on_click)
        self.mouse_listener.start()
        self.mouse_listener.join()

    def get_pixel_color(self, x, y):
        """Gets the color of the pixel at the given (x, y) screen coordinates."""
        hdc = win32gui.GetDC(None)
        color = win32gui.GetPixel(hdc, x, y)
        win32gui.ReleaseDC(None, hdc)
        # Converts color from int to RGB tuple
        red = color & 0xff
        green = (color >> 8) & 0xff
        blue = (color >> 16) & 0xff
        return red, green, blue

    def rgb_to_hex(self, rgb):
        """Converts an RGB tuple to a hex string."""
        return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])

    def clicked_outside_window(self, x, y):
        # Get the window's current position and size
        window_x = self.winfo_x()
        window_y = self.winfo_y()
        window_width = self.winfo_width()
        window_height = self.winfo_height()

        # Check if the click is outside the window bounds
        return x < window_x or x > window_x + window_width or y < window_y or y > window_y + window_height


    def on_click(self, x, y, button, pressed):
        if pressed and self.clicked_outside_window(x, y):
            color = self.get_pixel_color(x, y)
            hex_color = self.rgb_to_hex(color)
            # Updates UI components with the new color
            self.update_ui(color, hex_color)

    def update_ui(self, color, hex_color):
        # Uses `ctk.CTk` method to run UI updates in the main thread
        self.rgb_entry.delete(0, "end")
        self.rgb_entry.insert(0, str(color))

        self.hex_entry.delete(0, "end")
        self.hex_entry.insert(0, hex_color)

        self.color_display.configure(fg_color=hex_color)


if __name__ == "__main__":
    app = ColorDetector()
    app.mainloop()
