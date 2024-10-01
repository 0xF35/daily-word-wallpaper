from requests import get
from bs4 import BeautifulSoup
from PIL import ImageGrab, Image, ImageFont, ImageDraw
import ctypes
from os import path, getcwd
from time import sleep

def create_wallpaper(word, defination):
	# Constants
	HEADING_FONT = 'Fonts\\BebasNeue.ttf'
	BODY_FONT = 'Fonts\\Montserrat.ttf'
	WALLPAPER_PATH = 'Wallpaper\\Wallpaper.bmp'
	# Capture Screenshot To Identify Screen Size
	SCREEN_WIDTH, SCREEN_HEIGHT = ImageGrab.grab().size
	# Create Screen Sized Black Image
	image = Image.new('RGB', (SCREEN_WIDTH, SCREEN_HEIGHT), (0, 0, 0))
	# Find FontSize Of Heading >= 10% Of Screen Height
	for i in range(1, 9999):
		heading_font = ImageFont.truetype(HEADING_FONT, i)
		if heading_font.getbbox(word)[-1] >= int(SCREEN_HEIGHT * 0.1):break
	# Set That Size As Heading Font Size
	heading_font = ImageFont.truetype(HEADING_FONT, i)
	# Get Heading Dimensions
	HEADING_WIDTH, HEADING_HEIGHT = heading_font.getbbox(word)[2:]
	# Create Draw Object On Image
	draw = ImageDraw.Draw(image)
	# Find FontSize Of Body >= 4% Of Screen Height
	for i in range(1, 9999):
		body_font = ImageFont.truetype(BODY_FONT, i)
		if body_font.getbbox(defination)[-1] >= int(SCREEN_HEIGHT * 0.04):break
	# Set That Size As Body Font Size
	body_font = ImageFont.truetype(BODY_FONT, i)
	# Get Body Dimensions
	BODY_WIDTH, BODY_HEIGHT = body_font.getbbox(defination)[2:]
	# Calculate Heading X & Y
	#            50% Screen Width   -  50% Heading Width
	HEADING_X = (SCREEN_WIDTH // 2) - (HEADING_WIDTH // 2)
	#            50% Screen Height   -  50% Heading Height   - 1.5x Body Height
	HEADING_Y = (SCREEN_HEIGHT // 2) - (HEADING_HEIGHT // 2) - (BODY_HEIGHT * 1.5)
	# Draw Heading to Image
	draw.text((HEADING_X, HEADING_Y), word, (200, 200, 200), font=heading_font)
	# Calculate Heading X & Y
	#         50% Screen Width   -  50% Body Width
	BODY_X = (SCREEN_WIDTH // 2) - (BODY_WIDTH // 2)
	#        Heading Y + Heading Height + 50% Body Height
	BODY_Y = HEADING_Y + HEADING_HEIGHT + (BODY_HEIGHT // 2)
	# Draw Body to Image
	draw.text((BODY_X, BODY_Y), defination, (160, 160, 160),font=body_font)
	# Save Image
	image.save(WALLPAPER_PATH)
	# Set Wallpaper Path As Default Wallpaper Path
	ctypes.windll.user32.SystemParametersInfoW(20, 0, path.join(getcwd(), WALLPAPER_PATH) , 0)

def get_word_of_the_day():
	# Fetch URL As Text Response
	r = get('https://www.dictionary.com/e/word-of-the-day').text
	# Parse Response As Html Parser
	soup = BeautifulSoup(r, 'html.parser')
	# Find Word Div
	word = soup.find_all('div', class_='otd-item-headword__word')[0].text.strip()
	# Find Defination
	defination = soup.find_all('div', class_='otd-item-headword__pos')[0].text.strip().split('\n')[-1]
	# Create Wallpaper
	create_wallpaper(word, defination)

if __name__ == '__main__':
	get_word_of_the_day()