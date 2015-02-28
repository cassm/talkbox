from dataplicity.client.task import Task, onsignal
import urllib, urllib2, pycurl, subprocess
import pygame
from pygame.mixer import music
import goslate
import os
import glob
SONG_END = pygame.USEREVENT + 1

class Player(Task):

    songs = [] 
    trackNumber = 0
    playlistPath = ""

    def play_track(self):
        if self.trackNumber < len(self.songs):
            print "Playing track {} ({}).".format(self.trackNumber + 1, self.songs[self.trackNumber])
            music.load(os.path.join(self.playlistPath, self.songs[self.trackNumber]))
            music.play()
            
    def pre_startup(self):
        pygame.init()
        pygame.mixer.init()
        music.set_endevent(SONG_END)
        endtype = music.get_endevent() 

    @onsignal('settings_update', 'player')
    def on_settings_update(self, name, settings):        
        action  = settings.get_list('controls', 'action')[0]
        
        if action == 'play':
            if music.get_busy():
                music.unpause()
            else:
                inputPath = settings.get_list('path', 'path')[0]
                self.playlistPath = inputPath
                self.songs = []
                for songName in os.listdir(inputPath):
                    if ".mp3" in songName:
                        self.songs.append(songName)
                self.songs.sort()
                self.trackNumber = 0
                self.play_track()
                
        elif action == 'pause':
            music.pause()

        elif action == 'stop':
            music.stop()

    def poll(self):
        """Called on a schedule defined in dataplicity.conf"""
        for event in pygame.event.get():
            if event.type == SONG_END:
                self.trackNumber += 1
                self.play_track()

    def do_sample(self, value):
        """something"""
        #self.client.sample_now(self.sampler, value)

class Parrot(Task):
    """Samples a sin wave"""
    lastPhrase = "Test text"
    lang = "en"

    def downloadFile(self, url, fileName):
        fp = open(filename, "wb")
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, url)
        curl.setopt(pycurl.WRITEDATA, fp)
        curl.perform()
        curl.close()
        fp.close()

    def translatePhrase(self, phrase, lang):
        gs = goslate.Goslate()
        phrase = gs.translate(phrase, lang)
        return phrase

    def splitPhrase(self, phrase, length):
        phraseList = []
        while len(phrase) > length:
            phrasePart = phrase[:length].rsplit(' ', 1)[0]
            phraseList.append(phrasePart)
            phrase = phrase[len(phrasePart):]
            if phrase[0] == ' ':
                phrase = phrase[1:]
        phraseList.append(phrase)
        return phraseList
            
    def getGoogleSpeechURL(self, phraseSet, lang):
        urlSet = []
        for phrase in phraseSet:
            encodedPhrase = urllib.quote(phrase.encode('utf8'))          
            googleTranslateURL = "http://translate.google.com/translate_tts?ie=UTF-8&"
            parameters = {'q': encodedPhrase, 'tl': lang}
            data = urllib.urlencode(parameters)
            googleTranslateURL = "%s%s" % (googleTranslateURL, data)
            urlSet.append(googleTranslateURL)
            print googleTranslateURL
        return urlSet

    def speakText(self):
        translatedPhrase = self.translatePhrase(self.phrase, self.lang)
        phraseSet = self.splitPhrase(translatedPhrase, 100)
        urlSet = self.getGoogleSpeechURL(phraseSet, self.lang)
        subprocess.call(["mplayer"] + urlSet, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def pre_startup(self):
        """Called prior to running the project"""
        #self.phrase = settings.get_list(self.sampler, 'phrase')[0]
        #self.phrase = "Parrot online."
        #self.speakText()
        # self.conf contains the data- constants from the conf
        # self.sampler = self.conf.get('sampler')

    @onsignal('settings_update', 'talkbox')
    def on_settings_update(self, name, settings):
        # This signal is sent on startup and whenever settings are changed by the server
        self.phrase = settings.get_list('parrot', 'phrase')[0]
        self.lang = settings.get_list('parrot', 'lang')[0]
        self.lastPhrase = self.phrase
        self.speakText()


    def poll(self):
        """Called on a schedule defined in dataplicity.conf"""
        #value = math.sin(time() * self.frequency) * self.amplitude
        #self.do_sample(value)

    def do_sample(self, value):
        """something"""
        #self.client.sample_now(self.sampler, value)
