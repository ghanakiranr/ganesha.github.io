from flask import Flask, render_template, send_from_directory
from PIL import Image, ImageDraw, ImageFont
import os
import random
import threading

app = Flask(__name__)

# Directory for storing generated GIFs and images
static_directory = 'static'

# Create the static directory if it doesn't exist
os.makedirs(static_directory, exist_ok=True)

# List of image paths
image_paths = [
    'static/image1.jpg',
    'static/image2.jpg',
    'static/image3.jpg',
    'static/image4.jpg',
    'static/image5.jpg',
    'static/image6.jpg',
    'static/image7.jpg',
]

# List of GIF paths
gif_paths = [
    'static/gif1.gif',
    'static/gif2.gif',
]

# List of cracker images
cracker_paths = [
    'static/crackers_burst.gif',
    'static/crack.gif',
]

# List of color papers
color_paper_paths = [
    'static/firecrackers-happy-diwali.gif',
    'static/giphy.gif',
]

def generate_animation():
    # Create a list to hold each frame of the gif
    frames = []

    # Define the colors you want to use for text
    colors = ['#FF5733', '#4CAF50', '#FF5733', '#4CAF50', '#FF5733', '#4CAF50']

    for _ in range(5):  # Generate 5 frames
        for image_path in image_paths:
            # Load the image
            img = Image.open(image_path)
            img = img.resize((200, 200))

            # Create a drawing context
            d = ImageDraw.Draw(img)

            for color in colors:
                # Draw the text with changing color
                fnt = ImageFont.load_default()  # Use a default font
                d.text((10, 90), "Happy Birthday Ganesh", font=fnt, fill=color)

                # Add crackers and color papers randomly
                add_crackers_and_color_papers(img)

                # Append the frame to the list of frames
                frames.append(img.copy())

        for gif_path in gif_paths:
            gif_img = Image.open(gif_path)

            # Resize the GIF image if necessary
            if gif_img.width > 200 or gif_img.height > 200:
                gif_img.thumbnail((200, 200))

            # Add crackers and color papers randomly
            add_crackers_and_color_papers(gif_img)

            # Append the GIF frame to the list of frames
            frames.append(gif_img.copy())

    # Save frames as an animated gif
    gif_path = os.path.join(static_directory, 'animated_greeting.gif')
    frames[0].save(gif_path, format='GIF', append_images=frames[1:], save_all=True, duration=300, loop=0)

def add_crackers_and_color_papers(img):
    # Randomly add crackers and color papers to the image
    for _ in range(random.randint(1, 5)):
        cracker_path = random.choice(cracker_paths)
        color_paper_path = random.choice(color_paper_paths)

        cracker = Image.open(cracker_path)
        color_paper = Image.open(color_paper_path)

        # Randomly position crackers and color papers
        x = random.randint(0, img.width - cracker.width)
        y = random.randint(0, img.height - cracker.height)

        # Paste the cracker and color paper on the image
        img.paste(cracker, (x, y), cracker)
        img.paste(color_paper, (x, y), color_paper)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_gif')
def generate_gif_route():
    # Check if the GIF already exists
    gif_path = os.path.join(static_directory, 'animated_greeting.gif')
    if not os.path.exists(gif_path):
        # Generate the animation in a separate thread to avoid blocking the server
        animation_thread = threading.Thread(target=generate_animation)
        animation_thread.start()

    # Return a message to the user
    return 'Generating GIF, please refresh this page in a moment.'

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)
    
@app.route('/animate.html')
def animate():
    return render_template('animate.html')


if __name__ == '__main__':
    app.run(debug=True)
