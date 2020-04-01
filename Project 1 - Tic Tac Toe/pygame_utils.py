# Originally from
# https://github.com/witonisaurus/tictactoe/blob/master/Button.py
# adapted into pygame_utils
import pygame

class Button():
	def __init__(self, event, pos, width, height, color=None, bg_color=None, text=None, border_thickness=None):
		self.event = event
		self.pos = pos			# (x, y) format
		self.width = width
		self.height = height
		self.color = color if color is not None else (100, 100, 100)
		self.bg_color = bg_color if bg_color is not None else (200, 200, 200)
		self.text = text if text is not None else ""
		self.border_thickness = border_thickness if border_thickness is not None else 0

		self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)

	def is_clicked(self, mouse_coords):
		if mouse_coords[0] < self.pos[0] or mouse_coords[0] > (self.pos[0] + self.width):
			return False
		if mouse_coords[1] < self.pos[1] or mouse_coords[1] > (self.pos[1] + self.width):
			return False
		return True

	def draw(self, surface):
		pygame.draw.rect(surface, self.color, self.rect, self.border_thickness)

		font = pygame.font.Font('freesansbold.ttf', self.height // 3)
		text = font.render(self.text, True, self.color)

		surface.blit(text, (self.pos[0] + self.width // 2 - text.get_width() // 2, self.pos[1] + self.height // 2 - text.get_height() // 2))

	def update(self, event=None, pos=None, width=None, height=None, color=None, bg_color=None, text=None, border_thickness=None):
		self.event = event if event is not None else self.event
		self.pos = pos if pos is not None else self.pos
		self.width = width if width is not None else self.width
		self.height = height if height is not None else self.height
		self.color = color if color is not None else self.color
		self.bg_color = bg_color if bg_color is not None else self.bg_color
		self.text = text if text is not None else self.text
		self.border_thickness = border_thickness if border_thickness is not None else self.border_thickness

def main():
	pass

if __name__ == '__main__':
	main()