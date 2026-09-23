import random

class TicTacToe():

    def __init__(self, starting_turn: str = None):
        # Set up the following for the game:
        # Make the board state (display with brackets).
        # Set up the board symbols and set starting turn. 
        # Winning states of the game (i.e. diagonal & straights).
        # Start game by prompting the next play

        self.boardState = [' '] * 9
        self.boardDisplay = '\n   a   b   c \n\n1 [{0}] [{1}] [{2}]\n\n2 [{3}] [{4}] [{5}]\n\n3 [{6}] [{7}] [{8}]\n'
        self.showBoard()
        self.symbols = ['X','O']
        self.turn = starting_turn
        self.nextMoveFlag = True
        self.winSet = [{1,2,3},{4,5,6},{7,8,9},{1,4,7},{2,5,8},{3,6,9},{1,5,9},{3,5,7}]
        self.isGameRunning = True


    def showBoard(self):

        board_filled_in = self.boardDisplay.format(*self.boardState)
        print( board_filled_in )

    def promptPlayer(self):

        # For the first move, randomly choose a player to start
        if self.turn is None:
            self.turn = random.choice(self.symbols)

        # Ask for input from said player & roll out the game
        while self.isGameRunning:

            inputCoor = input(f'\nPlayer {self.turn}:\n\nEnter coordinates of your next move! (Number+Letter e.g. 3c) = ').strip().lower()

            # is input valid?
            if not self.evalBoardInput(inputCoor):
                continue

            if not self.updateBoardState(inputCoor):
                continue


            self.turn = 'O' if self.turn == 'X' else 'X'


    def evalBoardInput(self,inputCoor):
        # Check the input is valid, return to prompt player function if not.
        
        # check for length
        if len(inputCoor) != 2:
            print("\nInput must be exactly two characters! Digit and alphanumeric coordinates. Try again... ")
            return False
            
        coor_num = inputCoor[0]
        coor_letter = inputCoor[1]

        # Check for the alphanumeric values
        if not coor_num.isdigit() or int(coor_num) not in [1,2,3]:
            self.showBoard()
            print('Board coordinate number is not valid or out of range! Try again...')
            return False
    
        if not coor_letter.isalpha() or coor_letter not in ['a','b','c']:
            self.showBoard()
            print('Board coordinate character is either not valid! Try again...')
            return False

        return True
    
    def updateBoardState(self,inputCoor):

        # get linear index from alphanumeric input (e.g. 2b = column 2 row 2, linear index 5)
        move_linIndex = self.translateToBoardState(inputCoor)

        # check board index occupancy
        coor_is_occupied = self.boardState[move_linIndex].isalpha()
        
        if coor_is_occupied:
            self.showBoard()
            print('That board position is already occupied! Try Again... ')
            return False
        
        elif not coor_is_occupied:
            self.boardState[move_linIndex] = self.turn

        # present the board following the new move
        self.showBoard()

        # check for end game states.
        self.checkBoardState()

        return True


    def checkBoardState(self):

        # check the status of the board: Game won? Game tied?
        
        boardOccupancyDict = {'X':[] , 'O':[]}
        openBoardPos = set()
        for pos,sym in enumerate(self.boardState, start=1):
            if sym in boardOccupancyDict.keys():
                boardOccupancyDict[sym].append(pos)
            else:
                openBoardPos.add(pos)

        winningPosition = [True for s in self.winSet if s.issubset( boardOccupancyDict[self.turn] )]

        if winningPosition:
            print(f"\nGame has been won by player {self.turn}", r" *\(^o^)/* ", "\n")
            self.isGameRunning  = False
            return

        elif len(openBoardPos) <=2 :

            continueGame = []

            # which players to check
            if len(openBoardPos) == 1:
                sym_to_check = 'O' if self.turn == 'X' else 'X'
            elif len(openBoardPos) >1:
                sym_to_check = boardOccupancyDict.keys()


            for sym in sym_to_check:
                for s in self.winSet:

                    # Is there a winning move given player position AND open board positions?
                    if ( 
                        s.issubset( openBoardPos.union(boardOccupancyDict[sym])) and
                        len( s.difference(boardOccupancyDict[sym]) ) ==1
                    ):
                        continueGame = True
                        break


            if not continueGame:
                    print("\n", r"Game is a draw! ¯\_(ツ)_/¯","\n")
                    self.isGameRunning  = False
                    return


    def translateToBoardState(self,inputCoor):
        # return a linear index from the coordinates
        
        row = [1,2,3].index( int(inputCoor[0]) )
        col = ['a','b','c'].index( inputCoor[1] )

        linIndex = (row*3)+(col)
        return linIndex 

    


if __name__ == '__main__':
    
    gameObj = TicTacToe()
    gameObj.promptPlayer()
    