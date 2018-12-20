import xdotool
import time

sleep_length = 0.07
sleep = lambda: time.sleep(sleep_length)

class Board:
	def __init__(self, _s):
		s=_s
		if 'a' in s.lower():
			s = s.replace('\n', '').replace(' ', '').lower()
			if len(s) in [1, 4, 9, 16, 25] and set(s) == set("abcdefghijklmnopqrstuvwxy"[:len(s)]):
				for i in range(25):
					s = s.replace(chr(ord('a')+i), str(1+i)+' ')
			else:
				raise ValueError(s)
		board = [int(i) for i in s.split()]
		if set(board) != set(range(1,len(board)+1)):
			raise ValueError(_s)
		i=0
		while i*i < len(board):
			i += 1
		if i*i != len(board):
			raise ValueError(_s)
		self.board = [board[i*j:i*(j+1)] for j in range(i)]
		self.width = self.height = i
		self.x, self.y = (0, 0)
		self.keys = ''
	def move(self, x=None, y=None):
		if x is not None:
			w = self.width
			left_dist = (self.x%w - x%w) % w
			right_dist = (x%w - self.x%w) % w
			if left_dist < right_dist:
				for i in range(left_dist):
					xdotool.key('j')
					self.keys += 'j'
					sleep()
			else:
				for i in range(right_dist):
					xdotool.key('l')
					self.keys += 'l'
					sleep()
			self.x = x % self.width
		if y is not None:
			h = self.height
			up_dist = (self.y%h - y%h) % h
			down_dist = (y%h - self.y%h) % h
			if up_dist < down_dist:
				for i in range(up_dist):
					xdotool.key('i')
					self.keys += 'i'
					sleep()
			else:
				for i in range(down_dist):
					xdotool.key('k')
					self.keys += 'k'
					sleep()
			self.y = y % self.width
	def swipe_up(self, col, dist):
		self.move(col, None)
		col = self.x # allow None argument for col
		dist %= self.height
		column = [self.board[i][col] for i in range(self.height)]
		column = column[dist:] + column[:dist]
		for i in range(self.height):
			self.board[i][col] = column[i]
		if not dist:
			pass
		elif dist < (-dist) % self.height:
			for i in range(dist):
				xdotool.key("w")
				self.y = self.y-1 % self.height
				self.keys += 'w'
				sleep()
		else:
			for i in range(self.height - dist):
				xdotool.key("s")
				self.y = self.y+1 % self.height
				self.keys += 's'
				sleep()
	def swipe_left(self, row, dist):
		self.move(None, row)
		row = self.y # allow None argument for row
		dist %= self.height
		row_ = self.board[row][dist:] + self.board[row][:dist]
		self.board[row] = row_
		if not dist:
			pass
		elif dist < (-dist) % self.width:
			for i in range(dist):
				xdotool.key("a")
				self.x = self.x-1 % self.width
				self.keys += 'a'
				sleep()
		else:
			for i in range(self.width - dist):
				xdotool.key("d")
				self.x = self.x+1 % self.width
				self.keys += 'd'
				sleep()
	def find(self, i_x, y=None):
		if y is None:
			i = i_x
		else:
			i = self.width*(y%self.height) + (i_x%self.width) + 1 # 0,0 is 1
		for r in range(len(self.board)):
			if i in self.board[r]:
				return self.board[r].index(i), r
		raise ValueError((i_x, y) if y is not None else i_x)
	def reverse(self):
		opposite = {
			'a':lambda: self.swipe_left(None, -1),
			'd':lambda: self.swipe_left(None, 1),
			's':lambda: self.swipe_up(None, 1),
			'w':lambda: self.swipe_up(None, -1),
			'j':lambda: self.move(self.x+1, None),
			'l':lambda: self.move(self.x-1, None),
			'k':lambda: self.move(None, self.y-1),
			'i':lambda: self.move(None, self.y+1)
		}
		for key in self.keys[::-1]:
			#xdotool.key(opposite[key])
			opposite[key]()
		self.keys = ""
	def solved_box(self, width=None, height=None):
		for x in range(width or self.width):
			for y in range(height or self.height):
				if (x,y) != self.find(x, y):
					return False
		return True
	def solve_box(self, width=None, height=None):
		if width is None and height is None:
			width, height = self.width-1, self.height-1
		if self.width <= width or self.height <= height:
			raise ValueError
		if self.solved_box(width, height):
			return
		if height > 1: # solve shorter box and solve remaining row
#		if height >= width > 1: # solve shorter box and solve remaining row
			self.solve_box(width, height-1)
			for i in range(width): # move needed to (i, height-1) without disturbing
				#Actually moves it to (i, height-1), but the other iterations of the loop will get it to (i, height-1)
				nx, ny = i, height-1
				x, y = self.find(nx, ny)
				print(nx, ny, 'is at', x, y)
				if y == ny:
					self.swipe_left(y, x-width) # get it to first unused column
					self.swipe_up(width, -1) # move down
					self.swipe_left(y, width-x) # get row back
					self.swipe_up(width, 1) # move back up
					self.swipe_left(ny, 1) # move in for the rest of the row
				elif y < ny:
					self.swipe_up(x, y-ny-1) # move to below current row
					self.swipe_left(ny+1, x-width) # move to just below where it needs to be
					self.swipe_up(width, 1) # move up
					print('left', y, 1)
					self.swipe_left(ny, 1) # move in for the rest of the row
				elif y > ny:
					self.swipe_left(y, x-width) # move to below where it needs to be
					self.swipe_up(width, y-ny) # move up
					self.swipe_left(ny, 1) # move in for the rest
		elif width > height >= 1: # solve thinner box and solve remaining column
			self.solve_box(width-1, height)
			for i in range(height): # move needed to (width-1, i) without disturbing
				#Actually moves it to (width-1, height-1), but the other iterations of the loop will get it to (width-1, i)
				nx, ny = width-1, i
				x, y = self.find(nx, ny)
				print(nx, ny, 'is at', x, y)
				if x == nx:
					print('x == nx')
					self.swipe_up(x, y-height)
					self.swipe_left(height, -1)
					self.swipe_up(x, height-y)
					self.swipe_left(height, 1)
					self.swipe_up(nx, 1)
				elif x < nx:
					print('x < nx')
					self.swipe_left(y, x-nx-1)
					self.swipe_up(nx+1, y-height)
					self.swipe_left(height, 1)
					self.swipe_up(nx, 1)
				elif x > nx:
					print('x > nx')
					self.swipe_up(x, y-height)
					self.swipe_left(height, x-nx)
					self.swipe_up(nx, 1)
		elif width == height == 1:
			x,y = self.find(1)
			print('1 is at', x, y)
			self.swipe_up(x, y)
			self.swipe_left(0, x)
		xdotool.key("space") # for grouping, doesnt affect game
		sleep()
	def solve_lastcol(self): # leaves keyhole
		if not self.solved_box(self.width-1, self.height-1):
			raise ValueError(self)
		for i in range(self.height-2): # move needed to (width-1, i)
			#Actually moves it to (width-1, height-1), but the other iterations of the loop will get it to (width-1, i)
			nx, ny = self.width-1, i
			x, y = self.find(nx, ny)
			if x == self.width-1: # loop it out on the bottom row, then get it where it needs to be
				self.swipe_up(self.width-1, y+1)
				self.swipe_left(self.height-1, 1)
				self.swipe_up(self.width-1, -y-1)
				self.swipe_left(self.height-1, -1)
				self.swipe_up(self.width-1, 1)
			elif y == self.height-1: # get it where it needs to be
				self.swipe_left(self.height-1, x+1)
				self.swipe_up(self.width-1, 1)
			else:
				raise ValueError(self)
		self.swipe_up(self.width-1, 1)
	def solve_keyhole(self):
		if not self.solved_box(self.width-1, self.height-1): # box
			raise ValueError(self)
		if not self.solved_box(self.width, self.height-2): # lastcol
			raise ValueError(self)
		key = None # self.board[-2][-1]
		keyloc = (None, None)
		def update_keyloc():
			nonlocal keyloc
			keyloc = self.find(key)
		lastcol_up = True # is lastcol aligned properly
		def swapkey():
			nonlocal key, lastcol_up
			if lastcol_up:
				self.swipe_up(-1, -1)
				lastcol_up = False
				key = self.board[0][-1]
				update_keyloc()
			else:
				self.swipe_up(-1, 1)
				lastcol_up = True
				key = self.board[-2][-1]
				update_keyloc()
		x, y = self.find(0, -1)
		if y == self.height-1: # not the key
			self.swipe_left(-1, x) # get leftmost cell aligned
			key = self.board[-2][-1]
			update_keyloc()
		else: # the key
			self.swipe_up(-1, -1)
			self.swipe_left(-1, x)
			lastcol_up = False
			key = self.board[0][1]
			update_keyloc()
		for i in range(1, self.width):
			x, y = self.find(i, -1)
			if (x,y) == keyloc:
				self.swipe_left(-1, i+1)
				swapkey()
				self.swipe_left(-1, -i-1)
			else:
				self.swipe_left(-1, x+1)
				swapkey()
				#self.swipe_left(-1, -x-1)
				#self.swipe_left(-1, i+1)
				#combined
				self.swipe_left(-1, i-x)
				swapkey()
				self.swipe_left(-1, -i-1)
