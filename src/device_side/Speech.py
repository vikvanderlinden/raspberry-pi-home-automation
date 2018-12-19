import requests as url
from pygame import mixer, time


def say(text=""):
    """
        Fetches a file with the spoken specified text,
        stores it and plays it
    """
    if text == "":
        return

    with open('speech/speech.mp3', 'wb') as handle:
        file = url.get(
            'http://translate.google.com/translate_tts?ie=YTF-8&total=1&idx=0&textlen=' + \
            str(len(text)) + '&client=tw-ob&q=' + text + '&tl=En-us', stream=True)

        if not file.ok:
            print('error')
        for block in file.iter_content(1024):
            handle.write(block)

    mixer.init()
    mixer.music.load('/home/pi/Documents/python-programs/Controls/speech/speech.mp3')
    mixer.music.play()

    while mixer.music.get_busy():
        time.Clock().tick(10)
