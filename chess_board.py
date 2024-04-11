import aiomysql

class Piece:
    def __init__(self, color):
        self.color = color

    async def valid_move(self, start, end, board):
        raise NotImplementedError("Subclass must implement abstract method")

    def serialize(self):
        return str(self)

    def __str__(self):
        raise NotImplementedError("Subclass must implement abstract method")


class King(Piece):
    async def valid_move(self, start, end, board):
        if not (0 <= end[0] < 8 and 0 <= end[1] < 8):
            return False

        diff_x = abs(start[0] - end[0])
        diff_y = abs(start[1] - end[1])
        if diff_x <= 1 and diff_y <= 1:
            return True

        return False

    def __str__(self):
        return "♚" if self.color == "black" else "♔"


class Rook(Piece):
    async def valid_move(self, start, end, board):
        if not (0 <= end[0] < 8 and 0 <= end[1] < 8):
            return False

        if start[0] == end[0] or start[1] == end[1]:
            if start[0] == end[0]:
                step = 1 if end[1] > start[1] else -1
                for col in range(start[1] + step, end[1], step):
                    if board[start[0]][col] is not None:
                        return False
            else:
                step = 1 if end[0] > start[0] else -1
                for row in range(start[0] + step, end[0], step):
                    if board[row][start[1]] is not None:
                        return False
            return True

        return False

    def __str__(self):
        return "♜" if self.color == "black" else "♖"


class Knight(Piece):
    async def valid_move(self, start, end, board):
        if not (0 <= end[0] < 8 and 0 <= end[1] < 8):
            return False

        if abs(end[0] - start[0]) == 2 and abs(end[1] - start[1]) == 1:
            return True
        elif abs(end[0] - start[0]) == 1 and abs(end[1] - start[1]) == 2:
            return True

        return False

    def __str__(self):
        return "♞" if self.color == "black" else "♘"


class Bishop(Piece):
    async def valid_move(self, start, end, board):
        if not (0 <= end[0] < 8 and 0 <= end[1] < 8):
            return False

        diff_x = abs(start[0] - end[0])
        diff_y = abs(start[1] - end[1])
        if diff_x == diff_y:
            return True

        return False

    def __str__(self):
        return "♝" if self.color == "black" else "♗"


class Queen(Piece):
    async def valid_move(self, start, end, board):
        if not (0 <= end[0] < 8 and 0 <= end[1] < 8):
            return False

        diff_x = abs(start[0] - end[0])
        diff_y = abs(start[1] - end[1])
        if diff_x == diff_y or start[0] == end[0] or start[1] == end[1]:
            return True

        return False

    def __str__(self):
        return "♛" if self.color == "black" else "♕"


class Pawn(Piece):
    async def valid_move(self, start, end, board):
        if not (0 <= end[0] < 8 and 0 <= end[1] < 8):
            return False

        diff_x = abs(start[0] - end[0])
        diff_y = abs(start[1] - end[1])
        if diff_x == 1 and diff_y == 0:
            return True

        return False

    def __str__(self):
        return "♟" if self.color == "black" else "♙"


class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.initialize_board()

    async def initialize_board(self):
        self.board[0] = [Rook("black"), Knight("black"), Bishop("black"), Queen("black"), King("black"),
                         Bishop("black"), Knight("black"), Rook("black")]
        self.board[1] = [Pawn("black") for _ in range(8)]
        self.board[6] = [Pawn("white") for _ in range(8)]
        self.board[7] = [Rook("white"), Knight("white"), Bishop("white"), Queen("white"), King("white"),
                         Bishop("white"), Knight("white"), Rook("white")]

    async def is_valid_move(self, start, end):
        if not (0 <= end[0] < 8 and 0 <= end[1] < 8):
            return False

        piece = self.board[start[0]][start[1]]
        if not piece:
            return False

        return await piece.valid_move(start, end, self.board)

    async def move_piece(self, start, end):
        piece = self.board[start[0]][start[1]]
        self.board[start[0]][start[1]] = None
        self.board[end[0]][end[1]] = piece

    def serialize_board(self):
        serialized_board = []
        for i, row in enumerate(self.board):
            serialized_row = [str(7-i)] + [str(j) + str(piece) if piece is not None else ' ' + str(j) for j, piece in enumerate(row)]
            serialized_board.append(serialized_row)
        serialized_board.append([' ', '0', '1', '2', '3', '4', '5', '6', '7'])
        return serialized_board
