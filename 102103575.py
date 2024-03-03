import os
import sys
from pytube import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_audioclips

from youtubesearchpython import VideosSearch

def download_videos(singer_name, n):
    query = f"{singer_name} songs"
    search = VideosSearch(query, limit=n)
    videos = []
    i = 0
    while len(videos) < n and i < len(search.result()['result']):
        try:
            result = search.result()['result'][i]
            video_url = f"https://music.youtube.com/watch?v={result['id']}"
            video_id = result['id']
            video_path = f"{singer_name}_videos/{singer_name}_video_{len(videos)+1}.mp3"
            if not os.path.exists(video_path):
                yt = YouTube(video_url)
                stream = yt.streams.filter(only_audio=True).first()
                stream.download(output_path=f"{singer_name}_videos", filename=f"{singer_name}_video_{len(videos)+1}.mp3")
                print(f"Video {len(videos)+1} downloaded successfully")
            else:
                print(f"Video {len(videos)+1} already exists. Skipping download.")
            videos.append(video_path)
        except Exception as e:
            print(f"Error downloading video {len(videos)+1}: {e}")
        finally:
            i += 1
    return videos



def cut_audio(audio_paths, duration):
    audio=[]
    for audio_path in audio_paths:
        try:
            audio_clip = AudioFileClip(audio_path)
            cut_audio_clip = audio_clip.subclip(25, 25 + duration)
            cut_audio_path = audio_path.replace(".mp3", f"_cut_{duration}.mp3")
            cut_audio_clip.write_audiofile(cut_audio_path)
            print(f"Audio cut successfully: {cut_audio_path}")
            audio.append(cut_audio_path)
        except Exception as e:
            print(f"Error cutting audio: {e}")
    return audio

def merge_audios(audio_paths, output_file):
    audio_clips = [AudioFileClip(audio_path) for audio_path in audio_paths]
    concatenated_clip = concatenate_audioclips(audio_clips)
    concatenated_clip.write_audiofile(output_file)
    print(f"All audios merged successfully into: {output_file}")

def main():
    if len(sys.argv) != 5:
        print("Usage: python program.py <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        return

    singer_name = sys.argv[1]
    n = int(sys.argv[2])
    duration = int(sys.argv[3])
    output_file = sys.argv[4]

    if n <= 10:
        print("Number of videos must be greater than 10.")
        return

    if duration <= 20:
        print("Audio duration must be greater than 20 seconds.")
        return

    if not singer_name.isalpha():
        print("Singer name should contain only alphabets.")
        return

    if not output_file.endswith(".mp3"):
        output_file += ".mp3"

    try:
        os.makedirs(f"{singer_name}_videos", exist_ok=True)
        video_paths = download_videos(singer_name, n)
        cut_paths = cut_audio(video_paths, duration)
        merge_audios(cut_paths, output_file)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
