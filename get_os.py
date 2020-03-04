import platform
from bs4 import BeautifulSoup
import requests
import re

def main():
    current_platform = platform.system()

    if current_platform == 'Windows':
        get_song_windows()
    elif current_platform == 'Linux':
        get_song_linux()
    elif current_platform == 'Darwin':
        get_song_mac()
    else:
        print('Unidentified platform')


def get_song_windows():

    import win32gui

    # win2find = 'Spotify'  
    # whnd = win32gui.FindWindowEx(None, None, None, win2find)
    # if not (whnd == 0):
    #     print('Found')
    # else:
    #     print('Not found')
    title = []

    def winEnumHandler( hwnd, ctx ):
        """ 
        Callback function to handle EnumWindows
        hwnd is returned from the function win32gui.EnumWindows to get all Windows
        """
        if win32gui.IsWindowVisible( hwnd ):
            windowtext =  win32gui.GetWindowText(hwnd)
            classname = win32gui.GetClassName(hwnd)
            if classname == "Chrome_WidgetWin_0" and len(windowtext) > 0:
                title.append(windowtext)

    win32gui.EnumWindows( winEnumHandler, None )

    artist, track = title[0].split(" - ", 1)
    return artist, track

def get_url(artist, track):
    """
    Get Genius lyrics from artist and track
    """

    url = "https://genius.com/" + artist + '-' + track + '-lyrics'
    return url

def get_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup

def get_lyrics(url):
   
    # with open ('outfile.txt', 'w', encoding='utf-16') as outfile:
    #     outfile.write(r.text)
    soup = get_data(url)
    translation = soup.find('h3', class_="annotation_label")

    #If translation found
    if translation and translation.text == "Song Translations":
        a_string = soup.find(string=["English", "English Translation"])
        b  = a_string.find_parents("a")
        english_translate = (b[0].get("href"))
        translate_soup = get_data(english_translate)
        lyrics_data = translate_soup.find('div', class_='lyrics') 
        return (lyrics_data.get_text())
    else:
        lyrics_data = soup.find('div', class_='lyrics')
        return (lyrics_data.get_text())


def test_translation():
    with open('outfile.txt', 'r', encoding='utf-16' ) as infile:
        a = infile.read()
    
    #find translation
    soup = BeautifulSoup(a, 'html.parser')
    translation = soup.find('h3', class_="annotation_label")

    #If translation found
    if translation and translation.text == "Song Translations":
        a_string = soup.find("English")
        b  = a_string.find_parents("a")
        english_translate = (b[0].get("href"))
        return(get_lyrics(english_translate))


if __name__ == '__main__':
    artist, track = get_song_windows()
    url = get_url(artist, track)
    lyrics = get_lyrics(url)
    print(lyrics)

