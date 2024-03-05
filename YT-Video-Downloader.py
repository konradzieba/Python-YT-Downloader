from pytube import YouTube

url: str = input("Podaj URL")
output = input("Audio: [A], Video: [V]")

output_format = (
    "mp4" if output.lower() == "v" else "mp3" if output.lower() == "a" else None
)

if output_format is None:
    raise ValueError("Wpisano niedozwolony znak. Wpisz A lub V")

YouTube(url).streams.first().download()

yt = YouTube(url)
yt.streams.filter(progressive=True, file_extension=output_format).order_by(
    "resolution"
).desc().first().download(r"YT_Downloader")

print(f"\n Pobrano pomyślnie {yt.title}")
