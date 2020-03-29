#!/usr/bin/env python3
import pygame

from pygame.locals import *

pygame.init()

SCREEN_WIDTH = 640 # Default 640
SCREEN_HEIGHT = 480 # Default 480

BRUSH_WIDTH = 5

BGRD_COLOR = (42, 42, 42)
ACCENT_COLOR = (100, 200, 255)
ACCENT_COLOR2 = (80, 80, 80)
ACCENT_COLOR3 = (80, 80, 80, 192)
TEXT_COLOR = (230, 230, 230)

GRID_PAD = 40
BOX_PAD = 30

RIGHT_PAD = SCREEN_WIDTH - GRID_PAD - (SCREEN_HEIGHT - 2 * GRID_PAD)
GRID_WIDTH = SCREEN_WIDTH - GRID_PAD - RIGHT_PAD
GRID_HEIGHT = SCREEN_HEIGHT - 2 * GRID_PAD

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

font = pygame.font.SysFont("ubuntu", 16)

clock = pygame.time.Clock()

class TicTacToe(object):
	def __init__(self):
		self.sw = SCREEN_WIDTH
		self.sh = SCREEN_HEIGHT

		self.running = True
		self.playing = True

		self.clicked = False
		self.clickCircle = 1

		self.p1Wins = 0
		self.p2Wins = 0

		self.player = 1
		self.board = [[None, None, None], [None, None, None], [None, None, None]]

		self.Main()

	def Main(self):

		pygame.display.set_caption("Tic Tac Toe")


		def drawBox():
			# This draws a border *outside* of the rect. This helps setting the x and y overall
			pygame.draw.rect(screen, ACCENT_COLOR, pygame.Rect(GRID_PAD - BRUSH_WIDTH, GRID_PAD - BRUSH_WIDTH, GRID_PAD + GRID_WIDTH - GRID_PAD + 2 * BRUSH_WIDTH, GRID_PAD + GRID_HEIGHT - GRID_PAD + 2 * BRUSH_WIDTH)) # I'm going to ignore the fact that the last parameter is also brush width and can make the rect not filled in
			pygame.draw.rect(screen, BGRD_COLOR, pygame.Rect(GRID_PAD,	GRID_PAD, GRID_PAD + GRID_WIDTH - GRID_PAD, GRID_PAD + GRID_HEIGHT - GRID_PAD))

		def drawGrid():
			pygame.draw.line(screen, ACCENT_COLOR,	(GRID_PAD + GRID_WIDTH / 3, GRID_PAD),	(GRID_PAD + GRID_WIDTH / 3,GRID_PAD + GRID_HEIGHT),	BRUSH_WIDTH)
			pygame.draw.line(screen, ACCENT_COLOR,	(GRID_PAD + GRID_WIDTH * 2 / 3, GRID_PAD),	(GRID_PAD + GRID_WIDTH * 2 / 3,GRID_PAD + GRID_HEIGHT),	BRUSH_WIDTH)
			pygame.draw.line(screen, ACCENT_COLOR, (GRID_PAD, GRID_PAD + GRID_HEIGHT / 3), (GRID_PAD + GRID_WIDTH, GRID_PAD + GRID_HEIGHT / 3), BRUSH_WIDTH)
			pygame.draw.line(screen, ACCENT_COLOR,	(GRID_PAD, GRID_PAD + GRID_HEIGHT * 2 / 3), (GRID_PAD + GRID_WIDTH, GRID_PAD + GRID_HEIGHT * 2 / 3), BRUSH_WIDTH)

		def drawRestart():
			btn_x = SCREEN_WIDTH - RIGHT_PAD + GRID_PAD
			btn_y = SCREEN_HEIGHT - 2 * GRID_PAD
			btn_width = RIGHT_PAD - 2 * GRID_PAD + BRUSH_WIDTH
			btn_height = GRID_PAD + BRUSH_WIDTH
			pygame.draw.rect(screen, ACCENT_COLOR, pygame.Rect(btn_x, btn_y, btn_width, btn_height))
			text = font.render("Restart", True, BGRD_COLOR)
			screen.blit(text, (btn_x + btn_width // 2 - text.get_width() // 2, btn_y + btn_height // 2 - text.get_height() // 2))

		def drawWin():
			surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT / 3 - GRID_PAD), pygame.SRCALPHA)
			surf.fill(ACCENT_COLOR3)
			f = pygame.font.SysFont("ubuntu", 42)
			text = f.render("Player " + str(self.player) + " has won!", True, ACCENT_COLOR)
			surf.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, (SCREEN_HEIGHT // 3 - GRID_PAD) // 2 - text.get_height() // 2))
			screen.blit(surf, (0, SCREEN_HEIGHT / 3 + GRID_PAD // 2))
			
		def drawCross(gridX, gridY):
			x = GRID_PAD + BOX_PAD + gridX * GRID_WIDTH / 3
			y = GRID_PAD + BOX_PAD + gridY * GRID_HEIGHT / 3
			x2 = GRID_PAD - BOX_PAD + (gridX + 1) * GRID_WIDTH / 3
			y2 = GRID_PAD - BOX_PAD + (gridY + 1) * GRID_HEIGHT / 3

			pygame.draw.line(screen, ACCENT_COLOR, (x, y), (x2,y2), BRUSH_WIDTH)
			pygame.draw.line(screen, ACCENT_COLOR, (x2, y), (x, y2), BRUSH_WIDTH)

		def drawCircle(gridX, gridY):
			x = GRID_PAD + (GRID_WIDTH / 6) + gridX * GRID_WIDTH / 3
			y = GRID_PAD + (GRID_HEIGHT / 6) + gridY * GRID_HEIGHT / 3
			r = (GRID_HEIGHT / 6) - (BOX_PAD / 2)
			pygame.draw.circle(screen, ACCENT_COLOR, (int(x), int(y)), int(r), BRUSH_WIDTH)

		def drawText():
			text = font.render("It is Player " + str(self.player) + "'s turn", True, TEXT_COLOR)
			screen.blit(text, (SCREEN_WIDTH - RIGHT_PAD + GRID_PAD, GRID_PAD - BRUSH_WIDTH))
			text = font.render("Player 1 = O", True, TEXT_COLOR)
			screen.blit(text, (SCREEN_WIDTH - RIGHT_PAD + GRID_PAD, GRID_PAD - BRUSH_WIDTH + 3 * text.get_height()))
			text = font.render("Player 2 = X", True, TEXT_COLOR)
			screen.blit(text, (SCREEN_WIDTH - RIGHT_PAD + GRID_PAD, GRID_PAD - BRUSH_WIDTH + 4 * text.get_height()))
			text = font.render("Player 1: " + str(self.p1Wins) + " wins", True, TEXT_COLOR)
			screen.blit(text, (SCREEN_WIDTH - RIGHT_PAD + GRID_PAD, GRID_PAD - BRUSH_WIDTH + 6 * text.get_height()))
			text = font.render("Player 2: " + str(self.p2Wins) + " wins", True, TEXT_COLOR)
			screen.blit(text, (SCREEN_WIDTH - RIGHT_PAD + GRID_PAD, GRID_PAD - BRUSH_WIDTH + 7 * text.get_height()))

		def drawBoard():
			for i in range(3):
				for j in range(3):
					if self.board[i][j] == 1:
						drawCircle(j, i)
					if self.board[i][j] == 2:
						drawCross(j, i)

		def drawClick():
			pygame.draw.circle(screen, (140, 200, 140), (stored_x, stored_y), self.clickCircle, 1)
			if self.clickCircle < 30:
				self.clickCircle += 1
			else:
				self.clicked = False
				self.clickCircle = 1
				
		def checkWin(y, x):
			board = self.board
			# Check Vertical
			if board[0][y] == board[1][y] == board[2][y] == self.player:
				return 1
			# Check Horizontal
			if board[x][0] == board[x][1] == board[x][2] == self.player:
				return 1
			# Check Diagonal Top-Left to Bottom-Right
			if x == y and board[0][0] == board[1][1] == board[2][2] == self.player:
				return 1
			# Check Other Diagonal Top-Right to Bottom-Left
			if x + y == 2 and board[0][2] == board[1][1] == board[2][0] == self.player:
				return 1
			if None in board[0] or None in board[1] or None in board[2]:
				return 2
			else:
				return 3

		def restartGame():
			self.playing = True
			self.player = 1
			self.board = [[None, None, None], [None, None, None], [None, None, None]]

		def onClick(x, y):
			rbtn_x = SCREEN_WIDTH - RIGHT_PAD + GRID_PAD
			rbtn_y = SCREEN_HEIGHT - 2 * GRID_PAD
			rbtn_width = RIGHT_PAD - 2 * GRID_PAD + BRUSH_WIDTH
			rbtn_height = GRID_PAD + BRUSH_WIDTH

			# Convert pixel grid into board game grid
			if x > GRID_PAD and x < GRID_PAD + GRID_WIDTH and y > GRID_PAD and y < GRID_PAD + GRID_HEIGHT:
				gridX = (x - GRID_PAD) // (GRID_WIDTH // 3)
				gridY = (y - GRID_PAD) // (GRID_HEIGHT // 3)

				#print(self.board[gridY][gridX])

				if self.playing:
					if self.board[gridY][gridX] is None:
						self.board[gridY][gridX] = self.player
						if checkWin(gridX, gridY) == 1:
							self.playing = False
							print("Player", self.player, "has won!")
							if self.player == 1:
								self.p1Wins += 1
							else:
								self.p2Wins += 1
						elif checkWin(gridX, gridY) == 2:
							self.player = 2 if self.player == 1 else 1
						else:
							self.playing = False
							print("Tie game!")

			elif x > rbtn_x and x < rbtn_x + rbtn_width and y > rbtn_y and y < rbtn_y + rbtn_height:
				restartGame()


		while self.running:
			mx, my = pygame.mouse.get_pos()

			for event in pygame.event.get():
				if event.type == MOUSEBUTTONUP:
					self.clicked = True
					stored_x = mx
					stored_y = my
					onClick(mx, my)
				#if event.type == KEYDOWN:
					#if event.key == K_ESCAPE:
						#running = False
				if event.type == QUIT:
					self.running = False

			screen.fill(BGRD_COLOR)

			# Draw Grid Broder
			drawBox()

			# Draw Grid
			drawGrid()

			# Draw text info like player turns
			drawText()

			# Draw Board
			drawBoard()

			# Draw Restart Button
			drawRestart()

			if(not self.playing):
				drawWin()

			# Draw slightly cool click effect
			if(self.clicked):
				drawClick()

			pygame.display.flip()
			clock.tick(90)

		pygame.quit()

TicTacToe()