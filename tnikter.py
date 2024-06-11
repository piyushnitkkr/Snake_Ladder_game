import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Background Image Example")

    try:
        # Load the image file
        bg_image = tk.PhotoImage(file="istockphoto-455302535-612x612.jpg")

        # Create a label widget with the background image
        bg_label = tk.Label(root, image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        print("Image loaded successfully")

        # Add other widgets on top of the background image
        # For example, you can add buttons, labels, etc.

        # Run the Tkinter main loop
        root.mainloop()
    except Exception as e:
        print("Error loading image:", e)

if __name__ == "__main__":
    main()
