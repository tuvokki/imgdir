import click
from PIL import Image, ImageTk
import tkinter as tk


@click.command()
@click.option('--gif', prompt='Enter the path to the GIF file', type=click.Path(exists=True))
def play_gif(gif):
    # Load the GIF file
    gif_image = Image.open(gif)

    # Create the Tkinter window
    root = tk.Tk()

    # Create a Tkinter canvas to display the GIF image
    canvas = tk.Canvas(root, width=gif_image.width, height=gif_image.height)
    canvas.pack()

    # Create a list to hold the GIF frames
    gif_frames = []

    # Extract the individual frames from the GIF
    try:
        while True:
            gif_frames.append(gif_image.copy())
            gif_image.seek(len(gif_frames))
    except EOFError:
        pass

    # Create a function to display the GIF frames
    def update_frame(frame_index):
        # Update the canvas with the current frame
        canvas.image = ImageTk.PhotoImage(gif_frames[frame_index])
        canvas.create_image(0, 0, image=canvas.image, anchor='nw')

        # Update the frame index
        frame_index += 1
        if frame_index == len(gif_frames):
            frame_index = 0

        # Schedule the next frame update
        root.after(100, lambda: update_frame(frame_index))

    # Start displaying the GIF frames
    update_frame(0)

    # Run the Tkinter event loop
    root.mainloop()


if __name__ == '__main__':
    play_gif()
