class Piece:
    def __init__(self, color, king=False):
        self.color = color  # 'b' or 'w'
        self.king = king

    def __repr__(self):
        base = 'B' if self.color == 'b' else 'W'
        return base + ('K' if self.king else ' ')


class Board:
    SIZE = 8

    def __init__(self):
        self.board = [[None for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self.setup()

    def setup(self):
        # Place black pieces (top of board)
        for row in range(3):
            for col in range(self.SIZE):
                if (row + col) % 2 == 1:
                    self.board[row][col] = Piece('b')
        # Place white pieces (bottom of board)
        for row in range(5, self.SIZE):
            for col in range(self.SIZE):
                if (row + col) % 2 == 1:
                    self.board[row][col] = Piece('w')

    def display(self):
        print('  a b c d e f g h')
        for row in range(self.SIZE):
            line = []
            for col in range(self.SIZE):
                piece = self.board[row][col]
                if piece is None:
                    line.append('.')
                else:
                    line.append(repr(piece))
            print(f"{self.SIZE - row} " + ' '.join(line))
        print()

    def in_bounds(self, row, col):
        return 0 <= row < self.SIZE and 0 <= col < self.SIZE

    def parse_pos(self, pos):
        if len(pos) != 2:
            raise ValueError('position must be letter+number')
        col = ord(pos[0].lower()) - ord('a')
        row = self.SIZE - int(pos[1])
        if not self.in_bounds(row, col):
            raise ValueError('position out of bounds')
        return row, col

    def move_piece(self, start, end, player):
        sr, sc = start
        er, ec = end
        piece = self.board[sr][sc]
        if piece is None or piece.color != player:
            return False
        if self.board[er][ec] is not None:
            return False
        dr = er - sr
        dc = ec - sc
        forward = 1 if player == 'b' else -1
        if abs(dr) == 1 and abs(dc) == 1:
            if piece.king or dr == forward:
                self.board[er][ec] = piece
                self.board[sr][sc] = None
                self._maybe_king(piece, er)
                return True
        if abs(dr) == 2 and abs(dc) == 2:
            mr = sr + dr // 2
            mc = sc + dc // 2
            mid = self.board[mr][mc]
            if mid is not None and mid.color != player:
                if piece.king or dr == 2 * forward:
                    self.board[er][ec] = piece
                    self.board[sr][sc] = None
                    self.board[mr][mc] = None
                    self._maybe_king(piece, er)
                    return True
        return False

    def _maybe_king(self, piece, row):
        if not piece.king:
            if piece.color == 'b' and row == self.SIZE - 1:
                piece.king = True
            elif piece.color == 'w' and row == 0:
                piece.king = True

    def has_pieces(self, color):
        for row in self.board:
            for piece in row:
                if piece and piece.color == color:
                    return True
        return False

    def has_moves(self, color):
        for r in range(self.SIZE):
            for c in range(self.SIZE):
                piece = self.board[r][c]
                if piece and piece.color == color:
                    moves = self.valid_moves((r, c))
                    if moves:
                        return True
        return False

    def valid_moves(self, pos):
        r, c = pos
        piece = self.board[r][c]
        if piece is None:
            return []
        directions = []
        if piece.king or piece.color == 'b':
            directions.append((1, -1))
            directions.append((1, 1))
        if piece.king or piece.color == 'w':
            directions.append((-1, -1))
            directions.append((-1, 1))
        moves = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if self.in_bounds(nr, nc) and self.board[nr][nc] is None:
                moves.append((nr, nc))
            # capture
            nr2, nc2 = r + 2 * dr, c + 2 * dc
            if (
                self.in_bounds(nr2, nc2)
                and self.board[nr][nc] is not None
                and self.board[nr][nc].color != piece.color
                and self.board[nr2][nc2] is None
            ):
                moves.append((nr2, nc2))
        return moves


class Game:
    def __init__(self):
        self.board = Board()
        self.turn = 'b'  # black starts

    def play(self):
        while True:
            self.board.display()
            if not self.board.has_pieces('b'):
                print('White wins!')
                break
            if not self.board.has_pieces('w'):
                print('Black wins!')
                break
            if not self.board.has_moves(self.turn):
                print(f"{'Black' if self.turn == 'b' else 'White'} has no moves. Game over.")
                break
            move = input(f"{'Black' if self.turn == 'b' else 'White'} move (e.g., b6 a5): ")
            parts = move.strip().split()
            if len(parts) != 2:
                print('Invalid input. Use: <from> <to>')
                continue
            try:
                start = self.board.parse_pos(parts[0])
                end = self.board.parse_pos(parts[1])
            except ValueError as exc:
                print('Error:', exc)
                continue
            if self.board.move_piece(start, end, self.turn):
                self.turn = 'w' if self.turn == 'b' else 'b'
            else:
                print('Invalid move')


if __name__ == '__main__':
    Game().play()
