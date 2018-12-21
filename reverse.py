#!/usr/bin/env python3
import loopover
_s = input("Board to go back to (spaces separate, newline terminates): ")
board = loopover.Board(_s)
solved = [[board.width*j+k+1 for k in range(board.width)] for j in range(board.height)]
reversed =[[None]*board.width for i in range(board.height)]
for i in range(1, board.width*board.height+1):
	x, y = board.find(i)
	i -= 1
	reversed[i//board.width][i%board.width] = solved[y][x]
if board.width*board.height <= 26:
	# letters
	outstr = ""
	for row in reversed:
		outstr += ''.join(chr(ord('a')+i-1) for i in row) + ' '
	print("New Board:", outstr)
else:
	# numbers
	outstr = ""
	for row in reversed:
		outstr += ' '.join(str(i) for i in row) + '  '
	print("New Board:", outstr)
