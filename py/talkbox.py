from dataplicity.client.task import Task, onsignal
import urllib, urllib2, pycurl, subprocess
import pygame
import os
import glob

class Player(Task):
    pathChanged = True 
    lastAction = "stop"
    songs = [] 

    def pre_startup(self):
        pygame.mixer.init()
        
    @onsignal('settings_update', 'player')
    def on_settings_update(self, name, settings):
        # This signal is sent on startup and whenever settings are changed by the server
        if self.pathChanged:
            inputPath = settings.get_list('controls', 'path')[0]
            self.songs = []
            for songName in os.listdir(inputPath):
                if ".mp3" in songName:
                    self.songs.append(songName)

            self.pathChanged = False
            trackNumber = 0

        action  = settings.get_list('controls', 'action')[0]
        
        if action != self.lastAction:
            self.lastAction = action

            if action == 'play':
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.unpauseMusic()
                else:
                    pygame.mixer.music.load(os.path.join(inputPath, songs[trackNumber]))
                    pygame.mixer.music.play()
                
            elif action == 'pause':
                pygame.mixer.music.pauseMusic()

            elif action == 'stop':
                pygame.mixer.music.stop()

    def poll(self):
        """Called on a schedule defined in dataplicity.conf"""
        #value = math.sin(time() * self.frequency) * self.amplitude
        #self.do_sample(value)

    def do_sample(self, value):
        """something"""
        #self.client.sample_now(self.sampler, value)

class Parrot(Task):
    """Samples a sin wave"""
    lastPhrase = "Test text"

    def downloadFile(self, url, fileName):
        fp = open(filename, "wb")
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, url)
        curl.setopt(pycurl.WRITEDATA, fp)
        curl.perform()
        curl.close()
        fp.close()

    def getGoogleSpeechURL(self, phrase):
        googleTranslateURL = "http://translate.google.com/translate_tts?tl=en&"
        parameters = {'q': phrase}
        data = urllib.urlencode(parameters)
        googleTranslateURL = "%s%s" % (googleTranslateURL, data)
        return googleTranslateURL

    def speakText(self):
        googleSpeechURL = self.getGoogleSpeechURL(self.phrase)
        subprocess.call(["mplayer", googleSpeechURL], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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
        if self.phrase != self.lastPhrase:
            self.lastPhrase = self.phrase
            self.speakText()


    def poll(self):
        """Called on a schedule defined in dataplicity.conf"""
        #value = math.sin(time() * self.frequency) * self.amplitude
        #self.do_sample(value)

    def do_sample(self, value):
        """something"""
        #self.client.sample_now(self.sampler, value)
