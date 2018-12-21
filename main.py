import loopover, time
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
