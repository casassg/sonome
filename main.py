#!./env/bin/python

import cmd
import json
import os
import random

import mingus.core.scales as scales
import requests
import tweepy
from mingus.containers import Track, Composition
from mingus.midi import fluidsynth
from tweepy import OAuthHandler, API

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN", "ENTER YOUR ACCESS TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET", "ENTER YOUR ACCESS TOKEN SECRET")
CONSUMER_KEY = os.environ.get("CONSUMER_KEY", "ENTER YOUR API KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET", "ENTER YOUR API SECRET")

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = API(auth)


def generate_composition(happy=True, energetic=False, text='Hola em dic Gerard'):
    t = Track()
    t.augment()
    if happy:
        scale = scales.Diatonic('C', (3, 7)).ascending()


    else:
        scale = scales.NaturalMinor("A").descending()

    if energetic:
        chords = []
        for st in text.split(' '):
            chords.append([scale[ord(i) % len(scale)] for i in st])
        t = Track().from_chords(chords[:1], 1)
    else:
        ns = [scale[ord(i) % len(scale)] if i != ' ' else None for i in text]
        amount = int(20 * (len(text) / 280.0))
        ns = ns[:amount]
        for note in ns:
            t.add_notes(note)

    c = Composition()
    c.add_track(t)
    return c


def is_text_happy(text):
    result = requests.post('http://text-processing.com/api/sentiment/', {'text': text}).json()['probability']
    return (result['pos'] - result['neg']) > 0


def random_line(afile):
    line = next(afile)
    for num, aline in enumerate(afile):
        if random.randrange(num + 2):
            continue
        line = aline
    return line


def get_random_tweet(line):
    filename = os.path.join(BASE_DIR, line + '.json')
    with open(filename, 'r') as f:
        tweet = json.loads(random_line(f))['text']
        tweet = ' '.join(w for w in tweet.lower().split() if 'http' not in w)
    return tweet


def get_tweets_user(line):
    filename = os.path.join(BASE_DIR, line + '.json')
    if not os.path.isfile(filename):
        with open(filename, 'w') as f:
            for tweet in tweepy.Cursor(api.user_timeline, id=line, count=200).items():
                json.dump(tweet._json, f)
                f.write("\n")
    return filename


class SonomeCmd(cmd.Cmd):
    """Simple command processor example."""
    intro = 'Welcome to the Sonome interactive shell. Type help or ? to list commands.\nAuthor: @casassaez 2017'
    prompt = 'sonome> '

    def do_about(self, line):
        """about\nPrints about information"""
        print("Sonome is a music generator that extracts sentiments from text and plays a song accordingly")

    def do_quit(self, line):
        return True

    def do_text(self, line):
        """text <text_to_analyze>\nCreate song for input text"""
        happy = is_text_happy(line)
        c = generate_composition(happy=happy, text=line)
        fluidsynth.play_Composition(c, bpm=280 if happy else 150)

    def do_user(self, line):
        """user <twitter_user_to_analyze>\nGets a random tweet from specified user and creates song"""
        get_tweets_user(line)
        tweet = get_random_tweet(line)
        happy = is_text_happy(tweet)
        print(tweet)
        c = generate_composition(happy=happy, text=tweet)
        fluidsynth.play_Composition(c, bpm=280 if happy else 150)

    def preloop(self):
        fluidsynth.init('choriumreva.sf2', "coreaudio")

    def postloop(self):
        print('Bye! see you soon?')


if __name__ == '__main__':
    SonomeCmd().cmdloop()
