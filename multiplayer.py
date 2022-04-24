from rich.table import Table
from rich.console import Console

console = Console()


class Game:
    def __init__(self):
        self.reset_board()

    def print_board(self):
        # print("\n")
        # print(" | ".join(self.board[0]))
        # print("---------")
        # print(" | ".join(self.board[1]))
        # print("---------")
        # print(" | ".join(self.board[2]))
        # print("\n")

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


    def update_postion(self, letter, pos):
        if self.space_free(pos):
            if pos <= 3:
                self.board[0][pos-1] = letter
            elif pos <= 6:
                self.board[1][pos-4] = letter
            elif pos <= 9:
                self.board[2][pos-7] = letter    

            if self.check_draw():
                self.print_board()
                print("\nDraw!")
                exit(0)
            
            if self.check_win():
                self.print_board()
                print("\nYay {} wins!".format(letter))
                exit(0)

            return True

        else:
            print("Can't place {} here because space is already full".format(letter))
            position = int(input("Enter position (1-9): "))
            self.update_postion(letter, position)
            return True

    
    def player_move(self, letter):
        position = int(input(f"Enter position to move {letter}: "))
        self.update_postion(letter, position)
        return

    def player2_move(self, letter):
        position = int(input(f"Enter position to move {letter}: "))
        self.update_postion(letter, position)
        return


    def start(self, player, player2):
        while not self.check_win():
            self.player_move(player)
            self.print_board()
            self.player2_move(player2)
            self.print_board()


game = Game()
game.print_board()

def choose_player_letter():
    player2, player = "X", "O"
        
    while True:
        player = input("X or O: ")
        if player.lower() == "x":
            player2 = "O"
            break
        elif player.lower() == "o":
            player2 = "X"
            break
        else:
            console.print("[red]Invalid choice (X/O)")

    return [player, player2]


letters = choose_player_letter()
game.start(letters[0], letters[1])