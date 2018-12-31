try:
	#raise ModuleNotFoundError # to force xdotool if you want
	import pyautogui
	key = pyautogui.press
	type = pyautogui.typewrite
except ModuleNotFoundError:
	import shutil
	if shutil.which("xdotool") is None:
		import functools
		import sys
		#raise ImportWarning("Neither pyautogui nor xdotool is installed")
		print("Neither pyautogui nor xdotool could be found; Typing to stderr")
		key = type = functools.partial(print, file=sys.stderr, flush=True)
	else:
		import subprocess

		def key(keystroke):
			cmdline = "xdotool key %s" % keystroke
			subprocess.Popen(cmdline.split()).wait()
		def type(string):
			if not string:
				return
			cmdline = "xdotool type"
			subprocess.Popen(cmdline.split() + [string]).wait()
