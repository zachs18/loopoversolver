#!/usr/bin/env python3
import loopover
import time
import sys

try:
	loopover.sleep_length = float(sys.argv[1])
except (ValueError, IndexError) as e:
	pass

line_count = input("Multiline input? (empty for no, line count for yes): ")
if not line_count:
	boardstr = input("Board (space separated, newline terminated): ")
	board = loopover.Board(boardstr)
else:
	s = ""
	for i in range(int(line_count)):
		s += ' ' + input()
	board = loopover.Board(s)

print("Please Alt-Tab to Loopover and select the top-left cell: ", end='')

wait_time = 4
for i in range(wait_time):
	print(wait_time-i, end='', flush=True)
	time.sleep(1)
	print('\x1b[D', end='')
print('Go!')

board.solve()
