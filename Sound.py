import youtube_dl as yt 
import os 
import abc
import mimetypes
import Info

def get_acceptable_audio_formats():
    for ext in mimetypes.types_map:
        if mimetypes.types_map[ext].split('/')[0] == 'audio':
            yield ext

class Sound:
    

    def __init__(self,ctx):
        self.path = None
        self.title = None
        self.is_valid  = None
        self.voice_channel = ctx.author.voice.channel
        self.prefix = Info.ServerInformation("Data Files/server_info.json").server_info["audio_dir"]



    def validate_file(self):
        print(tuple(get_acceptable_audio_formats()))
        if self.path != None:
            self.is_valid = os.path.exists(self.path) and "."+self.path.split(".")[-1] in tuple(get_acceptable_audio_formats())
        else:
            self.is_valid = False

class LocalSound(Sound):
    def __init__(self,ctx,title):
        super().__init__(ctx) 
        self.title = self.find_files(title)
        self.path = self.prefix+self.title
        self.validate_file()
        print(self.is_valid)

    def find_files(self,title):
        for i in os.listdir(self.prefix):
            if i.split(".")[0] == title:
                return i
        return "zzzzzzzzz"

#t = LocalSound("test")

class YoutubeSound(Sound):

    def __init__(self,ctx,url):
        super().__init__(ctx) 
        self.url = url

        self.get_youtube_title()
        if self.is_valid:
            self.download_youtube_audio()
            self.validate_file()

    def __del__(self):
        if self.is_valid:
            print("Cleaning",self.path)
            os.remove(self.path)

    def download_youtube_audio(self):
        self.path = self.prefix + self.title  
        ydl_opts = { 'format': 'bestaudio/best',
                'outtmpl': self.path,
                'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
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
