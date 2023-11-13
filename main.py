import sys
from board import Board

class Main:

    def __init__(self): #metodo chiamato quando creo un istanza dell oggetto main
        
        if len(sys.argv) > 1:
            
            if int(sys.argv[1]) < 0 or int(sys.argv[1]) >2:
                self.board = Board()
            else:
                order = int(sys.argv[1])
                self.board = Board(order)

        else:
            self.board = Board()

        

main = Main()
main.board.play()
main.board.print_board()      