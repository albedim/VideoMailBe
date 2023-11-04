import moviepy.editor as mp
from pydub import AudioSegment
import numpy as np

def extract_audio(video_path):
    video = mp.VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile("temp_audio.wav")
    return "temp_audio.wav"

def detect_and_print_voice_pauses(video_path, threshold=0.1, duration_threshold=1):
    audio_path = extract_audio(video_path)

    # Load the audio using PyDub
    audio = AudioSegment.from_wav(audio_path)

    # Convert audio to a NumPy array
    audio_data = np.array(audio.get_array_of_samples())

    # Calculate the frame rate (samples per second)
    frame_rate = audio.frame_rate

    # Initialize variables
    in_voice_pause = False
    voice_pause_start_time = 0

    # Iterate through the audio frames
    for i, sample in enumerate(audio_data):
        amp = np.abs(sample) / 32768.0  # Normalize the sample
        if amp < threshold:
            if not in_voice_pause:
                in_voice_pause = True
                voice_pause_start_time = i / frame_rate
        else:
            if in_voice_pause:
                in_voice_pause = False
                voice_pause_end_time = i / frame_rate
                pause_duration = voice_pause_end_time - voice_pause_start_time

                # If the pause duration is greater than the threshold, print "a"
                if pause_duration >= duration_threshold:
                    print(f"Voice Pause: {voice_pause_start_time:.2f}s to {voice_pause_end_time:.2f}s")


import speech_recognition as sr
from translate import Translator
import pyttsx3
from moviepy.editor import VideoFileClip
from moviepy.editor import AudioFileClip


def transcribe_audio(video_path):
    r = sr.Recognizer()
    audio_path = "temp_audio.wav"

    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_path)

    with sr.AudioFile(audio_path) as source:
        audio_data = r.record(source)

    try:
        transcript = r.recognize_google(audio_data)  # You can choose a different recognition engine if needed
        return transcript
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""


def translate_text(text, target_language):
    translator = Translator(to_lang=target_language)
    return translator.translate(text)


def generate_audio(text, target_language, output_audio_path):
    engine = pyttsx3.init()
    engine.save_to_file(text, output_audio_path)
    engine.runAndWait()


def main(video_path, target_language, output_video_path):
    transcript = transcribe_audio(video_path)
    if not transcript:
        print("Speech recognition failed.")
        return

    translated_text = translate_text(transcript, target_language)

    output_audio_path = "translated_audio.mp3"
    generate_audio(translated_text, target_language, output_audio_path)

    video = VideoFileClip(video_path)
    translated_audio = AudioFileClip(output_audio_path)
    final_video = video.set_audio(translated_audio)
    final_video.write_videofile(output_video_path, codec="libx264", audio_codec="aac")


if __name__ == "__main__":
    video_path = "a.mp4"  # Replace with the path to your video
    target_language = "es"  # Replace with the target language code
    output_video_path = "b.mp4"  # Replace with the output video path
    main(video_path, target_language, output_video_path)

    # Example usage
    #video_path = "a.mp4"
    #detect_and_print_voice_pauses(video_path)
