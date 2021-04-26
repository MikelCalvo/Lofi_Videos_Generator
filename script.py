import moviepy.editor as mpe
import moviepy.video as mpv
from moviepy.video.fx.all import crop
from random import randint
from math import floor
from assets.wordlists.sad_words import sad_word_list
from assets.wordlists.happy_words import happy_word_list
from assets.wordlists.dark_words import dark_word_list

class Generator:
    def __init__(self, filename, audioname, outputFileName, resizeForTikTok, textBoolean, wordType, colorEffect, opacityEffect, textDuration):
        self.total_duration = 0
        self.clip_list = []
        self.clip = mpe.VideoFileClip(filename)
        self.audio = mpe.AudioFileClip(audioname)
        self.output_file_name = outputFileName
        self.overlay = mpe.VideoFileClip("assets/overlay.mov").subclip().resize(self.clip.size).set_opacity(0.40)
        self.resizeForTikTok = resizeForTikTok
        self.text_boolean = textBoolean
        self.word_type = wordType
        self.colorEffect = colorEffect
        self.opacity_effect = opacityEffect
        self.text_duration = textDuration

    def audi_test(self):
        f = self.clip.set_audio(self.audio)
        f.write_videofile("out.mp4", temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac")
    def create(self, desired_length):

        if self.text_boolean == "y" :
            self.random_word_screen()

        while self.total_duration < desired_length:
            self.add_clip()
        final = mpe.concatenate_videoclips(self.clip_list)
        image = mpe.ImageClip("assets/colors/" + self.colorEffect + ".png").resize(self.clip.size).set_opacity(self.opacity_effect).set_duration(self.total_duration)
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
            finalClip.write_videofile("TikTok_" + self.output_file_name + ".mp4", temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac")
        else :
            final.write_videofile(self.output_file_name + ".mp4", temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac")

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
            clip = mpe.TextClip(spaced_word, fontsize = 30, color = "white",size=self.clip.size,bg_color = "black",method="caption",align="center").set_duration(self.text_duration)
        else :
            clip = mpe.TextClip(spaced_word, fontsize = 50, color = "white",size=self.clip.size,bg_color = "black",method="caption",align="center").set_duration(self.text_duration)

        self.total_duration += self.text_duration
        self.clip_list.append(clip)
            
TEXT_BOLD = "\033[1m"
TEXT_BLUE = "\033[94m"
TEXT_FORMAT_END = "\033[0m"

print("")
print(TEXT_BOLD + TEXT_BLUE + "/********************************" + TEXT_FORMAT_END)
print(TEXT_BOLD + TEXT_BLUE + " *Social Media Content Generator*" + TEXT_FORMAT_END)
print(TEXT_BOLD + TEXT_BLUE + " ********************************/" + TEXT_FORMAT_END)
print("")

movie_name = input(TEXT_BOLD + "Filename of the Movie?: " + TEXT_FORMAT_END)
song_name = input(TEXT_BOLD + "Filename of the Song?: " + TEXT_FORMAT_END)
output_file_name = input(TEXT_BOLD + "Filename of the generate Movie?: " + TEXT_FORMAT_END)
movie_duration = int(input(TEXT_BOLD + "How much seconds should it last?: " + TEXT_FORMAT_END))
resizeForTikTok = input(TEXT_BOLD + "Resize for Tik Tok? (y/n): ")
text_boolean = input(TEXT_BOLD + "Do you want the initial text screen? (y/n): " + TEXT_FORMAT_END)
if text_boolean == "y" :
    text_duration = float(input(TEXT_BOLD + "How many seconds do you want for the initial screen? (ex: 1.5): " + TEXT_FORMAT_END))
    word_type = input(TEXT_BOLD + "What type of video do you want? (type 'list' to see the available types): " + TEXT_FORMAT_END)
    if word_type == "list" :
        word_type = input(TEXT_BOLD + "Available types: sad, happy or dark. What type of video do you want?: " + TEXT_FORMAT_END)
else :
    word_type = "None"
    text_duration = 0
colorEffect = input(TEXT_BOLD + "What color effect do you want? (type 'list' to see the available colors): " + TEXT_FORMAT_END)
if colorEffect == "list" :
    colorEffect = input(TEXT_BOLD + "Available colors: red, white, dark, blue, navy, orange, pink or yellow. What color effect do you want?: " + TEXT_FORMAT_END)      
opacity_effect = float(input(TEXT_BOLD + "How much opacity do you want for the color effect? (ex:0.30) (you can select 'd' for default opacity): " + TEXT_FORMAT_END))
if opacity_effect == "d" :
    opacity_effect = 0.30

g = Generator(movie_name, song_name, output_file_name, resizeForTikTok, text_boolean, word_type, colorEffect, opacity_effect, text_duration)
g.create(movie_duration)
