#! /usr/bin/python

import sys
import pygame
from PIL import Image
import requests
from io import BytesIO


def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        return img
    else:
        print(f"Failed to download image: {response.status_code}")
        return None


def display_notification(data):
    pygame.init()

    window_size = (400, 200)
    screen = pygame.display.set_mode(window_size, pygame.NOFRAME | pygame.SRCALPHA)
    pygame.display.set_caption("Notification")

    # Set the screen's background color to light blue
    # RGBA for light blue with full opacity (no transparency)
    light_blue = (173, 216, 230, 255)  # Adjust the alpha if you want some transparency
    screen.fill(light_blue)

    # Parse the data
    image_url, title, text = data.split(";")

    # Download the image
    pil_image = download_image(image_url)
    if pil_image:
        pil_image = pil_image.convert("RGBA")
        # Use Image.Resampling.LANCZOS for resizing
        pil_image = pil_image.resize((100, 100), Image.Resampling.LANCZOS)

        mode = pil_image.mode
        size = pil_image.size
        data = pil_image.tobytes()

        # Convert PIL image to PyGame image
        pygame_image = pygame.image.fromstring(data, size, mode)
        screen.blit(pygame_image, (10, 50))  # Adjust position as needed

    # Display the title
    font_title = pygame.font.Font(None, 36)
    font_title.set_bold(True)
    title_surface = font_title.render(
        title, True, (255, 255, 255)
    )  # Using white for text color
    screen.blit(title_surface, (120, 45))  # Adjust position as needed

    # Display the text
    font_text = pygame.font.Font(None, 24)
    text_surface = font_text.render(
        text, True, (255, 255, 255)
    )  # Using white for text color
    screen.blit(text_surface, (120, 85))  # Adjust position as needed

    pygame.display.flip()

    # Wait for a set duration then exit
    pygame.time.wait(5000)

    pygame.quit()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        data = sys.argv[1]
        display_notification(data)
    else:
        print("No data provided.")
