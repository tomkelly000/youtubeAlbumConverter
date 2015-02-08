''' youtubeAlbumParser.py
    A python script for parsing a youtube album into individual songs
    First argument is url of video
    Second argument is the name for the songs
    Tom Kelly '''

from bs4 import * # beautiful soup
import sys
import urllib2
import re

try:
  url = sys.argv[1]
except:
  url = raw_input('Enter a url: ')

try:
    album = urllib2.urlopen(url)
except:
    sys.stderr.write('Could not open ' + url + '\n')
    sys.exit()

soup = BeautifulSoup(album.read())
description = soup.find(id='eow-description')

timePattern = '\d*:\d*'
timeRE = re.compile(timePattern)

# sometimes youtubers include end times or durations on same line as start time
# so we must parse this out
times = []
newLine = True
for tag in description.contents:
  if not tag.string:
    newLine = True
    continue

  if newLine:
    if timeRE.match(tag.string):
      times.append(tag.string)
      newLine = False


index = url.find('=')
videoID = url[index+1:]
index = videoID.find('&')
if index > 0:
  videoID = videoID[:index]


import subprocess
subprocess.call(['youtube-dl', '--extract-audio', '--id', url]) # convert the video

def seconds(time):
  digits = time.split(':')
  if len(digits) < 2:
    return int(time)
  if len(digits) < 3:
    return 60 * int(digits[0]) + int(digits[1])
  else:
    return 60 * 60 * int(digits[0]) + 60 * int(digits[1]) + int(digits[2])
  return 0

try:
  name = sys.argv[2]
except:
  name = videoID

for i in range(len(times)):
  if i < len(times) - 1:
    subprocess.call(['ffmpeg', '-ss', times[i], '-i', './' + videoID + '.m4a', '-vn', '-c', 'copy', '-t', str(seconds(times[i+1])-seconds(times[i])-1), str(i) + name + '.m4a'])
  else:
    subprocess.call(['ffmpeg', '-ss', times[i], '-i', './' + videoID + '.m4a', '-vn', '-c', 'copy', str(i) + name + '.m4a'])




