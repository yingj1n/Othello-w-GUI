#othello_logic2.py
#Name: Ying Jin

NONE = 0
WHITE = 1
BLACK = 2

class InvalidSizeTooBigOrSmall(Exception):
    pass

class InvalidSizeNotEvenNum(Exception):
    pass

class InvalidColorError(Exception):
    pass

class InvalidWinningCondition(Exception):
    pass

class InvalidMoveError(Exception):
    pass

class Othello:
    def __init__(self,
                 BOARD_ROWS:int,BOARD_COLUMNS:int,
                 FIRST_MOVE:str,HOW_WIN:str):
        
        self.HOW_WIN = HOW_WIN
        
        if BOARD_ROWS < 4 or BOARD_ROWS > 16 or BOARD_COLUMNS < 4 or BOARD_COLUMNS > 16:
            raise InvalidSizeTooBigOrSmall
        
        if BOARD_ROWS % 2 != 0 or BOARD_COLUMNS % 2 != 0:
            raise InvalidSizeNotEvenNum
        
        self._ROWS = BOARD_ROWS
        self._COLUMNS = BOARD_COLUMNS

        if FIRST_MOVE not in ['B','W']:
            raise InvalidColorError

        if FIRST_MOVE in ['B','W']:
            if FIRST_MOVE == 'B':
                self._turn = BLACK
                self._first_move = BLACK
            elif FIRST_MOVE == 'W':
                self._turn = WHITE
                self._first_move = WHITE
                
        if HOW_WIN not in ['>','<']:
            raise InvalidWinningCondition

        initial_board = []
        #list of list = row of column
        for row in range(int(self._ROWS)):
            initial_board.append([])
            for col in range(int(self._COLUMNS)):
                initial_board[-1].append(NONE)

        self.board = initial_board
        
        self._stucked_count = 0

    def give_init_con(self, color:int, coor:tuple) -> None:
        if self.board[coor[0]][coor[1]] == NONE:
            self.board[coor[0]][coor[1]] = color

        self._stucked_count = 0

    def put_down_color(self,coor:tuple) -> None:
        _flip_places_found = self._places_to_flip(coor)
        if _flip_places_found == []:
            raise InvalidMoveError
        if self.board[coor[0]][coor[1]] != NONE:
            raise InvalidMoveError
        else:
            self._flip_color(_flip_places_found)
            self.board[coor[0]][coor[1]] = self._turn
            self._turn = self._return_oppo_color(self._turn)
            self._stucked_count = 0

    def _flip_color(self,_flip_places_found:list) -> None:
        for each_position in _flip_places_found:
            self.board[each_position[0]][each_position[1]] = self._turn

    def game_continue(self) -> bool:
        if self._stucked_count == 2:
            self._turn = NONE
            return False

        help_list = []
        NONE_COUNT = 0
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == NONE:
                    NONE_COUNT += 1
                    help_list += self._places_to_flip((row,col))
                    
        if NONE_COUNT == 0:
            self._turn = NONE
            return False
        
        if help_list == []:
            self._turn = self._return_oppo_color(self._turn)
            self._stucked_count += 1
            if self.game_continue() == True:
                return True
            else:
                return False
        elif help_list != []:
            return True

    def _places_to_flip(self,coor:tuple) -> list:
        _oppo_color = self._return_oppo_color(self._turn)

        #check whether there is stuff to flip in these directions (row,col)
        #               E,    SE,   S,    SW,     W,     NW,    N,     NE
        directions = [(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1)]

        list_of_coor_to_flip = []
        for each_direction in directions:
            potential_coor_to_flip = []
            row_coor = coor[0]
            col_coor = coor[1]
            while True:
                row_coor = row_coor + each_direction[0]
                col_coor = col_coor + each_direction[1]
                if col_coor >= 0 and row_coor >= 0:
                    try:
                        if self.board[row_coor][col_coor] == _oppo_color:
                            potential_coor_to_flip += [(row_coor,col_coor)]
                        elif self.board[row_coor][col_coor] == self._turn:
                            break
                        elif self.board[row_coor][col_coor] == NONE:
                            potential_coor_to_flip = []
                            break
                    except IndexError:
                        potential_coor_to_flip = []
                        break
                else:
                    potential_coor_to_flip = []
                    break
            if potential_coor_to_flip != []:
                list_of_coor_to_flip += potential_coor_to_flip
        return list_of_coor_to_flip
            
    def _return_oppo_color(self,color:int) -> int:
        if color == WHITE:
            oppo_color = BLACK
        elif color == BLACK:
            oppo_color = WHITE
        return oppo_color

    def return_turn(self) -> None:
        return self._turn

    def return_num_of_color(self) -> dict:
        count = {BLACK:0,WHITE:0}
        for color in [BLACK,WHITE]:
            for each_row in range(self._ROWS):
                for each_location in range(self._COLUMNS):
                    if self.board[each_row][each_location] == color:
                        count[color] += 1
        return count

    def _return_winner(self) -> int:
        count = self.return_num_of_color()
        if self.HOW_WIN == '>':
            if count[BLACK] > count[WHITE]:
                return BLACK
            elif count[BLACK] < count[WHITE]:
                return WHITE
            else:
                return NONE
        if self.HOW_WIN == '<':
            if count[BLACK] < count[WHITE]:
                return BLACK
            elif count[BLACK] > count[WHITE]:
                return WHITE
            else:
                return NONE
