import platform
from bs4 import BeautifulSoup
import requests

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

def get_lyrics(url):
    r = requests.get(url)
    # with open ('outfile.txt', 'w', encoding='utf-16') as outfile:
    #     outfile.write(r.text)
    soup = BeautifulSoup(r.text, "html.parser")
    lyrics_data = soup.find('div', class_='lyrics')
    return (lyrics_data.get_text())


if __name__ == '__main__':
    artist, track = get_song_windows()
    url = get_url(artist, track)
    lyrics = get_lyrics(url)
    print(lyrics)

