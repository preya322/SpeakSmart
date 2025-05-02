import asyncio
from random import randint
from PIL import Image
import requests
import os
from time import sleep

# Configuration
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
HEADERS = {"Authorization": "Bearer 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"}
IMAGE_FOLDER = "Data/Generated-Images"
DATA_FILE = "Frontend/Files/ImageGeneration.data"


def sanitize_prompt(prompt: str) -> str:
    """Removes spaces from the prompt to use as a filename."""
    return prompt.replace(" ", "")


def open_images(prompt: str):
    """Opens the generated images sequentially."""
    sanitized_prompt = sanitize_prompt(prompt)
    files = [f"{sanitized_prompt}{i}.jpg" for i in range(1, 5)]

    for jpg_file in files:
        image_path = os.path.join(IMAGE_FOLDER, jpg_file)

        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)
        except IOError:
            print(f"Unable to open {image_path}")


async def query(payload):
    """Sends an API request to generate an image."""
    response = await asyncio.to_thread(requests.post, API_URL, headers=HEADERS, json=payload)
    return response.content


async def generate_images_async(prompt: str):
    """Generates images asynchronously using the API."""
    tasks = []

    # for i in range(4):
    payload = {
        "inputs": f"{prompt}, 4K, sharp, ultra-high details",
        "parameters": {"seed": randint(0, 1000000)}
    }
    tasks.append(asyncio.create_task(query(payload)))

    image_bytes_list = await asyncio.gather(*tasks)

    save_generated_images(prompt, image_bytes_list)


def save_generated_images(prompt: str, image_bytes_list: list):
    """Saves the generated images to disk."""
    os.makedirs(IMAGE_FOLDER, exist_ok=True)
    sanitized_prompt = sanitize_prompt(prompt)

    for i, image_bytes in enumerate(image_bytes_list):
        image_path = os.path.join(IMAGE_FOLDER, f"{sanitized_prompt}{i+1}.jpg")
        with open(image_path, "wb") as f:
            f.write(image_bytes)


def generate_images(prompt: str):
    """Runs the image generation and opens the images."""
    asyncio.run(generate_images_async(prompt))
    open_images(prompt)


def read_data_file() -> tuple:
    """Reads the data file and returns the prompt and status."""
    try:
        with open(DATA_FILE, "r") as f:
            data = f.read().strip()

        if "," not in data:
            print("Invalid data format")
            return None, None

        return data.split(",")

    except Exception as e:
        print(f"Error reading data file: {e}")
        return None, None


def write_data_file(content: str):
    """Writes data to the file."""
    try:
        with open(DATA_FILE, "w") as f:
            f.write(content)
    except Exception as e:
        print(f"Error writing to data file: {e}")


def main():
    """Main loop to check the data file and generate images if required."""
    while True:
        prompt, status = read_data_file()

        if not prompt or not status:
            sleep(1)
            continue

        if status.strip().lower() == "true":
            print("Generating Image...")
            generate_images(prompt.strip())
            write_data_file("False, False")
            break
        else:
            sleep(1)


if __name__ == "__main__":
    main()
