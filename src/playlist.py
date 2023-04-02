import os
from googleapiclient.discovery import build
import isodate
from src.video import Video
import datetime

class PlayList():
    api_key = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.playlists = PlayList.youtube.playlistItems().list(playlistId=playlist_id,
                                                 part='snippet,contentDetails',
                                                 maxResults=50,
                                                 ).execute()
        self.title = self.playlists['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/playlist?list=' + playlist_id

    @property
    def total_duration(self):
        ans = datetime.timedelta(0)
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlists['items']]
        video_response = PlayList.youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            ans += duration
        return ans

    def show_best_video(self):
        ans_likes = -1
        ans_url = ''
        videos = [video['contentDetails']['videoId'] for video in self.playlists['items']]
        for i in videos:
            my_video = Video(i)
            if ans_likes < my_video.like_count:
                ans_likes = my_video.like_count
                ans_url = my_video.video_url
        return ans_url

