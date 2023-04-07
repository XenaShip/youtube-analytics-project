import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class Video:
    api_key = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str) -> None:
        self.__video_id = video_id
        try:
            video_response = Video.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id
                                               ).execute()
            self.video_title = video_response['items'][0]['snippet']['title']
        except Exception as e:
            self.video_title = None
            self.video_url = None
            self.view_count = None
            self.like_count = None
        else:
            self.video_title = video_response['items'][0]['snippet']['title']
            self.video_url = 'https://www.youtube.com/watch?v=' + self.__video_id
            self.view_count = int(video_response['items'][0]['statistics']['viewCount'])
            self.like_count = int(video_response['items'][0]['statistics']['likeCount'])

    def __str__(self):
        return self.video_title


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id