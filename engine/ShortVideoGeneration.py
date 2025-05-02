import os
import re
import time
import json
import eel
from timeit import default_timer as timer
from gtts import gTTS
from moviepy.editor import *
from huggingface_hub import InferenceClient
from pydub import AudioSegment
from tqdm import tqdm
import google.generativeai as genai
from engine.TextToSpeech import TextToSpeech

# Configure API keys
HF_TOKEN = "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"
GENAI_KEY = "AIzaSyByGyBAFczgCUGsOaXv_vWdXsxYZ7ylnsg"
IMAGE_MODEL = "stabilityai/stable-diffusion-3.5-large-turbo"
TEXT_MODEL = "gemini-1.5-flash-latest"

# Initialize APIs
client = InferenceClient(
    provider="hf-inference",
    api_key=HF_TOKEN,
)
# client = InferenceClient(model=IMAGE_MODEL, token=HF_TOKEN)
genai.configure(api_key=GENAI_KEY)
gen_model = genai.GenerativeModel(TEXT_MODEL, generation_config={"response_mime_type": "application/json"})

# Define global variables
WIDTH, HEIGHT = 1472, 832


def setup_directories():
    """Create necessary directories if they do not exist."""
    os.makedirs("ShortVideoAssets/audio", exist_ok=True)
    os.makedirs("ShortVideoAssets/image", exist_ok=True)
    os.makedirs("ShortVideoAssets/videos", exist_ok=True)


def generate_story(topic):
    """Generate a short story with image prompts using Gemini API."""
    prompt = (
        f"Generate a short story on the topic '{topic}'. "
        "Each slide should have a 'par_no', 'paragraph', and 'image_prompt' section. "
        "Provide 5 paragraphs with 1 sentence each and a very detailed image prompt. "
        "Return the output in JSON format."
    )
    response = gen_model.generate_content(prompt)
    story_data = json.loads(response.text)

    with open("ShortVideoAssets/generated_text.txt", "w") as file:
        for para in story_data['story']:
            file.write(para['paragraph'] + "\n\n")

    with open("ShortVideoAssets/prompt.txt", "w") as file:
        for para in story_data['story']:
            file.write(para['image_prompt'] + ".\n\n")

    print("The text has been generated successfully!")


def read_file(filename):
    """Read content from a file."""
    with open(filename, "r") as file:
        return file.read()


def generate_ai_image(prompt, index):
    """Generate an AI image based on the prompt."""
    try:
        print(f"Generating AI image {index}...")
        time.sleep(5)  # Simulate processing delay
        output = client.text_to_image(prompt,model="stabilityai/stable-diffusion-xl-base-1.0",
                                       width=WIDTH, height=HEIGHT)
        time.sleep(5)
        image_path = f"ShortVideoAssets/image/image{index}.png"
        output.save(image_path)
        return image_path
    except Exception as e:
        print(f"Error generating image: {e}")
        time.sleep(5)
        return None


def generate_voiceover(text, index):
    """Convert text to speech and save as audio."""
    try:
        print(f"Generating voiceover {index}...")
        tts = gTTS(text=text, lang="en", slow=False)
        audio_mp3_path = f"ShortVideoAssets/audio/voiceover{index}.mp3"
        tts.save(audio_mp3_path)

        # Convert MP3 to WAV for compatibility
        audio_wav_path = f"ShortVideoAssets/audio/voiceover{index}.wav"
        audio = AudioSegment.from_mp3(audio_mp3_path)
        audio.export(audio_wav_path, format="wav")

        return audio_wav_path
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None


def create_video_clip(image_path, audio_path, index):
    """Combine an image with an audio file to create a video clip."""
    try:
        print(f"Creating video clip {index}...")

        # Load audio
        audio_clip = AudioFileClip(audio_path)
        audio_duration = audio_clip.duration

        # Load image and set duration
        image_clip = ImageClip(image_path).set_duration(audio_duration)

        # Combine image and audio
        video_clip = CompositeVideoClip([image_clip]).set_audio(audio_clip)
        video_output_path = f"ShortVideoAssets/videos/video{index}.mp4"
        video_clip.write_videofile(video_output_path, fps=24, codec="libx264", audio_codec="aac")
        TextToSpeech(f"videoclip-{index} generated successfully....")
        return video_clip
    except Exception as e:
        print(f"Error creating video: {e}")
        return None


def process_story():
    """Process the story by generating images, voiceovers, and combining them into video clips."""
    text_content = read_file("ShortVideoAssets/generated_text.txt")
    prompt_content = read_file("ShortVideoAssets/prompt.txt")

    paragraphs = re.split(r"[.]", text_content)
    image_prompts = re.split(r"[.]", prompt_content)

    clips = []

    for i, para in tqdm(enumerate(paragraphs, start=1), desc="Processing Paragraphs", total=len(paragraphs)):
        if not para.strip():
            continue

        print(f"\nProcessing paragraph {i}...")

        # Generate AI image
        image_path = generate_ai_image(image_prompts[i - 1], i)
        if not image_path:
            continue

        # Convert text to speech
        audio_path = generate_voiceover(para, i)
        if not audio_path:
            continue

        # Create video clip
        video_clip = create_video_clip(image_path, audio_path, i)
        if video_clip:
            clips.append(video_clip)

        time.sleep(5)

    return clips


def merge_videos(clips):
    """Merge all generated video clips into a final video."""
    if clips:
        print("\nConcatenating all video clips...")
        try:
            final_video = concatenate_videoclips(clips, method="compose").set_fps(24)
            final_video.write_videofile("ShortVideoAssets/final_video.mp4", fps=24, codec="libx264", audio_codec="aac")
            print("The final video has been created successfully!")
        except Exception as e:
            print(f"Error concatenating videos: {e}")


def ShortVideo(topic: str):
    """Main function to execute the script workflow."""
    start = timer()

    # Setup directories
    setup_directories()

    # Generate a story
    # topic = input("Enter your topic: ")
    generate_story(topic)

    # Process the story into video clips
    video_clips = process_story()

    # Merge clips into a final video
    merge_videos(video_clips)

    # Measure execution time
    end = timer()
    print(f"Time taken: {(end - start) / 60:.2f} minutes")

    # Play final video (Mac: 'open', Windows: 'start')
    os.system("open ShortVideoAssets/final_video.mp4")


if __name__ == "__main__":
    ShortVideo("Pokemon")
