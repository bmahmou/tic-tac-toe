import random
import argparse
from itertools import cycle

class TicTacToe:

    def __init__(self, *,
                 playmode: str,
                 train_flag: bool = False,
                 player_info):
        
        # Set up the following for the game:
        # Make the board state (display with brackets).
        # Set up the board symbols and set starting turn. 
        # Winning states of the game (i.e. diagonal & straights).
        # Start game by prompting the next play

        self.boardState = [' '] * 9
        self.boardDisplay = '\n   a   b   c \n\n1 [{0}] [{1}] [{2}]\n\n2 [{3}] [{4}] [{5}]\n\n3 [{6}] [{7}] [{8}]\n'
        self.showBoard()
        self.symbols = list( player_info.values() )
        self.turn_cycle = cycle( list(player_info.values()) )
        self.turn = next(self.turn_cycle)
        self.nextMoveFlag = True
        self.winSet = [{1,2,3},{4,5,6},{7,8,9},{1,4,7},{2,5,8},{3,6,9},{1,5,9},{3,5,7}]
        self.isGameRunning = True
        self.opponent = playmode
        self.train_flag = train_flag


    def showBoard(self):

        board_filled_in = self.boardDisplay.format(*self.boardState)
        print( board_filled_in )

    def promptPlayer(self):

        # Ask for input from said player & roll out the game
        while self.isGameRunning:

            inputCoor = input(f'\nPlayer {self.turn}:\n\nEnter coordinates of your next move! (Number+Letter e.g. 3c) = ').strip().lower()

            # is input valid?
            if not self.evalBoardInput(inputCoor):
                continue

            if not self.updateBoardState(inputCoor):
                continue


            self.turn = next(self.turn_cycle)

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
                sym_to_check = get_opposite(self.turn) #'O' if self.turn == 'X' else 'X'
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


def input_parser():

    # TODO: Add a clear help section for the CLI inputs you have.
    
    parser = argparse.ArgumentParser(description="Play a game of Tic Tac Toe in the terminal: 2-Player or against the computer.")
    
    symbol_parser = argparse.ArgumentParser(description = "Two player name and symbol information",add_help = False)
    symbol_parser.add_argument('--p1-name', required = False, type = str, default = None, help = "First player name")
    symbol_parser.add_argument('--p1-sym', required = False, choices = ['X','O'], default = None, help = "First player symbol")
    
    symbol_parser.add_argument('--p2-name', required = False, type = str, default = None, help = "Second player name")
    symbol_parser.add_argument('--p2-sym', required = False, choices = ['X','O'], default = None, help = "Second player symbol")

    compInfo_parser = argparse.ArgumentParser(description= "Single player name and symbol", add_help = False)
    compInfo_parser.add_argument('--p-name', required = False, type = str, default = None, help = 'Player name')
    compInfo_parser.add_argument('--p-sym', required = False, choices = ['X','O'], default = None, help = 'Player symbol')

    #turn_parser = argparse.ArgumentParser(description = "Indicate the first turn")
    parser.add_argument('--first-turn', required = False, type = str, choices = ['X','O'], help = 'Pick the first turn (indicated by symbol)')

    playtype_parser = parser.add_subparsers(dest='playtype', required=True)
    
    playtype_parser.add_parser('2player', parents = [symbol_parser])

    comp_parser = playtype_parser.add_parser('computer', parents = [compInfo_parser])
    comp_parser.add_argument('--train', action='store_true', help = 'Train the RL algorithm')

    parsed_input = parser.parse_args()

    playerInfo = get_player_info(parsed_input)

    playerInfo["playtype"] = parsed_input.playtype
    playerInfo["train"] = vars(parsed_input).get("train")

    return playerInfo

def get_player_info(parsed_input):

    name_sym = {}
    if parsed_input.playtype == 'computer':

        p_name = 'COMPUTER_2' if parsed_input.train else parsed_input.p_name or 'Human'
        p_sym = parsed_input.p_sym or random.choice(['X','O'])

        comp_sym = get_opposite(p_sym) #'X' if p_sym =='O' else 'O'

        name_sym[p_name] = p_sym
        name_sym['COMPUTER'] = comp_sym

    elif parsed_input.playtype == '2player':

        # name: if there is a None, then insert a placeholder. 
        # symbol: if both are None, then random.choice; If one is none, then put the other.
        
        args = vars(parsed_input)

        for k,v in args.items():
            if '_name' in k:

                # get the symbol of the same place
                sym_key = k.replace('_name','_sym')
                sym = args.get(sym_key)

                # if the player name is missing, create one
                if v is None:
                    name_sym[ f"Player{ k[1] }" ] = sym   
                else:
                    name_sym[v] = sym


        # if no symbols haven't been chosen.
        if not any(name_sym.values()) :

            # randomly assign the symbols
            player1, player2= name_sym.keys()
            name_sym[ player1 ] = random.choice(['X','O'])
            name_sym[ player2 ] = get_opposite(name_sym[player1])
        else:

            # otherwise take the symbol that was chosen, 
            # and player name that needs the new assignment
            for k,v in name_sym.items():
                if v: taken = v
                else: player_to_set = k
            name_sym[player_to_set] = get_opposite(taken) #'X' if taken == 'O' else 'O'



    first_turn = (parsed_input.first_turn 
                if parsed_input.first_turn
                else random.choice( list(name_sym.values()) ) )

    # sort the name:symbol dict by the first turn. False=0 goes before True=1, therefore assert NOT match
    name_sym_sorted = dict(sorted(name_sym.items(), key = lambda item: item[1] != first_turn))
    
    return {"player_and_sym": name_sym_sorted}


def get_opposite(sym):
    return 'X' if sym == 'O' else 'O'
    
if __name__ == '__main__':

    game_config = input_parser()

    game = TicTacToe(playmode = game_config["playtype"], 
                     train_flag = game_config["train"],
                     player_info = game_config["player_and_sym"])
    
    game.promptPlayer()

    