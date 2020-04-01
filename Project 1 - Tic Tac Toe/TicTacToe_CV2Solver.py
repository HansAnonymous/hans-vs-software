import cv2
import numpy as np
import pyscreenshot as ImageGrab
import imutils

scale = 0.7 #thx wito
debug = False
grid = [[None, None, None, None], [None, None, None], [None, None, None]]

def main():
	# take screenshot
	scr = cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_RGB2BGR)

	# resize screenshot
	scr = imutils.resize(scr, width=int(scr.shape[1]*scale))
	# convert to grayscale
	scr_gray = cv2.cvtColor(scr, cv2.COLOR_BGR2GRAY)

	# grab image to match with
	template = cv2.imread('match.jpg', 0)

	# resize matching image
	template = imutils.resize(template, width=int(template.shape[1]*scale))
	w, h = template.shape[::-1]

	res = cv2.matchTemplate(scr_gray, template, cv2.TM_CCOEFF_NORMED)
	threshold = 0.96

	loc = np.where(res >= threshold)

	found = False
	for pt in zip(*loc[::-1]):
		found = True
		if debug:
			print("pt @", pt)
			cv2.rectangle(scr, (pt[0], pt[1]), (pt[0] + w, pt[1] + h), (0,255,255), 2)

	if found:
		if debug:
			cv2.imshow('Detected', scr)
			if cv2.waitKey() & 0xFF == ord('q'):
				cv2.destroyAllWindows()

		print(grid.count(None))
main()