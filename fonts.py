import tkinter as tk

class FontDemoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Handwritten Fonts Demo")

        # Create labels with different fonts
        fonts = [
            ("Comic Sans MS", 20),
            ("Bradley Hand ITC", 20),
            ("Lucida Handwriting", 20),
            ("Dancing Script", 20),
            ("Pacifico", 20)
        ]

        for font_name, font_size in fonts:
            label = tk.Label(root, text=f"Font: {font_name}", font=(font_name, font_size))
            label.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = FontDemoApp(root)
    root.mainloop()
