import tkinter as tk
from tkinter import messagebox
from pytube import YouTube
from moviepy.editor import *

clip_length = None


def download_video_or_audio(start_time, end_time):
    url = url_entry.get()
    output = format_var.get()

    output_format = (
        "mp4" if output.lower() == "v" else "mp3" if output.lower() == "a" else None
    )

    try:
        if output_format is None:
            messagebox.showinfo("Wpisano niedozwolony znak. Wpisz A lub V")

        yt = YouTube(url)
        global clip_length
        clip_length = yt.length

        if clip_length is None:
            messagebox.showinfo("Nie znaleziono długości klipu.")

        start_time_slider.configure(to=clip_length, length=clip_length)
        end_time_slider.configure(to=clip_length, length=clip_length)

        if output_format == "mp4":
            video_stream = (
                yt.streams.filter(progressive=True, file_extension=output_format)
                .order_by("resolution")
                .desc()
                .first()
            )
            if video_stream:
                video_path = f"./Youtube-Downloader/{yt.title}.mp4"
                video_stream.download(
                    output_path="./Youtube-Downloader", filename=f"{yt.title}.mp4"
                )
                video_clip = VideoFileClip(video_path).subclip(start_time, end_time)
                video_clip.write_videofile(
                    f"./Youtube-Downloader/{yt.title}_trimmed.mp4",
                    codec="libx264",
                    audio_codec="aac",
                    progress_bar=True,
                )
                video_clip.close()
                messagebox.showinfo(
                    "Sukces",
                    f"Pobieranie {yt.title} zakończone. Plik znajduje się w folderze Youtube-Downloader.",
                )
            else:
                messagebox.showinfo("Nie znaleziono odpowiedniego strumienia wideo.")
        elif output_format == "mp3":
            audio_stream = yt.streams.filter(only_audio=True).first()
            if audio_stream:
                audio_stream.download(
                    output_path="./Youtube-Downloader",
                    filename=f"{yt.title}.mp3",
                    progress_bar=True,
                )
                messagebox.showinfo(
                    "Sukces",
                    f"Pobieranie {yt.title} zakończone. Plik znajduje się w folderze Youtube-Downloader.",
                )
            else:
                messagebox.showinfo("Nie znaleziono odpowiedniego strumienia audio.")
        else:
            messagebox.showinfo(
                "Wpisano niedozwolony format. Wpisz V dla wideo lub A dla audio."
            )
    except Exception as e:
        messagebox.showerror("Błąd", f"Wystąpił błąd: {e}")


def close_app():
    root.destroy()


def update_slider_values(_):
    start_time = start_time_slider.get()
    end_time = end_time_slider.get()
    start_label.config(text=f"Start: {start_time} s")
    end_label.config(text=f"End: {end_time} s")


def update_sliders_on_url_focus_out(_):
    url = url_entry.get()
    if url:
        try:
            yt = YouTube(url)
            global clip_length
            clip_length = yt.length
            start_time_slider.configure(to=clip_length, length=clip_length)
            end_time_slider.configure(to=clip_length, length=clip_length)
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd: {e}")


root = tk.Tk()
root.title("YouTube Downloader")
root.resizable(False, False)


tk.Label(root, text="Podaj URL:").pack()
url_entry = tk.Entry(root, width=70)
url_entry.pack()
url_entry.bind("<<FocusOut>>", update_sliders_on_url_focus_out)

tk.Label(root, text="Format:").pack()

format_var = tk.StringVar()
format_var.set("V")

format_radio_video = tk.Radiobutton(root, text="Video", variable=format_var, value="V")
format_radio_audio = tk.Radiobutton(root, text="Audio", variable=format_var, value="A")

format_radio_video.pack(side=tk.TOP, padx=5)
format_radio_audio.pack(side=tk.TOP, padx=5)

start_label = tk.Label(root, text="Start: 0 s")
start_label.pack()
start_time_slider = tk.Scale(
    root,
    from_=0,
    to=clip_length,
    orient=tk.HORIZONTAL,
    length=300,
    command=update_slider_values,
)
start_time_slider.pack()

end_label = tk.Label(root, text="End: 300 s")
end_label.pack()
end_time_slider = tk.Scale(
    root,
    from_=0,
    to=clip_length,
    orient=tk.HORIZONTAL,
    length=300,
    command=update_slider_values,
)
end_time_slider.pack()


download_button = tk.Button(
    root,
    text="Pobierz",
    command=lambda: download_video_or_audio(
        start_time_slider.get(), end_time_slider.get()
    ),
)
download_button.pack(side=tk.BOTTOM, pady=15)

close_button = tk.Button(root, text="Zamknij", command=close_app)
close_button.pack(side=tk.BOTTOM, pady=5)

root.mainloop()
