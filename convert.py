import urllib.request
import tempfile
import json
from moviepy.editor import *
from bs4 import BeautifulSoup

#This case should pass. It's a mp4 file from gif file. 
#https://twitter.com/a19641sk/status/733608387770884096/
#This case should not be pass. It's a photo
#https://twitter.com/a19641sk/status/733614675225546752/
#This case should not be pass. It's a mp4 file with sound
#https://twitter.com/a19641sk/status/733615645145735169/
def convert(originalURL):
	identicalValue = originalURL.split('/')[-2]
	#simplifiedURL makes HTML parsing easily
	simplfiedURL = 'https://twitter.com/i/videos/tweet/'+ identicalValue
	#https://twitter.com/i/videos/tweet/733608387770884096
	response = urllib.request.urlopen(simplfiedURL)
	html = response.read()
	soup = BeautifulSoup(html, 'html.parser')
	try :
		mp4URL = json.loads(soup.body.find(id='playerContainer')['data-config'])['video_url']
	except TypeError as e : 
		print('This is a photo')
		return None
	mp4Response = urllib.request.urlopen(mp4URL)
	data = mp4Response.read()

	#If you have problems with clip, use this code for find error
	'''  
	with open ('test.mp4','wb') as test:
		test.write(data)
	''' 

	f = tempfile.NamedTemporaryFile()
	f.write(data)
	try : 
		clip = VideoFileClip(f.name)
	except OSError as e :
		print('The URL '+ originalURL +' is a movie')
		return None
	clip.write_gif('static/'+identicalValue+'.gif')
	return identicalValue+'.gif'

if __name__ == '__main__':
	convert(input())
