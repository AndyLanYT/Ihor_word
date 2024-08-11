from gtts import gTTS
from playsound import playsound
import os
import glob
import time
import random


FILENAME = 'words.txt'
LANGUAGE = 'uk'
FINAL_QUESTION = 'Де ви бачите себе через 5 років?'
DURATION = 375


def pause(i):
    if i < 9:
        duration = 10
    
    elif 10 <= i < 18:
        duration = 8.5
    
    else:
        duration = max(8 - 0.6 * (i-18), 0.3)
    
    time.sleep(duration)


def words_from_file(filename):
    try:
        with open(filename, 'r', encoding='UTF-8') as f:
            return list(map(lambda word: word.rstrip(), f.readlines()))
        
    except FileNotFoundError:
        return []


def random_word(words, weights):
    idx = random.choices(range(len(weights)), weights)[0]
        
    word = words[idx]
    weights[idx] = weights[idx] // 2

    return word, idx


def create_soundfile(text, language, idx=None):
    filepath = f'sounds/{idx}.mp3'

    if not os.path.exists(filepath):
        gTTSobj = gTTS(text=text, lang=language)
        gTTSobj.save(filepath)
    
    return filepath


def words_to_speech(words, weights, language=LANGUAGE):
    start = time.time()
    i = 0
    
    while time.time() - start < DURATION:
        word, idx = random_word(words, weights)
        
        print(time.time() - start)
        print(word)
        
        filepath = create_soundfile(word, language, idx)
        playsound(filepath)

        pause(i)

        i += 1

    time.sleep(15)
    filepath = create_soundfile(FINAL_QUESTION, language, 'final')
    
    playsound(filepath)


def clear_folder():
    files = glob.glob(f'sounds/*')
    for f in files:
        os.remove(f)


time.sleep(7)

words = words_from_file(FILENAME)
weights = [2 ** 8 for _ in range(len(words))]

words_to_speech(words, weights)
clear_folder()
