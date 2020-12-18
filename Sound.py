import youtube_dl as yt 
import os 
import abc

class Sound:
    
    path : str 
    title : str
    is_valid : bool
    

    prefix = "Data Files/Audio Files/"

    @abc.abstractmethod
    def validate_file(self):
        return NotImplementedError
    
    def validate_file(self):
        if self.path != None:
            self.is_valid = os.path.exists(self.path)
        else:
            self.is_valid = False
    
    def get_acceptable_audio_formats(self)

class YoutubeSound(Sound):

    def __init__(self,url):
        self.url = url

        self.get_youtube_title()
        self.download_youtube_audio()
        self.validate_file()

    def __del__(self):
        self.validate_file()
        if self.is_valid:
            os.remove(self.path)

    def download_youtube_audio(self):
        self.path = self.prefix + self.title  
        ydl_opts = { 'format': 'bestaudio/best',
                'outtmpl': self.path,
                'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],}

        with yt.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([self.url])
            except yt.utils.DownloadError:
                self.is_valid = False
                print("Not able to download")

    def get_youtube_title(self):
        ydl_opts = {}

        with yt.YoutubeDL(ydl_opts) as ydl:
            try:
                info_dict = ydl.extract_info(self.url, download=False)
                
                self.title  = info_dict.get('title', None) + ".mp3"
                self.is_valid = True
            except yt.utils.DownloadError:
                print("User Reqested Invalid Video")
                self.is_valid =  False




#t = YoutubeSound("https://www.youtube.com/watch?v=JCkEzmaGNac")
