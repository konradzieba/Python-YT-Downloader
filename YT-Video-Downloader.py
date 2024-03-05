import os
from pytube import YouTube
from tqdm import tqdm

audio_only: bool = True

url: str = input("Podaj URL: ")
audio_only_input = input("Tylko audio [A], Video [V]: ")

is_input_valid: bool = (
    isinstance(url, str)
    and isinstance(audio_only_input, str)
    and audio_only_input.lower() == "v"
    or audio_only_input == "a"
)

if is_input_valid:
    if audio_only_input.lower() == "v":
        audio_only = False


video = YouTube(url)

stream = (
    video.streams.filter(only_audio=audio_only).get_highest_resolution()
    if not audio_only
    else video.streams.filter(only_audio=audio_only).first()
)

file_size = stream.filesize

out_dir = "YT_Downloader"

os.makedirs(out_dir, exist_ok=True)

cleaned_title = "".join(c for c in video.title if c.isalnum() or c in [" ", ".", "-"])

progress_bar = tqdm(total=file_size, unit="B", unit_scale=True, unit_divisor=1024)


def on_progress(chunk, file_handle, remaining):
    if isinstance(chunk, bytes):
        chunk = len(chunk)
    progress_bar.update(chunk)


stream.on_progress = on_progress

file_format = ".mp4" if not audio_only else ".mp3"

stream.download(output_path=out_dir, filename=f"{cleaned_title}{file_format}")

progress_bar.close()

print(f"{video.title} został pobrany pomyślnie!")
