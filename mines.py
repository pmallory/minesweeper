import random
import sys

BOARD_WIDTH  = 8
BOARD_HEIGHT = 8
MINE_COUNT = 10

class Board:
    def __init__(self):
        self.mines = set()
        self.flags = set()
        self.explored = {} # (row, col) -> number of neighboring mines
        self._initialize_mines()

    def __str__(self):
        out = ' ABCDEFGH\n' #column labels
        for row in range(BOARD_HEIGHT):
            out += str(row) #row labels
            for col in range(BOARD_WIDTH):
                if (row, col) in self.explored:
                    out += str(self.explored[(row, col)])
                elif (row, col) in self.flags:
                    out += '⚑'
                else:
                    out += ' '
            out += '\n'

        out += self.status_line

        return out

    def _initialize_mines(self):
        assert self.mines == set()

        while len(self.mines) != MINE_COUNT:
            row, col = random.randrange(BOARD_HEIGHT), random.randrange(BOARD_WIDTH)
            if (row, col) not in self.mines:
                    self.mines.add((row,col))

    @property
    def status_line(self):
        return "there's some stuff" #TODO

    def bombat(self, row, col):
        return (row, col) in self.mines

    def flag(self, row, col):
        self.flags.add((row,col))

    def explore(self, row, col):
        neighboring_mine_count = self.count_neighbors(row, col)
        self.explored[(row, col)] = neighboring_mine_count
        if neighboring_mine_count == 0:
            #import pdb; pdb.set_trace()
            for roff in [-1, 0, 1]:
                for coff in [-1, 0, 1]:
                    neighbor_row, neighbor_col = row + roff, col+coff
                    if (row, col) == (neighbor_row, neighbor_col):
                        continue
                    if neighbor_row < 0 or neighbor_row >= BOARD_HEIGHT:
                        continue
                    if neighbor_col < 0 or neighbor_col >= BOARD_WIDTH:
                        continue
                    if (neighbor_row, neighbor_col) in self.explored:
                        continue
                    self.explore(neighbor_row, neighbor_col)

    def count_neighbors(self, row, col):
        count = 0

        for roff in [-1, 0, 1]:
            for coff in [-1, 0, 1]:
                neighbor_row, neighbor_col = row + roff, col+coff
                if (row, col) == (neighbor_row, neighbor_col):
                    continue
                if neighbor_row < 0 or neighbor_row >= BOARD_HEIGHT:
                    continue
                if neighbor_col < 0 or neighbor_col >= BOARD_WIDTH:
                    continue

                if (neighbor_row, neighbor_col) in self.mines:
                    count += 1

        return count

    def check_solution(self):
        return self.flags == self.mines


class Game:
    def __init__(self):
        self.board = Board()
        self.gameover = False
        self.mines_left = MINE_COUNT

    def take_turn(self, row, col, place_flag):
        if place_flag:
            self.board.flag(row, col)
        else:
            if self.board.bombat(row, col):
                self.gameover = True
            else:
                self.board.explore(row, col)

    def get_input(self):
        """asks the player to zainput which square to explore"""
        s = input("What square to explore? ")

        if len(s) < 2 or len(s) > 3: #TODO make error checking more robust
            print("bad input!")
            return self.get_input()

        row = int(s[0])

        col = s[1]
        #translate column labels A, B, C,... to 0, 1, 2, ...
        col = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.index(col.upper())

        mark = (len(s) == 3 and s[2] =='m')

        return row, col, mark


    def play(self):
        while not self.gameover:
            print(self.board)
            self.take_turn(*self.get_input())
            if self.board.check_solution():
                sys.exit()



if __name__ == '__main__':
    g = Game()
    g.play()

