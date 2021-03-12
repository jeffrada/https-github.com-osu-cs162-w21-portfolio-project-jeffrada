# Author: Adam Jeffries
# Date: 3/4/2021
# Description: A program that runs an abstract board game called Janggi.

class JanggiGame:
    '''
    Game class. Includes the board, pieces for the game as well as state members.
    Includes several methods including, but not limited to starting a new game, making moves and
    getting the current state of the game.
    '''

    def __init__(self):
        self.__pieces = self.new_pieces()
        self.__board = self.new_board(self.__pieces)
        self.make_moves_dicts()
        self.__game_state = "UNFINISHED"
        self.__whose_turn = 'R'
        self.__is_check = False
        self.__is_checkmate = False
        self.__is_stalemate = False

    def get_pieces(self):
        return self.__pieces

    def get_board(self):
        return self.__board

    def get_game_state(self):
        return self.__game_state

    def is_in_check(self, player):
        p = ''
        if self.__is_check:
            if player == 'red':
                p = 'R'
            elif player == 'black':
                p = 'B'
            if self.__is_check == p:
                return True
            else:
                return False

    def new_pieces(self):
        pieces = {
            Pawn('R', 3, 0), Pawn('R', 3, 2), Pawn('R', 3, 4), Pawn('R', 3, 6), Pawn('R', 3, 8),
            Pawn('B', 6, 0), Pawn('B', 6, 2), Pawn('B', 6, 4), Pawn('B', 6, 6), Pawn('B', 6, 8),
            Cannon('R', 2, 1), Cannon('R', 2, 7), Cannon('B', 7, 1), Cannon('B', 7, 7),
            Rook('R', 0, 0), Rook('R', 0, 8), Rook('B', 9, 0), Rook('B', 9, 8),
            Horse('R', 0, 1), Horse('R', 0, 7), Horse('B', 9, 1), Horse('B', 9, 7),
            Elephant('R', 0, 2), Elephant('R', 0, 6), Elephant('B', 9, 2), Elephant('B', 9, 6),
            Advisor('R', 0, 3), Advisor('R', 0, 5), Advisor('B', 9, 3), Advisor('B', 9, 5),
            General('R', 0, 4), General('B', 9, 4)
        }
        return pieces

    def new_board(self, pieces):
        empty_board = {}
        board = self.place_pieces(empty_board, pieces)
        return board

    def place_pieces(self, board, pieces):
        for piece in pieces:
            board[(piece.get_row(), piece.get_col())] = piece
        return board

    def find_occupant(self, space):
        if space in self.__board:
            return self.__board[space]
        return None

    def check_if_stalemate(self):
        are_moves = False
        for piece in self.__pieces:
            if len(piece.get_moves()) == 0:
                continue
            else:
                are_moves = True
            if are_moves:
                self.__is_stalemate = False
            else:
                self.__is_stalemate = True
                self.__game_state = 'GAME_OVER'

    def check_check_set_check(self, space, occupant):
        if occupant.get_type() == 'general':
            player = occupant.get_player()
            if self.__is_check == player:
                self.__is_checkmate = player
                if player == 'R':
                    self.__state = 'BLUE_WON'
                elif player == 'B':
                    self.__state = 'RED_WON'
            else:
                self.__is_check = player

    def check_if_flying_general(self):
        for piece in self.__pieces:
            if piece.get_type() == 'general':
                if self.helper_flying_general(piece, 1) or self.helper_flying_general(piece, -1):
                    return True

    def helper_flying_general(self, piece, j):
        flying_general = False
        i = 1
        row = piece.get_row()
        col = piece.get_col()
        while row + (j * i) in range(10):
            space = (row + (j * i), col)
            occupant = self.find_occupant(space)
            if occupant is not None:
                if occupant.get_type() == 'general':
                    flying_general = True
                    return flying_general
                else:
                    flying_general = False
                    return flying_general
            i += 1
        return flying_general

    def convert_coords_to_algnot(self, x, y):
        row_nums = [str(i) for i in range(1, 11)]
        col_lets = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        row = row_nums[x]
        col = col_lets[y]
        alg_pos = col + row
        return alg_pos

    def convert_algnot_to_coords(self, pos_str):
        col_lets = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        col = pos_str[0]
        row = pos_str[1]
        if col in col_lets:
            c = col_lets.index(col)
            r = int(row) - 1
            coord_pos = (r, c)
            return coord_pos

    def make_move(self, curr, to):
        curr = self.convert_algnot_to_coords(curr)
        to = self.convert_algnot_to_coords(to)
        occupant = self.set_up_for_move(curr, to)
        if occupant:
            if self.moving_moving(curr, to, occupant):
                if self.__game_state != 'UNFINISHED':
                    print(self.__game_state)
                    return True
        return False

    def set_up_for_move(self, curr, to):
        if curr[0] not in range(10) or curr[1] not in range(9):
            print('CURR off board D:')
            return False
        if to[0] not in range(10) or to[1] not in range(9):
            print('TO off board D:')
            return False
        occupant = self.find_occupant(curr)
        if occupant == None:
            print('No one here')
            return False
        turn = self.__whose_turn
        if occupant.get_player() != turn:
            print('Not your turn >:(')
            return False
        return occupant

    def moving_moving(self, curr, to, occupant):
        revert_board = self.__board
        revert_pieces = self.__pieces
        moves = occupant.get_moves()
        if to in moves:
            capture = moves[to]
            occupant.set_row(to[0])
            occupant.set_col(to[1])
            self.__board[curr] = None
            self.__board[to] = occupant
            if capture != None:
                self.__pieces.remove(capture)
            self.make_moves_dicts()
            if self.__is_check == occupant.get_player():
                self.__board = revert_board
                self.__pieces = revert_pieces
                self.make_moves_dicts()
                return False
            if self.check_if_flying_general():
                self.__board = revert_board
                self.__pieces = revert_pieces
                self.make_moves_dicts()
                return False
            self.check_if_stalemate()
            if self.__whose_turn == 'R':
                self.__whose_turn = 'B'
            elif self.__whose_turn == 'B':
                self.__whose_turn = 'R'
                return True
            return False

    def make_moves_dicts(self):
        for piece in self.__pieces:
            if piece.get_type() == 'pawn':
                piece.set_moves(self.make_pawn_moves(piece))
            elif piece.get_type() == 'cannon':
                piece.set_moves(self.make_cannon_moves(piece))
            elif piece.get_type() == 'rook':
                piece.set_moves(self.make_rook_moves(piece))
            elif piece.get_type() == 'horse':
                piece.set_moves(self.make_horse_moves(piece))
            elif piece.get_type() == 'elephant':
                piece.set_moves(self.make_elephant_moves(piece))
            elif piece.get_type() == 'advisor':
                piece.set_moves(self.make_advisor_moves(piece))
            elif piece.get_type() == 'general':
                piece.set_moves(self.make_general_moves(piece))

    def make_pawn_moves(self, piece):
        moves = {}
        piece_player = piece.get_player()
        row = piece.get_row()
        if piece_player == 'R':
            self.helper_pawn_moves(piece, moves, 1, 0)
        if row > 4:
            self.helper_pawn_moves(piece, moves, 0, 1)
            self.helper_pawn_moves(piece, moves, 0, -1)
        if piece_player == 'B':
            self.helper_pawn_moves(piece, moves, -1, 0)
        if row < 5:
            self.helper_pawn_moves(piece, moves, 0, 1)
            self.helper_pawn_moves(piece, moves, 0, -1)
        return moves

    def helper_pawn_moves(self, piece, moves, j, k):
        piece_player = piece.get_player()
        row = piece.get_row()
        col = piece.get_col()
        if row + j in range(10) and col + k in range(9):
            space = (row + j, col + k)
            occupant = self.find_occupant(space)
            if occupant is None:
                moves[space] = occupant
            elif occupant.get_player() != piece_player:
                moves[space] = occupant
                self.check_check_set_check(space, occupant)

    def make_cannon_moves(self, piece):
        moves = {}
        self.helper_cannon_moves(piece, moves, 1, 0)
        self.helper_cannon_moves(piece, moves, -1, 0)
        self.helper_cannon_moves(piece, moves, 0, 1)
        self.helper_cannon_moves(piece, moves, 0, -1)
        return moves

    def helper_cannon_moves(self, piece, moves, j, k):
        between = None
        row = piece.get_row()
        col = piece.get_col()
        piece_player = piece.get_player()
        i = 1
        while row + (j * i) in range(10) and col + (k * i) in range(9):
            space = (row + (j * i), col + (k * i))
            occupant = self.find_occupant(space)
            if between == None:
                if occupant == None:
                    moves[space] = occupant
                    i += 1
                else:
                    between = occupant
                    i += 1
            else:
                if occupant == None:
                    i += 1
                elif occupant.get_player() != piece_player:
                    moves[space] = occupant
                    self.check_check_set_check(space, occupant)
                    break
                else:
                    break

    def make_rook_moves(self, piece):
        moves = {}
        self.helper_rook_moves(piece, moves, 1, 0)
        self.helper_rook_moves(piece, moves, -1, 0)
        self.helper_rook_moves(piece, moves, 0, 1)
        self.helper_rook_moves(piece, moves, 0, -1)
        return moves

    def helper_rook_moves(self, piece, moves, j, k):
        row = piece.get_row()
        col = piece.get_col()
        piece_player = piece.get_player()
        i = 1
        while row + (j * i) in range(10) and col + (k * i) in range(9):
            space = (row + (j * i), col + (k * i))
            occupant = self.find_occupant(space)
            if occupant == None:
                moves[space] = occupant
                i += 1
            elif occupant.get_player() != piece_player:
                moves[space] = occupant
                self.check_check_set_check(space, occupant)
                break
            else:
                break
        return moves

    def make_horse_moves(self, piece):
        moves = {}
        self.helper_horse_moves(piece, moves, 1, 0, 1, 1)
        self.helper_horse_moves(piece, moves, 1, 0, 1, -1)
        self.helper_horse_moves(piece, moves, -1, 0, -1, 1)
        self.helper_horse_moves(piece, moves, -1, 0, -1, -1)
        self.helper_horse_moves(piece, moves, 0, 1, 1, 1)
        self.helper_horse_moves(piece, moves, 0, 1, -1, 1)
        self.helper_horse_moves(piece, moves, 0, -1, 1, -1)
        self.helper_horse_moves(piece, moves, 0, -1, -1, -1)
        return moves

    def helper_horse_moves(self, piece, moves, j, k, h, i):
        row = piece.get_row()
        col = piece.get_col()
        piece_player = piece.get_player()
        if row + j in range(10) and col + k in range(9):
            between = (row + j, col + k)
            if self.find_occupant(between) is not None:
                return
            elif between[0] + h in range(10) and between[1] + i in range(9):
                space = (between[0] + h, between[1] + i)
                occupant = self.find_occupant(space)
                if occupant is None:
                    moves[space] = occupant
                elif occupant.get_player() != piece_player:
                    moves[space] = occupant
                    self.check_check_set_check(space, occupant)
                else:
                    return

    def make_elephant_moves(self, piece):
        moves = {}
        self.helper_elephant_moves(piece, moves, 1, 1)
        self.helper_elephant_moves(piece, moves, 1, -1)
        self.helper_elephant_moves(piece, moves, -1, 1)
        self.helper_elephant_moves(piece, moves, -1, -1)
        return moves

    def helper_elephant_moves(self, piece, moves, j, k):
        piece_player = piece.get_player()
        row = piece.get_row()
        col = piece.get_col()
        if piece_player == 'R':
            if row + (2 * j) in range(5) and col + (2 * k) in range(9):
                space = (row + (2 * j), col + (2 * k))
                between = (row + j, col + k)
                if self.find_occupant(between) == None:
                    occupant = self.find_occupant(space)
                    if occupant == None:
                        moves[space] = occupant
                    elif occupant.get_player() != piece_player:
                        moves[space] = occupant
                        self.check_check_set_check(space, occupant)
        if piece_player == 'B':
            if row + (2 * j) in range(5, 10) and col + (2 * k) in range(9):
                space = (row + (2 * j), col + (2 * k))
                between = (row + j, col + k)
                if self.find_occupant(between) == None:
                    occupant = self.find_occupant(space)
                    if occupant == None:
                        moves[space] = occupant
                    elif occupant.get_player() != piece_player:
                        moves[space] = occupant
                        self.check_check_set_check(space, occupant)

    def make_advisor_moves(self, piece):
        moves = {}
        self.helper_advisor_moves(piece, moves, 1, 1)
        self.helper_advisor_moves(piece, moves, 1, -1)
        self.helper_advisor_moves(piece, moves, -1, 1)
        self.helper_advisor_moves(piece, moves, -1, -1)
        return moves

    def helper_advisor_moves(self, piece, moves, j, k):
        piece_player = piece.get_player()
        row = piece.get_row()
        col = piece.get_col()
        if piece_player == 'R':
            if row + j in range(3) and col + k in range(3, 6):
                space = (row + j, col + k)
                occupant = self.find_occupant(space)
                if occupant == None:
                    moves[space] = occupant
                elif occupant.get_player() != piece_player:
                    moves[space] = occupant
        if piece_player == 'B':
            if row + j in range(7, 10) and col + k in range(3, 6):
                space = (row + j, col + k)
                occupant = self.find_occupant(space)
                if occupant == None:
                    moves[space] = occupant
                elif occupant.get_player() != piece_player:
                    moves[space] = occupant
                    self.check_check_set_check(space, occupant)
        return moves

    def make_general_moves(self, piece):
        moves = {}
        self.helper_general_moves(piece, moves, 1, 0)
        self.helper_general_moves(piece, moves, -1, 0)
        self.helper_general_moves(piece, moves, 0, 1)
        self.helper_general_moves(piece, moves, 0, -1)
        return moves

    def helper_general_moves(self, piece, moves, j, k):
        piece_player = piece.get_player()
        row = piece.get_row()
        col = piece.get_col()
        if piece_player == 'R':
            if row + j in range(3) and col + k in range(3, 6):
                space = (row + j, col + k)
                occupant = self.find_occupant(space)
                if occupant is None:
                    moves[space] = occupant
                elif occupant.get_player() != piece_player:
                    moves[space] = occupant
                    self.check_check_set_check(space, occupant)
        if piece_player == 'B':
            if row + j in range(7, 10) and col + k in range(3, 6):
                space = (row + j, col + k)
                occupant = self.find_occupant(space)
                if occupant is None:
                    moves[space] = occupant
                elif occupant.get_player() != piece_player:
                    moves[space] = occupant
                    self.check_check_set_check(space, occupant)

    def print_board(self):
        for item in self.__board.items():
            print(item)

    def show_board(self):
        print('-' * 82)
        print('| - | c0 | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 ', end='')
        row_labels = ['| r0 ', '| r1 ', '| r2 ', '| r3 ', '| r4 ', '| r5 ', '| r6 ', '| r7 ', '| r8 ', '| r9 ']
        sorted_keys = sorted(self.__board.keys())
        for row in range(10):
            print('|')
            print('-' * 82)
            print(row_labels[row], end='')
        for col in range(9):
            match = False
        for key in sorted_keys:
            if key[0] == row and key[1] == col:
                if self.__board[key] != None:
                    match = True
                    name = (self.__board[key]).get_name()
        if match:
            print('| ' + name, end=' ')
        else:
            print('| --- ', end='')
        print('|')
        print('-' * 82)
        print()
        for piece in self.__pieces:
            print(piece.get_name_pos(), piece.get_type(), end=': Moves: ')
            print(piece.get_moves())
        print()
        print(self.__game_state)

class Piece:

    def __init__(self, player, row, col):
        self.__name_pos = str(player) + str(row) + str(col)
        self.__player = player
        self.__row = row
        self.__col = col
        # self.__position = (row, col)
        self.__alg_pos = self.coords_to_alg_nots(row, col)
        self.__moves = {}

    def get_player(self):
        return self.__player

    def get_moves(self):
        return self.__moves

    def set_moves(self, moves):
        self.__moves = moves

    def get_row(self):
        return self.__row

    def set_row(self, row):
        self.__row = row

    def get_col(self):
        return self.__col

    def set_col(self, col):
        self.__col = col

    def get_alg_pos(self):
        return self.__alg_pos

    def get_name_pos(self):
        return self.__name_pos

    def coords_to_alg_nots(self, x, y):
        nums = [str(i) for i in range(1, 11)]
        lets = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        row = nums[self.__row]
        col = lets[self.__col]
        alg_pos = row + col
        return alg_pos


class Pawn(Piece):
    '''
    Represents the pawn piece in the game Janggi.
    '''
    def __init__(self, player, row, col):
        super().__init__(player, row, col)
        self.__type = 'pawn'
        self.__typeAb = 'Pn'
        self.__name = str(player).lower() + str(self.__typeAb)

    def get_type(self):
        return self.__type

    def get_typeAb(self):
        return self.__typeAb

    def get_name(self):
        return self.__name


class Cannon(Piece):
    '''
    Represents the cannon piece in the game Janggi.
    '''

    def __init__(self, player, row, col):
        super().__init__(player, row, col)
        self.__type = 'cannon'
        self.__typeAb = 'Cn'
        self.__name = str(player).lower() + str(self.__typeAb)

    def get_type(self):
        return self.__type

    def get_typeAb(self):
        return self.__typeAb

    def get_name(self):
        return self.__name


class Rook(Piece):
    '''
    Represents the rook piece in the game Janggi.
    '''

    def __init__(self, player, row, col):
        super().__init__(player, row, col)
        self.__type = 'rook'
        self.__typeAb = 'Rk'
        self.__name = str(player).lower() + str(self.__typeAb)

    def get_type(self):
        return self.__type

    def get_typeAb(self):
        return self.__typeAb

    def get_name(self):
        return self.__name


class Horse(Piece):
    '''
    Represents the horse piece in the game Janggi.
    '''

    def __init__(self, player, row, col):
        super().__init__(player, row, col)
        self.__type = 'horse'
        self.__typeAb = 'Hr'
        self.__name = str(player).lower() + str(self.__typeAb)

    def get_type(self):
        return self.__type

    def get_typeAb(self):
        return self.__typeAb

    def get_name(self):
        return self.__name


class Elephant(Piece):
    '''
    Represents the elephant piece in the game Janggi.
    '''

    def __init__(self, player, row, col):
        super().__init__(player, row, col)
        self.__type = 'elephant'
        self.__typeAb = 'El'
        self.__name = str(player).lower() + str(self.__typeAb)

    def get_type(self):
        return self.__type

    def get_typeAb(self):
        return self.__typeAb

    def get_name(self):
        return self.__name


class Advisor(Piece):
    '''
    Represents the advisor piece in the game Janggi.
    '''

    def __init__(self, player, row, col):
        super().__init__(player, row, col)
        self.__type = 'advisor'
        self.__typeAb = 'Ad'
        self.__name = str(player).lower() + str(self.__typeAb)

    def get_type(self):
        return self.__type

    def get_typeAb(self):
        return self.__typeAb

    def get_name(self):
        return self.__name


class General(Piece):
    '''
    Represents the general piece in the game Janggi.
    '''

    def __init__(self, player, row, col):
        super().__init__(player, row, col)
        self.__type = 'general'
        self.__typeAb = 'Gn'
        self.__name = str(player).lower() + str(self.__typeAb)

    def get_type(self):
        return self.__type

    def get_typeAb(self):
        return self.__typeAb

    def get_name(self):
        return self.__name
