import customtkinter as ctk
import win32gui
from pynput.mouse import Listener as Mouse_Listener
from pynput.keyboard import Listener as Key_Listener, Key
import threading

class ColorPicker(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Color Analyzer")
        self.geometry("300x200")
        self.attributes('-topmost', True)

        self.color_display = ctk.CTkFrame(self, width=100, height=100, corner_radius=10)

        self.color_display.pack(pady=20)

        self.rgb_entry = ctk.CTkEntry(self, placeholder_text="RGB Color")
        self.rgb_entry.pack()

        self.hex_entry = ctk.CTkEntry(self, placeholder_text="Hex Color")
        self.hex_entry.pack()

        # Start color picker functionality in a separate thread to keep UI responsive
        threading.Thread(target=self.start_color_picker, daemon=True).start()

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

    def start_color_picker(self):
        with Key_Listener(on_press=self.on_key_press) as keyboard_listener, \
                Mouse_Listener(on_click=self.on_click) as mouse_listener:
            print("Color Picker active... Press 'Esc' to stop.")
            keyboard_listener.join()
            mouse_listener.stop()

    def on_key_press(self, key):
        if key == Key.esc:
            self.stop_listeners = True
            self.quit()  # Closes the GUI
            return False  # Stops listener

if __name__ == "__main__":
    app = ColorPicker()
    app.mainloop()
