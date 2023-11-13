import sys

class Board:

    def __init__(self, order=2):
        

        #order 
        # 0 = seriale
        # 1 = random
        # 2 = greedy - Wransfdorf's rule
        self.order = order

        # scacchiera
        self.board = [[-1,-1,-1,-1,-1,-1,-1,-1] for col in range(8)]
        self.board[7][1] = 0

        # lista mosse/posizioni fatte
        self.list_move=[]
        self.list_move.append([7,1])
        
        #lista delle mosse possibili
        self.list_of_possible_move  = [[] for i in range(64)]
        self.list_of_possible_move[0].append([7,1])

        self.top_move = 0

    #questa fuzione ordina in base alle mosse possibili a sua volta
    def _order_by_warnsdorff_rule(self, next_move_number):
        
        number_of_moves= len(self.list_of_possible_move[next_move_number])

        possible_number_of_moves_list = [0 for i in range(number_of_moves)]

        # popolo l''array con il numero delle possibili mosse
        for i in range(number_of_moves):

            
            row = self.list_of_possible_move[next_move_number][i][0]
            col = self.list_of_possible_move[next_move_number][i][1]

            new_rows = [-2,-2,2,2,-1,-1,1,1]
            new_cols = [1,-1,1,-1,2,-2,2,-2]
            
            for j in range(8):
                new_row = row + new_rows[j]
                new_col = col + new_cols[j]
                
                if new_row>=0 and new_row<=7 and new_col >=0 and new_col <=7:    
                    if self.board[new_row][new_col] == -1:
                        possible_number_of_moves_list[i] += 1



        #ordino le mosse possibili in base al numero di mosse a loro volta valide
        self.list_of_possible_move[next_move_number] = [x for _, x in sorted(zip(possible_number_of_moves_list, self.list_of_possible_move[next_move_number]))]

            
    def _add_candidates_moves(self):

        board = self.board
        next_move_number = len(self.list_move)

        last_move = len(self.list_move)-1
        row = self.list_move[last_move][0]
        col = self.list_move[last_move][1]

        
        new_rows = [-2,-2,2,2,-1,-1,1,1]
        new_cols = [1,-1,1,-1,2,-2,2,-2]

        for i in range(8):
            new_row = row + new_rows[i]
            new_col = col + new_cols[i]

            if new_row>=0 and new_row<=7 and new_col >=0 and new_col <=7:    
                if board[new_row][new_col] == -1:
                    self.list_of_possible_move[next_move_number].append([new_row,new_col])

        
        # da come è ordinata la lista delle mosse possibili, dipenderà anche 
        # quale mossa viene tentata per primo, dato che si utilizzerà il metodo pop() 
        # per selezionara la mossa

        next_move_number = last_move+1
        
        
        if self.order == 1:
            #random per non avere sempre la stessa soluzione finale, ed è anche più veloce
            self.list_of_possible_move[next_move_number].sort()
        
        elif self.order == 2:

            #GREEDY: scegliamo sempre la mossa che avrà in seguito meno mosse possibili a disposizione
            # -- Warnsdorff's Rule --
            # quindi dobbiamo ordinare dalla mossa con piu mosse disposizione, a quella che ne ha di meno
            self._order_by_warnsdorff_rule(next_move_number)
    
        #print(self.list_of_possible_move)    


    def play(self):

        next_move_number = 1
        new_position = True


        while next_move_number <64:

            
            #calcolo le mosse possibili, se non le ho gia calcolate, e le aggiungo
            if new_position:
                self._add_candidates_moves()
        
            #se ho mosse possibili
            if self.list_of_possible_move[next_move_number] != []:

                # seleziono una mossa tra le candidate con pop
                next_move_position = self.list_of_possible_move[next_move_number].pop(0)

                #aggiorno la scacchiera
                new_row = next_move_position[0]
                new_col = next_move_position[1]
                self.board[new_row][new_col] = next_move_number

                #aggiorno la lista delle mosse
                self.list_move.append(next_move_position)

                #aggiorno numero prossima mossa
                next_move_number = len(self.list_move)


                '''
                # se ho fatto progressi, stampo la scacchiera
                if next_move_number > self.top_move:
                    self.top_move = next_move_number
                    print (self.top_move)
                    self.print_board()
                '''
                
                #nuova posizione
                new_position = True


            #non è possibile effettuare altre mosse
            else:
                
                #backtracking
                move_to_remove = self.list_move.pop()
                next_move_number=len(self.list_move)

                new_row = move_to_remove[0]
                new_col = move_to_remove[1]
                self.board[new_row][new_col] = -1
                new_position = False # se torno indietro non devo ricalcolare le mosse candidate


    def print_board(self):
        for i in self.board:
            print (i)