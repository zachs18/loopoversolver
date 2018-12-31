try:
	#raise ModuleNotFoundError # to force xdotool if you want
	import pyautogui
	key = pyautogui.press
	type = pyautogui.typewrite
except ModuleNotFoundError:
	import subprocess
	import time

	def key(keystroke, window=None, clearmodifiers=False, delay=None):
		cmdline = "xdotool key"
		if window is not None:
			cmdline += " --window %s" % window
		if clearmodifiers:
			cmdline += " --clearmodifers"
		if delay is not None:
			cmdline += " --delay %s" % delay
		cmdline += " %s" % keystroke
		subprocess.Popen(cmdline.split()).wait()
	def keydown(keystroke, window=None, clearmodifiers=False, delay=None):
		cmdline = "xdotool keydown"
		if window is not None:
			cmdline += " --window %s" % window
		if clearmodifiers:
			cmdline += " --clearmodifers"
		if delay is not None:
			cmdline += " --delay %s" % delay
		cmdline += " %s" % keystroke
		subprocess.Popen(cmdline.split()).wait()
	def keyup(keystroke, window=None, clearmodifiers=False, delay=None):
		cmdline = "xdotool keyup"
		if window is not None:
			cmdline += " --window %s" % window
		if clearmodifiers:
			cmdline += " --clearmodifers"
		if delay is not None:
			cmdline += " --delay %s" % delay
		cmdline += " %s" % keystroke
		subprocess.Popen(cmdline.split()).wait()
	def type(*strings, window=None, clearmodifiers=False, delay=None):
		if not strings:
			return
		cmdline = "xdotool type"
		if window is not None:
			cmdline += " --window %s" % window
		if clearmodifiers:
			cmdline += " --clearmodifers"
		if delay is not None:
			cmdline += " --delay %s" % delay
		subprocess.Popen(cmdline.split() + list(strings)).wait()

	mouse_previous_location = (None, None)

	def mousemove(x=None, y=None, window=None, screen=None, polar=False, clearmodifers=False, sync=True):
		cmdline = "xdotool mousemove"
		if y is None:
			if x == 'restore' or x is None:
				x, y = mouse_previous_location
				loc_str = " %s %s" % (x, y)
			else:
				raise TypeError("mousemove takes 0 or 2 int arguments or 1 argument 'restore'")
		elif not isinstance(x, int) or not isinstance(y, int):
			raise TypeError("mousemove takes 0 or 2 int arguments or 1 argument 'restore'")
		else:
			loc_str = " %s %s" % (x, y)
		if window is not None:
			cmdline += " --window %s" % window
		if screen is not None:
			cmdline += " --screen %s" % screen
		if polar and y is not None:
			cmdline += " --polar"
		if clearmodifiers:
			cmdline += " --clearmodifers"
		if sync:
			cmdline += " --sync"
		cmdline += loc_str
		subprocess.Popen(cmdline.split()).wait()
	def mousemove_relative(x=None, y=None, window=None, screen=None, polar=False, clearmodifers=False, sync=True):
		if y is None:
			if x == 'restore' or x is None:
				x, y = mouse_previous_location
				loc_str = " %s %s" % (x, y)
			else:
				raise TypeError("mousemove takes 0 or 2 int arguments or 1 argument 'restore'")
		elif not isinstance(x, int) or not isinstance(y, int):
			raise TypeError("mousemove takes 0 or 2 int arguments or 1 argument 'restore'")
		else:
			loc_str = " %s %s" % (x, y)
		cmdline = "xdotool mousemove_relative"
		if window is not None:
			cmdline += " --window %s" % window
		if screen is not None:
			cmdline += " --screen %s" % screen
		if polar and y is not None:
			cmdline += " --polar"
		if clearmodifiers:
			cmdline += " --clearmodifers"
		if sync:
			cmdline += " --sync"
		cmdline += loc_str
		subprocess.Popen(cmdline.split()).wait()
	def click(button, clearmodifiers=False, repeat=None, delay=None, window=None):
		cmdline = "xdotool click"
		if clearmodifiers:
			cmdline += " --clearmodifers"
		if repeat is not None:
			cmdline += " --repeat %s" % repeat
		if delay is not None:
			cmdline += " --delay %s" % delay
		if window is not None:
			cmdline += " --window %s" % window
		cmdline += " %s" % button
		subprocess.Popen(cmdline.split()).wait()
	def mousedown(button, clearmodifiers=False, repeat=None, delay=None, window=None):
		cmdline = "xdotool mousedown"
		if clearmodifiers:
			cmdline += " --clearmodifers"
		if repeat is not None:
			cmdline += " --repeat %s" % repeat
		if delay is not None:
			cmdline += " --delay %s" % delay
		if window is not None:
			cmdline += " --window %s" % window
		cmdline += " %s" % button
		subprocess.Popen(cmdline.split()).wait()
	def mouseup(button, clearmodifiers=False, repeat=None, delay=None, window=None):
		cmdline = "xdotool mouseup"
		if clearmodifiers:
			cmdline += " --clearmodifers"
		if repeat is not None:
			cmdline += " --repeat %s" % repeat
		if delay is not None:
			cmdline += " --delay %s" % delay
		if window is not None:
			cmdline += " --window %s" % window
		cmdline += " %s" % button
		subprocess.Popen(cmdline.split()).wait()
	def getmouselocation():
		out, err = subprocess.Popen("xdotool getmouselocation".split(), stdout=subprocess.PIPE).communicate()
		x, y, screen, window = [i[i.index(':')+1:] for i in out.split()]
		return (x, y, screen, window)
