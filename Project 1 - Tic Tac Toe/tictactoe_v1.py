#!/usr/bin/env python3
import pygame

from pygame.locals import *
from pygame_utils import Button

import tictactoe_game

pygame.init()

SCREEN_WIDTH = 640 # Default 640
SCREEN_HEIGHT = 480 # Default 480

BRUSH_WIDTH = 5
GRID_PAD = 40
BOX_PAD = 30

RIGHT_PAD = SCREEN_WIDTH - GRID_PAD - (SCREEN_HEIGHT - 2 * GRID_PAD)
GRID_WIDTH = SCREEN_WIDTH - GRID_PAD - RIGHT_PAD
GRID_HEIGHT = SCREEN_HEIGHT - 2 * GRID_PAD

BGRD_COLOR = [(42, 42, 42), (213, 213, 213)]
ACCENT_COLOR = [(100, 200, 255), (25, 50, 80)]
ACCENT_COLOR2 = [(80, 80, 80), (175, 175, 175)]
ACCENT_COLOR3 = [(80, 80, 80, 192), (175, 175, 175, 192)]
TEXT_COLOR = [(230, 230, 230), (25, 25, 25)]

REFRESH_RATE = 90

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
font = pygame.font.SysFont("ubuntu", 16)
clock = pygame.time.Clock()

class TicTacToe(object):
	def __init__(self):
		self.params = [SCREEN_WIDTH, SCREEN_HEIGHT, RIGHT_PAD, BOX_PAD, GRID_WIDTH, GRID_HEIGHT, GRID_PAD, BRUSH_WIDTH]
		self.theme = [0, BGRD_COLOR[0], ACCENT_COLOR[0], ACCENT_COLOR2[0], ACCENT_COLOR3[0], TEXT_COLOR[0]]
		self.clicked = False
		self.click_circle = 10

		# running, state,   player,  p1_wins, p2_wins, round
		# game[0], game[1], game[2], game[3], game[4], game[5]
		self.game = [True, 1, 1, 0, 0, 1] 
		self.board = [[None, None, None], [None, None, None], [None, None, None]]
		self.btns = []
		self.Main()

	def Main(self):

		def initialize():
			pygame.display.set_caption("Crosses and Noughts by Hans")
			self.btns.append(Button(screen, (self.params[0] - self.params[2] + self.params[6], self.params[1] - 2 * self.params[6]), self.params[2] - 2 * self.params[6] + self.params[7], self.params[6] + self.params[7], color=self.theme[2], bg_color=self.theme[1], text="Restart", border_thickness=2))
			self.btns.append(Button(screen, (self.params[0] - self.params[2] + self.params[6], self.params[1] - 3 * self.params[6] - self.btns[0].height / 2), self.params[2] - 2 * self.params[6] + self.params[7], self.params[6] + self.params[7], color=self.theme[2], bg_color=self.theme[1], text="Change Theme", border_thickness=2))
			self.btns.append(Button(screen, (self.params[0] - self.params[2] + self.params[6], self.params[1] - 3 * self.params[6] - self.btns[0].height * 2 ), self.params[2] - 2 * self.params[6] + self.params[7], self.params[6] + self.params[7], color=self.theme[2], bg_color=self.theme[1], text="Play AI Turn", border_thickness=2))

		def draw_box():
			# This draws a border *outside* of the rect. This helps setting the x and y overall
			pygame.draw.rect(screen, self.theme[2], pygame.Rect(self.params[6] - self.params[7], self.params[6] - self.params[7], self.params[6] + self.params[4] - self.params[6] + 2 * self.params[7], self.params[6] + self.params[5] - self.params[6] + 2 * self.params[7])) # I'm going to ignore the fact that the last parameter is also brush width and can make the rect not filled in
			pygame.draw.rect(screen, self.theme[1], pygame.Rect(self.params[6],	self.params[6], self.params[6] + self.params[4] - self.params[6], self.params[6] + self.params[5] - self.params[6]))

		def draw_grid():
			pygame.draw.line(screen, self.theme[2],	(self.params[6] + self.params[4] // 3, self.params[6]),	(self.params[6] + self.params[4] // 3,self.params[6] + self.params[5]),	self.params[7])
			pygame.draw.line(screen, self.theme[2],	(self.params[6] + self.params[4] * 2 // 3, self.params[6]),	(self.params[6] + self.params[4] * 2 // 3,self.params[6] + self.params[5]),	self.params[7])
			pygame.draw.line(screen, self.theme[2], (self.params[6], self.params[6] + self.params[5] // 3), (self.params[6] + self.params[4], self.params[6] + self.params[5] // 3), self.params[7])
			pygame.draw.line(screen, self.theme[2],	(self.params[6], self.params[6] + self.params[5] * 2 // 3), (self.params[6] + self.params[4], self.params[6] + self.params[5] * 2 // 3), self.params[7])

		def draw_win():
			surf = pygame.Surface((self.params[0], self.params[1] // 3 - self.params[6]), pygame.SRCALPHA)
			surf.fill(self.theme[4])
			f = pygame.font.SysFont("ubuntu", 42)
			text = ""
			if self.game[1] == 2:
				text = "Player " + str(self.game[2]) + " has won!"
			elif self.game[1] == 3:
				text = "Tie Game!"
			content = f.render(text, True, self.theme[2])
			surf.blit(content, (self.params[0] // 2 - content.get_width() // 2, (self.params[1] // 3 - self.params[6]) // 2 - content.get_height() // 2))
			screen.blit(surf, (0, self.params[1] // 3 + self.params[6] // 2))
			
		def draw_cross(grid_x, grid_y):
			x = self.params[6] + self.params[3] + grid_x * self.params[4] // 3
			y = self.params[6] + self.params[3] + grid_y * self.params[5] // 3
			x2 = self.params[6] - self.params[3] + (grid_x + 1) * self.params[4] // 3
			y2 = self.params[6] - self.params[3] + (grid_y + 1) * self.params[5] // 3

			pygame.draw.line(screen, self.theme[2], (x, y), (x2,y2), self.params[7])
			pygame.draw.line(screen, self.theme[2], (x2, y), (x, y2), self.params[7])

		def draw_circle(grid_x, grid_y):
			x = self.params[6] + (self.params[4] / 6) + grid_x * self.params[4] / 3
			y = self.params[6] + (self.params[5] / 6) + grid_y * self.params[5] / 3
			r = (self.params[5] / 6) - (self.params[3] / 2)
			pygame.draw.circle(screen, self.theme[2], (int(x), int(y)), int(r), self.params[7])

		def draw_text():
			text = font.render("It is Player " + str(self.game[2]) + "'s turn", True, self.theme[5])
			screen.blit(text, (self.params[0] - self.params[2] + self.params[6], self.params[6] - self.params[7]))
			text = font.render("Player 1 = O", True, self.theme[5])
			screen.blit(text, (self.params[0] - self.params[2] + self.params[6], self.params[6] - self.params[7] + 3 * text.get_height()))
			text = font.render("Player 2 = X", True, self.theme[5])
			screen.blit(text, (self.params[0] - self.params[2] + self.params[6], self.params[6] - self.params[7] + 4 * text.get_height()))
			text = font.render("Round " + str(self.game[5]), True, self.theme[5])
			screen.blit(text, (self.params[0] - self.params[2] + self.params[6], self.params[6] - self.params[7] + 6 * text.get_height()))
			text = font.render("Player 1: " + str(self.game[3]) + " wins", True, self.theme[5])
			screen.blit(text, (self.params[0] - self.params[2] + self.params[6], self.params[6] - self.params[7] + 8 * text.get_height()))
			text = font.render("Player 2: " + str(self.game[4]) + " wins", True, self.theme[5])
			screen.blit(text, (self.params[0] - self.params[2] + self.params[6], self.params[6] - self.params[7] + 9 * text.get_height()))

		def draw_board():
			for i in range(3):
				for j in range(3):
					if self.board[i][j] == 1:
						draw_circle(j, i)
					if self.board[i][j] == 2:
						draw_cross(j, i)

		def draw_click():
			pygame.draw.circle(screen, (140, 200, 140), (stored_x, stored_y), self.click_circle, 1)
			if self.click_circle > 1:
				self.click_circle -= 1
			else:
				self.clicked = False
				self.click_circle = 10

		def switch_theme():
			self.theme[0] = 1 if self.theme[0] == 0 else 0
			self.theme = [self.theme[0], BGRD_COLOR[self.theme[0]], ACCENT_COLOR[self.theme[0]], ACCENT_COLOR2[self.theme[0]], ACCENT_COLOR3[self.theme[0]], TEXT_COLOR[self.theme[0]]]
			for btn in self.btns:
				btn.update(color=self.theme[2])

		def refresh_screen():
			screen.fill(self.theme[1])
			draw_box() 					# Draw Grid Broder
			draw_grid() 				# Draw Grid
			draw_text() 				# Draw text info like player turns
			draw_board()				# Draw Board
			for i in range(len(self.btns)):
				self.btns[i].draw(screen)
			if(self.game[1] == 2 or self.game[1] == 3):
				draw_win()

			# Draw slightly cool click effect
			if(self.clicked):
				draw_click()

			pygame.display.flip()
			clock.tick(REFRESH_RATE)
				
		def check_win(grid):
			board = self.board
			if board[0][grid[1]] == board[1][grid[1]] == board[2][grid[1]] == self.game[2]:
				# Check Vertical
				self.game[1] = 2 # Win
			elif board[grid[0]][0] == board[grid[0]][1] == board[grid[0]][2] == self.game[2]:
				# Check Horizontal
				self.game[1] = 2 # Win
			elif grid[0] == grid[1] and board[0][0] == board[1][1] == board[2][2] == self.game[2]:
				# Check Diagonal Top-Left to Bottom-Right
				self.game[1] = 2 # Win
			elif grid[0] + grid[1] == 2 and board[0][2] == board[1][1] == board[2][0] == self.game[2]:
				# Check Other Diagonal Top-Right to Bottom-Left
				self.game[1] = 2 # Win
			elif None in board[0] or None in board[1] or None in board[2]:
				self.game[1] = 1 # Continue Game
			else:
				self.game[1] = 3 # Tie Game
			#print(board[0][grid[1]], board[1][grid[1]], board[2][grid[1]], self.game[2])
			#print("Game State:", self.game[1])
			#print(grid)
			#print(self.board)

		def restart_game():
			self.game[1] = 1
			self.game[2] = 1
			self.board = [[None, None, None], [None, None, None], [None, None, None]]

		def on_click(pos):
			rbtn_x = self.params[0] - self.params[2] + self.params[6]
			rbtn_y = self.params[1] - 2 * self.params[6]
			rbtn_width = self.params[2] - 2 * self.params[6] + self.params[7]
			rbtn_height = self.params[6] + self.params[7]

			# Convert pixel grid into board game grid
			if pos[0] > self.params[6] and pos[0] < self.params[6] + self.params[4] and pos[1] > self.params[6] and pos[1] < self.params[6] + self.params[5]:
				grid_x = (pos[0] - self.params[6]) // (self.params[4] // 3)
				grid_y = (pos[1] - self.params[6]) // (self.params[5] // 3)
				#print(self.board[grid_y][grid_x])
				if not self.game[1] == 0:
					if self.game[1] == 1:
						if self.board[grid_y][grid_x] is None:
							self.board[grid_y][grid_x] = self.game[2]
							check_win((grid_y, grid_x))
							#print(self.game[1])
							if self.game[1] == 1: # If game can still continue
								# Swap players
								self.game[2] = 2 if self.game[2] == 1 else 1
							elif self.game[1] == 2:
								#print("Player", self.game[2], "has won!")
								if self.game[2] == 1:
									self.game[3] += 1
								else:
									self.game[4] += 1
								self.game[5] += 1
							elif self.game[1] == 3:
								self.game[5] += 1
								#print("Tie game!")

		initialize()

		while self.game[0]:
			mx, my = pygame.mouse.get_pos()

			for event in pygame.event.get():
				if event.type == MOUSEBUTTONUP:
					self.clicked = True
					stored_x = mx
					stored_y = my
					on_click((mx, my))
					if self.btns[0].is_clicked((mx, my)):
						restart_game()
					elif self.btns[1].is_clicked((mx, my)):
						switch_theme()
				if event.type == QUIT:
					self.game[0] = False

			refresh_screen()

		pygame.quit()

TicTacToe()