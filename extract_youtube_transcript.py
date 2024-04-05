import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api import TranscriptsDisabled

youtube_re = r"((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?"


def extract_youtube_transcript(input_string):
    transcript_map = {}
    video_ids = list(set([str(v[-2]) for v in re.findall(youtube_re, input_string) if str(v[-2]) != ""]))
    
    for video_id in video_ids:
        print(video_id)
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            transcript_map[video_id] = " ".join([d['text'] for d in transcript])
        except TranscriptsDisabled:
            print(f"No transcript for video id: {video_id}")
            continue
        print(transcript)
    
    return transcript_map
