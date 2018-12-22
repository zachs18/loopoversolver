#!/usr/bin/env python3
import loopover
import time
import sys

try:
	loopover.sleep_length = float(sys.argv[1])
except (ValueError, IndexError) as e:
	pass

line_count = input("Multiline input? (line count for yes, empty or non-int for no): ")
try:
	s = ""
	for i in range(int(line_count)):
		s += ' ' + input()
	board = loopover.Board(s)
except ValueError:
	boardstr = input("Board (space separated, newline terminated): ")
	board = loopover.Board(boardstr)

print("Please Alt-Tab to Loopover and select the top-left cell: ", end='')

wait_time = 4
for i in range(wait_time):
	print(wait_time-i, end='', flush=True)
	time.sleep(1)
	print('\x1b[D', end='')
print('Go!')

board.solve()
