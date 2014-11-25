#coding = utf-8

# RAFAEL VALER
# WILLIAM WEBER BERUTTI


import time
import sys
import random
import copy

from random import *

from base_client import LiacBot

INF = 1000000
WHITE = 1
BLACK = -1
NONE = 0

nivel = int(sys.argv[2])  # vamos ver

# BOT =========================================================================
class RandomBot(LiacBot):
	name = 'Silvio Santos'

	def __init__(self):
		super(RandomBot, self).__init__()
		self.last_move = None

	def on_move(self, state):
		print 'Generating a move...',
		board = Board(state)

		if state['bad_move']:
			print state['board']
			raw_input()
		
		
		move = board.alphabeta(nivel)
		
		self.last_move = move
		print move
		self.send_move(move[0], move[1])

		

	def on_game_over(self, state):
		print 'Game Over.'
		# sys.exit()
# =============================================================================

# MODELS ======================================================================
class Board(object):
	def __init__(self, state):
		self.cells = [[None for j in xrange(8)] for i in xrange(8)]
		self.my_pieces = []

		self.his_pieces = []
		
		self.state = state
		self.my_team = state['who_moves']
		PIECES = {
			'r': Rook,
			'p': Pawn,
			'b': Bishop,
			'q': Queen,
			'n': Knight,
		}


		c = state['board']
		i = 0

		for row in xrange(7, -1, -1):
			for col in xrange(0, 8):
				if c[i] != '.':
					cls = PIECES[c[i].lower()]
					team = BLACK if c[i].lower() == c[i] else WHITE

					piece = cls(self, team, (row, col))
					self.cells[row][col] = piece
					
					if team == self.my_team:
						self.my_pieces.append(piece)
					else: 
						self.his_pieces.append(piece)

				i += 1



	def __getitem__(self, pos):
		if not 0 <= pos[0] <= 7 or not 0 <= pos[1] <= 7:
			return None

		return self.cells[pos[0]][pos[1]]


	def alphabeta(self, niveis):
		

		#
		
		maior = -INF			
		moves = self.generate()  # gera todos os movimentos possiveis de cada peca
		
		
		for move in moves:
			
			c = self.movepiece(self.cells, move)  #c: armazena temporariamente o tabuleiro do movimento de uma peca
			aux = self.alfabeta(c, niveis-1, -INF, INF, False)
		
			if  aux > maior:
				maior = aux
				bestmove = move
		
		
		return bestmove	


    #ce: self.cells -> onde esta armazenado o tabuleiro com as pecas
	def alfabeta(self,ce, depth, alfa, beta, player):
		if depth == 0:  #or final
			return self.avalia(ce, player)
		
		if player:
			moves = self.generate()
		else:
			moves = self.generateEnemy()

		if player:
			
			for move in moves:
				
				c = self.movepiece(ce, move)
				alfa = max(alfa, self.alfabeta(c, depth-1, alfa, beta, False))
				if beta <= alfa:
					break
			return alfa
		else:
			
			for move in moves:
				
				c = self.movepiece(ce, move)
				beta = min(beta, self.alfabeta(c, depth-1, alfa, beta, True))
				if beta <= alfa:
				#if alfa <= beta:
					break
			return beta
			
	def avalia(self, cells, player):
		infinito = 5000
		whiteWin = False
		blackWin = False
		value = 0
		
		
		whitePawns = 0
		blackPawns = 0
		whiteRooks = 0
		blackRooks = 0
		whiteKnights = 0
		blackKnights = 0


		if self.my_team == 1:
		#time branco 
			for row in range(8):
				for col in range(8):
					piece = cells[row][col]
					if piece != None:
						
						if piece.team == self.my_team:
							if type(piece) == Rook:
								whiteRooks += 1
							if type(piece) == Knight:
								whiteKnights += 1
								if piece.position[1] == 3 or piece.position[1] == 4 or piece.position[1] == 5 or piece.position[1] == 6:
									value = value + 25
							if type(piece) == Pawn:
								if piece.position[0] == 7:
									whiteWin
								whitePawns +=1
								value = value - (7 - row)
						else:
							
							if type(piece) == Rook:
								blackRooks += 1
							if type(piece) == Knight:
								blackKnights += 1
							if type(piece) == Pawn:
								if piece.position[0] == 0:
									blackWin
								blackPawns +=1
								value = value - row


			if whitePawns == 0:
				blackWin = True
			elif blackPawns == 0:
				whiteWin = True

			
			if blackWin:
				value = -infinito
				return value
			elif whiteWin:
				value = infinito
				return value


			value = value + 10*(whitePawns - blackPawns) + 3*(whiteRooks - blackRooks) + 5*(whiteKnights - blackKnights)
			
			return value

		else:
		#time preto
			for row in range(8):
				for col in range(8):
					piece = cells[row][col]
					if piece != None:
						
						if piece.team == self.my_team:
							if type(piece) == Rook:
								blackRooks += 1
							if type(piece) == Knight:
								blackKnights += 1
								if piece.position[1] == 3 or piece.position[1] == 4 or piece.position[1] == 5 or piece.position[1] == 6:
									value = value + 25
							if type(piece) == Pawn:
								if piece.position[0] == 0:
									blackWin
								blackPawns +=1
								value = value - row 
								
						else:
							
							if type(piece) == Rook:
								whiteRooks += 1
							if type(piece) == Knight:
								whiteKnights += 1
							if type(piece) == Pawn:
								if piece.position[0] == 7:
									whiteWin
								whitePawns +=1
								value = value - (7 - row)
								


			if whitePawns == 0:
				blackWin = True
			elif blackPawns == 0:
				whiteWin = True
			
			if blackWin:
				print "black"
				value = infinito
				return value
			elif whiteWin:
				print "white"
				value = -infinito
				return value

			value = value + 10*(blackPawns - whitePawns) + 3*(blackRooks - whiteRooks) + 5*(blackKnights - whiteKnights)
			
			return value	



		


			
		

## Aparentemente certo ##
	def movepiece(self,c, move):
		


		cel = [[0 for x in range(8)] for x in range(8)]

		for i in range(0, 8):
			for j in range(0, 8):
				cel[i][j] = c[i][j]

		
		move1 = move[1]
		move0 = move[0]
		cel[move1[0]][move1[1]] = cel[move0[0]][move0[1]]
		cel[move0[0]][move0[1]] = None
		


		return cel
		
		


##

	def __setitem__(self, pos, value):
		self._cells[pos[0]][pos[1]] = value

	def is_empty(self, pos):
		return self[pos] is None

	def generate(self):
		moves = []
		for piece in self.my_pieces:
			ms = piece.generate()
			ms = [(piece.position, m) for m in ms]
			moves.extend(ms)

		return moves

	def generateEnemy(self):
		moves = []
		for piece in self.his_pieces:
			ms = piece.generate()
			ms = [(piece.position, m) for m in ms]
			moves.extend(ms)

		return moves

class Piece(object):
	def __init__(self):
		self.board = None
		self.team = None
		self.position = None
		self.type = None

	def generate(self):
		pass

	def is_opponent(self, piece):
		return piece is not None and piece.team != self.team

class Pawn(Piece):
	def __init__(self, board, team, position):
		self.board = board
		self.team = team
		self.position = position

	def generate(self):

		moves = []
		my_row, my_col = self.position

		d = self.team

        # Movement to 1 forward
		pos = (my_row + d*1, my_col)
		if self.board.is_empty(pos):
			moves.append(pos)

        # Normal capture to right
		pos = (my_row + d*1, my_col+1)
		piece = self.board[pos]
		if self.is_opponent(piece):
			moves.append(pos)

        # Normal capture to left
		pos = (my_row + d*1, my_col-1)
		piece = self.board[pos]
		if self.is_opponent(piece):
			moves.append(pos)

		return moves


        #moves = []
	

class Rook(Piece):
	def __init__(self, board, team, position):
		self.board = board
		self.team = team
		self.position = position
		
	def _col(self, dir_):
		my_row, my_col = self.position
		d = -1 if dir_ < 0 else 1
		for col in xrange(1, abs(dir_)):
			yield (my_row, my_col + d*col)

	def _row(self, dir_):
		my_row, my_col = self.position

		d = -1 if dir_ < 0 else 1
		for row in xrange(1, abs(dir_)):
			yield (my_row + d*row, my_col)

	def _gen(self, moves, gen, idx):
		for pos in gen(idx):
			piece = self.board[pos]

			if piece is None: 
				moves.append(pos)
				continue
			
			elif piece.team != self.team:
				moves.append(pos)

			break

	def generate(self):
		moves = []

		my_row, my_col = self.position
		self._gen(moves, self._col, 8-my_col) # RIGHT
		self._gen(moves, self._col, -my_col-1) # LEFT
		self._gen(moves, self._row, 8-my_row) # TOP
		self._gen(moves, self._row, -my_row-1) # BOTTOM

		return moves

class Bishop(Piece):
	def __init__(self, board, team, position):
		self.board = board
		self.team = team
		self.position = position

	def _gen(self, moves, row_dir, col_dir):
		my_row, my_col = self.position

		for i in xrange(1, 8):
			row = row_dir*i
			col = col_dir*i
			q_row, q_col = my_row+row, my_col+col

			if not 0 <= q_row <= 7 or not 0 <= q_col <= 7:
				break

			piece = self.board[q_row, q_col]
			if piece is not None:
				if piece.team != self.team:
					moves.append((q_row, q_col))
				break

			moves.append((q_row, q_col))

	def generate(self):
		moves = []

		self._gen(moves, row_dir=1, col_dir=1) # TOPRIGHT
		self._gen(moves, row_dir=1, col_dir=-1) # TOPLEFT
		self._gen(moves, row_dir=-1, col_dir=-1) # BOTTOMLEFT
		self._gen(moves, row_dir=-1, col_dir=1) # BOTTOMRIGHT

		return moves

class Queen(Piece):
	def __init__(self, board, team, position):
		self.board = board
		self.team = team
		self.position = position

	def _col(self, dir_):
		my_row, my_col = self.position
		
		d = -1 if dir_ < 0 else 1
		for col in xrange(1, abs(dir_)):
			yield (my_row, my_col + d*col)

	def _row(self, dir_):
		my_row, my_col = self.position

		d = -1 if dir_ < 0 else 1
		for row in xrange(1, abs(dir_)):
			yield (my_row + d*row, my_col)

	def _gen_rook(self, moves, gen, idx):
		for pos in gen(idx):
			piece = self.board[pos]
			
			if piece is None: 
				moves.append(pos)
				continue
			
			elif piece.team != self.team:
				moves.append(pos)

			break

	def _gen_bishop(self, moves, row_dir, col_dir):
		my_row, my_col = self.position

		for i in xrange(1, 8):
			row = row_dir*i
			col = col_dir*i
			q_row, q_col = my_row+row, my_col+col

			if not 0 <= q_row <= 7 or not 0 <= q_col <= 7:
				break

			piece = self.board[q_row, q_col]
			if piece is not None:
				if piece.team != self.team:
					moves.append((q_row, q_col))
				break

			moves.append((q_row, q_col))

	def generate(self):
		moves = []

		my_row, my_col = self.position
		self._gen_rook(moves, self._col, 8-my_col) # RIGHT
		self._gen_rook(moves, self._col, -my_col-1) # LEFT
		self._gen_rook(moves, self._row, 8-my_row) # TOP
		self._gen_rook(moves, self._row, -my_row-1) # BOTTOM
		self._gen_bishop(moves, row_dir=1, col_dir=1) # TOPRIGHT
		self._gen_bishop(moves, row_dir=1, col_dir=-1) # TOPLEFT
		self._gen_bishop(moves, row_dir=-1, col_dir=-1) # BOTTOMLEFT
		self._gen_bishop(moves, row_dir=-1, col_dir=1) # BOTTOMRIGHT

		return moves

class Knight(Piece):
	def __init__(self, board, team, position):
		self.board = board
		self.team = team
		self.position = position

	def _gen(self, moves, row, col):
		if not 0 <= row <= 7 or not 0 <= col <= 7:
			return

		piece = self.board[(row, col)]
		if piece is None or self.is_opponent(piece):
			moves.append((row, col))

	def generate(self):
		moves = []
		my_row, my_col = self.position

		self._gen(moves, my_row+1, my_col+2)
		self._gen(moves, my_row+1, my_col-2)
		self._gen(moves, my_row-1, my_col+2)
		self._gen(moves, my_row-1, my_col-2)
		self._gen(moves, my_row+2, my_col+1)
		self._gen(moves, my_row+2, my_col-1)
		self._gen(moves, my_row-2, my_col+1)
		self._gen(moves, my_row-2, my_col-1)

		return moves
# =============================================================================

if __name__ == '__main__':
	color = 0
	port = 50100

	if len(sys.argv) > 1:
		if sys.argv[1] == 'black':
			color = 1
			port = 50200
			
	#nivel = sys.argv[2]  # -> deu errado

	bot = RandomBot()
	bot.port = port

	bot.start()






