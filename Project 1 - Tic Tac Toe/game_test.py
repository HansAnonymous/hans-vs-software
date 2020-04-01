from tictactoe_game import TicTacToe

game = TicTacToe()
game.print_board()
while(not game.game_over(game.get_board())):
	game.ai_move(game.PLAYERONE)
	game.print_board()
	game.ai_move(game.PLAYERTWO)
	game.print_board()