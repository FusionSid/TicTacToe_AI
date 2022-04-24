# I have gotten so much brain damage from this that idk how im alive

from rich.table import Table
from rich.console import Console

console = Console()

class Game:
    def __init__(self):
        self.reset_board()

    def print_board(self):
        table = Table(show_lines=True, show_header=False, border_style="bold blue")
        for row in self.board:
            table.add_row(row[0], row[1], row[2], style="red")
        
        console.print(table)
    
    def reset_board(self):
        self.board = [
            [" ", " ", " "],
            [" ", " ", " "],
            [" ", " ", " "]
        ]


    def space_free(self, pos:int):
        if pos <= 3:
            position = self.board[0][pos-1]
        elif pos <= 6:
            position = self.board[1][pos-4]
        elif pos <= 9:
            position = self.board[2][pos-7]

        if position == " ":
            return True
        return False


    def check_draw(self):
        for row in self.board:
            for item in row:
                if item == " ":
                    return False

        return True


    def check_win(self):
        # Horizontal Wins
        for row in self.board:
            if row[0] == row[1] and row[1] == row[2] and row[0] != " ":
                return True

        # Vertical Wins
        for i in range(3):
            if self.board[0][i] == self.board[1][i] and self.board[1][i] == self.board[2][i] and self.board[0][i] != " ":
                return True

        # Check for diagonal wins
        if self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2] and self.board[0][0] != " ":
            return True

        elif self.board[0][2] == self.board[1][1] and self.board[1][1] == self.board[2][0] and self.board[0][2] != " ":
            return True

        return False

    def check_mark_win(self, mark):
        # Horizontal Wins
        for row in self.board:
            if row[0] == row[1] and row[1] == row[2] and row[0] == mark:
                return True

        # Vertical Wins
        for i in range(3):
            if self.board[0][i] == self.board[1][i] and self.board[1][i] == self.board[2][i] and self.board[0][i] == mark:
                return True

        # Check for diagonal wins
        if self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2] and self.board[0][0] == mark:
            return True

        elif self.board[0][2] == self.board[1][1] and self.board[1][1] == self.board[2][0] and self.board[0][2] == mark:
            return True

        return False


    def update_postion(self, letter, pos):
        if self.space_free(pos):
            if pos <= 3:
                self.board[0][pos-1] = letter
            elif pos <= 6:
                self.board[1][pos-4] = letter
            elif pos <= 9:
                self.board[2][pos-7] = letter    

            if self.check_win():
                self.print_board()
                print("\nYay {} wins!".format(letter))
                exit(0)

            if self.check_draw():
                self.print_board()
                print("\nDraw!")
                exit(0)
            

            return True

        else:
            print("Can't place {} at {} because space is already full".format(letter, pos))
            position = int(input("Enter position (1-9): "))
            self.update_postion(letter, position)
            return True

    
    def player_move(self, letter):
        try:
            position = int(input(f"Enter position to move {letter}: "))
            if position > 9 or position < 1:
                raise ValueError
        except ValueError:
            return self.player_move(letter)

        self.update_postion(letter, position)
        return

    def bot_move(self, letter):
        best_score, best_move = -100, None

        for row_id, row in enumerate(self.board):
            for index, key in enumerate(row):
                if key == " ":
                    self.board[row_id][index] = letter
                    score = self.minimax(letter, self.board, 0, False)
                    self.board[row_id][index] = " "
                    if score > best_score:
                        best_score = score

                        index +=1
                        if row_id == 0:
                            best_move = index
                        elif row_id == 1:
                            best_move = index + 3
                        elif row_id == 2:
                            best_move = index + 6
        return self.update_postion(letter, best_move)


    def minimax(self, bot, board, depth, isMaximizing):
        player = "X" if bot == "O" else "O"
        if self.check_mark_win(bot):
            return 100

        elif self.check_mark_win(player):
            return -100

        elif self.check_draw():
            return 0

        if isMaximizing:
            best_score = -1000

            for row_id, row in enumerate(board):
                for index, key in enumerate(row):
                    if key == " ":
                        board[row_id][index] = bot
                        score = self.minimax(bot, board, 0, False)
                        board[row_id][index] = " "
                        if score > best_score:
                            best_score = score

            return best_score

        else:
            best_score = 800

            for row_id, row in enumerate(board):
                for index, key in enumerate(row):
                    if key == " ":
                        board[row_id][index] = player
                        score = self.minimax(bot, board, 0, True)
                        board[row_id][index] = " "
                        if score < best_score:
                            best_score = score

            return best_score


    def start(self, player, bot):
        while not self.check_win():
            self.player_move(player)
            self.print_board()
            self.bot_move(bot)
            self.print_board()


game = Game()
game.print_board()

def choose_player_letter():
    bot, player = "X", "O"
        
    while True:
        player = input("X or O: ")
        if player.lower() == "x":
            bot = "O"
            break
        elif player.lower() == "o":
            bot = "X"
            break
        else:
            console.print("[red]Invalid choice (X/O)")

    return [player, bot]


letters = choose_player_letter()
game.start(letters[0], letters[1])