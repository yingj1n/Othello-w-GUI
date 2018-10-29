#othello_gui.py
#Name: Ying Jin

import tkinter
import othello_logic2

PINK = '#e3b3b1'
DEFAULT_FONT = 'Helvetica'
FIRST_MOVE = 'Black'
_SHOW_DEBUG_TRACE = False

class TakeInputs:
    def __init__(self):
        self._dialog_window = tkinter.Toplevel()

        #0. Pick your game setting
        self._game_setting = tkinter.Label(
            master = self._dialog_window, text = 'Hello! Before you start, please pick your game settings.',
            font = DEFAULT_FONT+' 14 bold')
        self._game_setting.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5,
                              sticky = tkinter.W + tkinter.N)

        #1. column number
        self._col_dimensions = range(4,18,2)
        self._col_var = tkinter.StringVar()
        self._col_var.set(self._col_dimensions[2])
        
        self._choose_col = tkinter.Label(
            master = self._dialog_window, text = 'Number of Columns:',
            font = DEFAULT_FONT)
        self._choose_col.grid(row = 1, column = 0, padx = 5, pady = 5,
                              sticky = tkinter.W + tkinter.N)
        
        self._dropdown_col = tkinter.OptionMenu(
            self._dialog_window, self._col_var,
            *self._col_dimensions)
        self._dropdown_col.grid(
            row = 1, column = 1, padx = 5, pady = 5,
            sticky = tkinter.W + tkinter.N)

        #2. row number
        self._row_dimensions = range(4,18,2)
        self._row_var = tkinter.StringVar()
        self._row_var.set(self._row_dimensions[2])
        
        self._choose_row = tkinter.Label(
            master = self._dialog_window, text = 'Number of rows:',
            font = DEFAULT_FONT)
        self._choose_row.grid(row = 2, column = 0, padx = 5, pady = 5,
                              sticky = tkinter.W + tkinter.N)
        
        self._dropdown_row = tkinter.OptionMenu(
            self._dialog_window, self._row_var,
            *self._row_dimensions)
        self._dropdown_row.grid(
            row = 2, column = 1, padx = 5, pady = 5,
            sticky = tkinter.W + tkinter.N)

        #3. first move color
        self._color_options = ['Black', 'White']
        self._color_var = tkinter.StringVar()
        self._color_var.set(self._color_options[0])
        
        self._choose_firstmove = tkinter.Label(
            master = self._dialog_window, text = 'Player who goes first:',
            font = DEFAULT_FONT)
        self._choose_firstmove.grid(row = 3, column = 0, padx = 5, pady = 5,
                                    sticky = tkinter.W + tkinter.N)
        
        self._dropdown_firstmove = tkinter.OptionMenu(
            self._dialog_window, self._color_var,
            *self._color_options)
        self._dropdown_firstmove.grid(
            row = 3, column = 1, padx = 5, pady = 5,
            sticky = tkinter.W + tkinter.N)

        #4. winning condition
        self._winning_options = ['The Player with more discs.', 'The Player with fewer discs.']
        self._winning_var = tkinter.StringVar()
        self._winning_var.set(self._winning_options[0])
        
        self._choose_winning = tkinter.Label(
            master = self._dialog_window, text = 'Winning condition:',
            font = DEFAULT_FONT)
        self._choose_winning.grid(row = 4, column = 0, padx = 5, pady = 5,
                                  sticky = tkinter.W + tkinter.N)
        
        self._dropdown_winning = tkinter.OptionMenu(
            self._dialog_window, self._winning_var,
            *self._winning_options)
        self._dropdown_winning.grid(
            row = 4, column = 1, padx = 5, pady = 5,
            sticky = tkinter.W + tkinter.N)

        #DONE Button
        self._done_button = tkinter.Button(
            master = self._dialog_window, text = 'DONE',
            font = DEFAULT_FONT, command = self._on_done_button_clicked)

        self._done_button.grid(
            row = 5, column = 1, padx = 5, pady = 5,
            sticky = tkinter.E + tkinter.N)

        #other
        self._done_clicked = False

    def _show(self) -> None:
        self._dialog_window.grab_set()
        self._dialog_window.wait_window()

    def _on_done_button_clicked(self) -> None:
        self._done_clicked = True
        
        self._col_num = int(self._col_var.get())
        self._row_num = int(self._row_var.get())
        self._first_color = self._color_var.get()
        self._winning_con = self._winning_var.get()

               
        if self._first_color == 'Black':
            self._first_color = 'B'
        elif self._first_color == 'White':
            self._first_color = 'W'
            
        if self._winning_con == 'The Player with more discs.':
            self._winning_con = '>'
        elif self._winning_con == 'The Player with fewer discs.':
            self._winning_con = '<'
            
        
        if _SHOW_DEBUG_TRACE == True:
            print ("from input window:",self._col_num,self._row_num,self._first_color,self._winning_con)
        
        self._dialog_window.destroy()

    def _get_all_info(self) -> 'all conditions':
        return (self._col_num,self._row_num,self._first_color,self._winning_con)

    def _was_done_clicked(self) -> bool:
        return self._done_clicked



class OthelloApplication:
    def __init__(self):
        self._root_window = tkinter.Tk()

        #instruction
        self._instruction = tkinter.Label(
            master = self._root_window, text = "Othello Game Instruction:",
            font = DEFAULT_FONT+' 16 bold')

        self._instruction.grid(
            row = 0, column = 1, padx = 5, pady = 5,
            sticky = tkinter.W)
        
        self._game_words = tkinter.Label(
            master = self._root_window, text = 'Click "Start New Othello Game" button to start',
            font = DEFAULT_FONT+' 14 italic')

        self._game_words.grid(
            row = 1, column = 1, padx = 5, pady = 0,
            sticky = tkinter.E)

        #turnboard
        self._turnboard = tkinter.Label(
            master = self._root_window, text = '---------------',
            font = DEFAULT_FONT + ' 14 bold', background = PINK)

        self._turnboard.grid(
            row = 2, column = 1, padx = 5, pady = 5,
            sticky = tkinter.W + tkinter.N + tkinter.S + tkinter.E)
        
        #1.scoreboard (White)
        self._scoreboard_w = tkinter.Label(
            master = self._root_window, text = 'White\n0 ',
            font = DEFAULT_FONT+' 14 bold')

        self._scoreboard_w.grid(
            row = 0, rowspan = 4, column = 0, padx = 15, pady = 5,
            sticky = tkinter.W)

        #2.scoreboard (Black)
        self._scoreboard_b = tkinter.Label(
            master = self._root_window, text = 'Black\n0',
            font = DEFAULT_FONT+' 14 bold')

        self._scoreboard_b.grid(
            row = 0, rowspan = 4, column = 2, padx = 15, pady = 5,
            sticky = tkinter.E)

        #canvas
        self._canvas = tkinter.Canvas(
            master = self._root_window, width = 400, height = 400,
            background = PINK, highlightbackground='black')

        self._canvas.grid(
            row = 3, column = 1, padx = 0, pady = 5,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        self._canvas.bind('<Configure>', self._on_canvas_resized)
        self._canvas.bind('<Button-1>', self._on_canvas_clicked)

        #game version
        self._version_info = tkinter.Label(
            master = self._root_window, text = 'ver: FULL',
            font = DEFAULT_FONT + ' 12 bold')

        self._version_info.grid(
            row = 4, column = 0, padx = 5, pady = 5,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        #start button
        self._start_button = tkinter.Button(
            master = self._root_window, text = 'Start New Othello Game',
            font = DEFAULT_FONT+' 13', command = self._on_start_button_clicked)

        self._start_button.grid(
            row = 4, column = 1, padx = 10, pady = 5,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        #next button
        self._next_button = tkinter.Button(
            master = self._root_window, text = 'Next',
            font = DEFAULT_FONT+' 13', command = self._on_next_button_clicked)

        self._next_button.grid(
            row = 4, column = 2, padx = 10, pady = 5,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        self._next = 0

        #weight of each
        self._root_window.rowconfigure(0, weight = 0)
        self._root_window.rowconfigure(1, weight = 0)
        self._root_window.rowconfigure(2, weight = 0)
        self._root_window.rowconfigure(3, weight = 1)
        self._root_window.rowconfigure(4, weight = 0)

        self._root_window.columnconfigure(0, weight = 0)
        self._root_window.columnconfigure(1, weight = 1)
        self._root_window.columnconfigure(2, weight = 0)


        self._got_inputs = False
        self._game_started = False
        self._next = 0
        self._game_ended = False


    def _update_scoreboard(self) -> None:
        try:
            count = self._othello_game.return_num_of_color()
            black_count = count[othello_logic2.BLACK]
            white_count = count[othello_logic2.WHITE]
            self._scoreboard_b['text'] = 'Black\n{}'.format(str(black_count))
            self._scoreboard_w['text'] = 'White\n{}'.format(str(white_count))

        except AttributeError:
            pass

    def _update_turnboard(self) -> None:
        try:
            if self._next > 1:
                if self._othello_game.game_continue() == True:
                    turn = self._othello_game.return_turn()
                    if turn == othello_logic2.BLACK:
                        self._turnboard['text'] = 'Turn: Black'
                    elif turn == othello_logic2.WHITE:
                        self._turnboard['text'] = 'Turn: White'
            
                if self._othello_game.game_continue() == False:
                    self._game_ended = True
                    
                    self._game_words['text'] = 'Click "Start New Othello Game" button to start a new game.'
                    _winner = self._othello_game._return_winner()
                    if _winner == othello_logic2.NONE:
                        self._turnboard['text'] = "It's a tie"
                    if _winner == othello_logic2.BLACK:
                        self._turnboard['text'] = 'Black Won'
                    if _winner == othello_logic2.WHITE:
                        self._turnboard['text'] = 'White Won'
            else:
                self._turnboard['text'] = '---------------'
        except ValueError:
            pass
        
    def _on_canvas_resized(self, event: tkinter.Event) -> None:
        self._redraw_board()

    def _on_canvas_clicked(self, event: tkinter.Event) -> None:
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()
        x = event.x
        y = event.y

        try:
            col_coor = int(event.x/width*self._col)
            row_coor = int(event.y/height*self._row)
            
            if _SHOW_DEBUG_TRACE == True:
                print (row_coor,col_coor)

            if self._game_ended == False:
                self._take_coor((row_coor,col_coor))

            if self._game_started == True:
                self._game_words['text'] = "Continue by clicking the board."
                    
        except othello_logic2.InvalidMoveError:
            self._game_words['text'] = "This Move is INVALID"

        except AttributeError:
            pass

        
        self._redraw_board()

    def _on_next_button_clicked(self) -> None:
        if (self._got_inputs == True) and (self._game_started == False) and (self._game_ended == False):
            self._next += 1

        if _SHOW_DEBUG_TRACE == True:
            print('clicked',str(self._next))
            print(self._othello_game.board)

        if self._next == 1:
            self._game_words['text'] = "Please place the initial WHITE DISCS on the board. \nClick 'Next' when you are ready."
            self._init_con_color = othello_logic2.WHITE
            
        if (self._next == 2) and (self._game_ended == False):
            self._game_words['text'] = "The game is ON!! Continue by clicking the board."
            self._game_started = True

    def _on_start_button_clicked(self) -> None:
        self._got_inputs = False
        self._game_started = False
        self._next = 0
        self._game_ended = False
        
        _input_dialog = TakeInputs()
        _input_dialog._show()
        
        if _input_dialog._was_done_clicked():
            
            x = _input_dialog._get_all_info()
            self._got_inputs = True
            
            if _SHOW_DEBUG_TRACE == True:
               print ('RECV:', x)
            
            self._col, self._row, self._first_move, self._winning_con = x
            self._othello_game = othello_logic2.Othello(self._row, self._col, self._first_move, self._winning_con)
            
            self._start_game()
            self._redraw_board()

    def _take_init_con(self) -> None:
        self._game_words['text'] = "Please place the initial BLACK DISCS on the board.\nClick 'Next' when you are ready."
        self._init_con_color = othello_logic2.BLACK

    def _start_game(self) -> None:
        self._canvas['height'] = 400*self._row/self._col
        self._take_init_con()

    def _take_coor(self, coor:tuple) -> None:
        if self._game_started == True:
            self._othello_game.put_down_color((coor[0],coor[1]))
        elif self._game_started == False:
            self._othello_game.give_init_con(self._init_con_color, coor)

    def _redraw_board(self) -> None:
        self._canvas.delete(tkinter.ALL)
        
        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()

        self._update_scoreboard()
        self._update_turnboard()
        
        try:
            for i in range(self._col-1):
                self._canvas.create_line(
                    canvas_width*(i+1)/self._col, 0,
                    canvas_width*(i+1)/self._col, canvas_height)

            for i in range(self._row-1):
                self._canvas.create_line(
                    0, canvas_height*(i+1)/self._row,
                    canvas_width, canvas_height*(i+1)/self._row)

            for row_coor in range(len(self._othello_game.board)):
                for col_coor in range(len(self._othello_game.board[row_coor])):
                    if self._othello_game.board[row_coor][col_coor] == othello_logic2.BLACK:
                        self._canvas.create_oval(canvas_width*col_coor/self._col,
                                                 canvas_height*row_coor/self._row,
                                                 canvas_width*(col_coor+1)/self._col,
                                                 canvas_height*(row_coor+1)/self._row,
                                                 fill = 'black')
                    if self._othello_game.board[row_coor][col_coor] == othello_logic2.WHITE:
                        self._canvas.create_oval(canvas_width*col_coor/self._col,
                                                 canvas_height*row_coor/self._row,
                                                 canvas_width*(col_coor+1)/self._col,
                                                 canvas_height*(row_coor+1)/self._row,
                                                 fill = 'white')
                                          
                                          
            
        except AttributeError:
            pass


    def run(self) -> None:
        self._root_window.mainloop()


if __name__ == '__main__':
#    x = TakeInputs()._get_all_info()
    OthelloApplication().run()
