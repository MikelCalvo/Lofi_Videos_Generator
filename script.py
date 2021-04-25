import moviepy.editor as mpe
import moviepy.video as mpv
from moviepy.video.fx.all import crop
from random import randint
from math import floor
from assets.wordlists.sad_words import sad_word_list
from assets.wordlists.happy_words import happy_word_list
from assets.wordlists.dark_words import dark_word_list

class Generator:
    def __init__(self, filename, audioname, resizeForTikTok, textBoolean, wordType):
        self.total_duration = 0
        self.clip_list = []
        self.clip = mpe.VideoFileClip(filename)
        self.audio = mpe.AudioFileClip(audioname)
        self.overlay = mpe.VideoFileClip("assets/overlay.mov").subclip().resize(self.clip.size).set_opacity(0.40)
        self.resizeForTikTok = resizeForTikTok
        self.text_boolean = textBoolean
        self.word_type = wordType

    def audi_test(self):
        f = self.clip.set_audio(self.audio)
        f.write_videofile("out.mp4", temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac")
    def create(self, desired_length):

        if self.text_boolean == "y" :
            self.random_word_screen()

        while self.total_duration < desired_length:
            self.add_clip()
        final = mpe.concatenate_videoclips(self.clip_list)
        image = mpe.ImageClip("assets/blue.png").resize(self.clip.size).set_opacity(0.35).set_duration(self.total_duration)
        final = mpe.CompositeVideoClip([final, image])
        self.audio = self.audio.set_duration(self.total_duration)
        final = final.set_audio(self.audio)
        if self.resizeForTikTok == "y" :
            (w, h) = final.size
            if h == 1080 :
                cropClip = crop(final, width=607.50, height=1080, x_center=w/2, y_center=h/2)
                finalClip = cropClip.resize(height=1080)
            else :
                cropClip = crop(final, width=405, height=720, x_center=w/2, y_center=h/2)
                finalClip = cropClip.resize(height=720)
            finalClip.write_videofile("output_file.mp4", temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac")
        else :
            final.write_videofile("output_file.mp4", temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac")

    def add_clip(self):
        r = randint(0, floor(self.clip.duration-10))
        subclip = self.clip.subclip(r, r+(r%10))
        merged = mpe.CompositeVideoClip([subclip, self.overlay.subclip(2, 2+r%10)])
        if r%2==0: #adds a fade_in transition if r is even.
            merged = mpv.fx.all.fadein(merged, 3)
        self.clip_list.append(merged)
        self.total_duration += r%10

    def random_word_screen(self):
        if self.word_type == "sad" :
            r = randint(0, len(sad_word_list))
            word = sad_word_list[r]
        if self.word_type == "happy" :
            r = randint(0, len(happy_word_list))
            word = happy_word_list[r]
        if self.word_type == "dark" :
            r = randint(0, len(dark_word_list))
            word = dark_word_list[r]
        spaced_word = "  ".join([e for e in word])
        if self.resizeForTikTok == "y" :
            clip = mpe.TextClip(spaced_word, fontsize = 30, color = "white",size=self.clip.size,bg_color = "black",method="caption",align="center").set_duration(1.5)
            self.total_duration += 1.5
        else :
            clip = mpe.TextClip(spaced_word, fontsize = 50, color = "white",size=self.clip.size,bg_color = "black",method="caption",align="center").set_duration(2)
            self.total_duration += 2
        self.clip_list.append(clip)
            
movie_name = input("Filename of the Movie?: ")
song_name = input("Filename of the Song?: ")
movie_duration = int(input("How much seconds should it last?: "))
convert_to_tiktok = input("Resize for Tik Tok? (y/n): ")
text_boolean = input("Do you want the initial text screen? (y/n): ")
if text_boolean == "y" :
    word_type = input("What type of video is? (sad/happy/dark): ")
else :
    word_type = "None"        

g = Generator(movie_name, song_name, convert_to_tiktok, text_boolean, word_type)
g.create(movie_duration)
