from dataplicity.client.task import Task, onsignal
import urllib, urllib2, pycurl, subprocess
import pygame
import os
import glob

class Player(Task):
    SONG_END = pygame.USEREVENT + 1
    songs = [] 
    trackNumber = 0
    playlistPath = ""


    def play_track(self):
        if self.trackNumber < len(self.songs):
            print "Playing track {} ({}).".format(self.trackNumber + 1, self.songs[self.trackNumber])
            pygame.mixer.music.load(os.path.join(self.playlistPath, self.songs[self.trackNumber]))
            pygame.mixer.music.play()
            
    def pre_startup(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.set_endevent(self.SONG_END)
        
    @onsignal('settings_update', 'player')
    def on_settings_update(self, name, settings):        
        action  = settings.get_list('controls', 'action')[0]
        
        if action == 'play':
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.unpause()
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
            pygame.mixer.music.pause()

        elif action == 'stop':
            pygame.mixer.music.stop()

    def poll(self):
        """Called on a schedule defined in dataplicity.conf"""
        for event in pygame.event.get():
            if event.type == self.SONG_END:
                print "Track {} ({}) finished.".format(self.trackNumber + 1, self.songs[self.trackNumber])
                self.trackNumber += 1
                self.play_track

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
