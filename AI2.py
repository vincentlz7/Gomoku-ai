from Heuristics import *
from GameMap import *
from random import randint


SCORE5 = 100000
SCORE4 = 10000
SCORE4_hole = 1000


depth = 3


MAX = 0x7fffffff
MIN = -0x7fffffff


class AI2():
    def __init__(self, len):
        self.len = len
        self.heuristics = Heuristics(len)
        self.record = [[[0,0,0,0] for x in range(self.len)] for y in range(self.len)]
        self.pos_score = [[(7 - max(abs(x - 7), abs(y - 7))) for x in range(self.len)] for y in range(self.len)]

    def get_random_pos(self):
        return randint(0, self.len),randint(0, self.len) 
    
    def click(self, map, x, y, turn):
        map.click(x, y, turn)
        
    def isWin(self, board, turn):
        return self.heuristics.evaluate(board, turn, True)

    def hasNeighbor(self, board, x, y, radius):
        start_x, end_x = (x - radius), (x + radius)
        start_y, end_y = (y - radius), (y + radius)

        for i in range(start_y, end_y+1):
            for j in range(start_x, end_x+1):
                if i >= 0 and i < self.len and j >= 0 and j < self.len:
                    if board[i][j] != 0:
                        return True
        return False


    #The upgraded heuristics
    def genmove(self, board, turn):
        fives = []
        mfours, ofours = [], []
        msfours, osfours = [], []
        if turn == MAP_ENTRY_TYPE.MAP_PLAYER_ONE:
            mine = 1
            opponent = 2
        else:
            mine = 2
            opponent = 1

        moves = []
        radius = 1
        for y in range(self.len):
            for x in range(self.len):
                if board[y][x] == 0 and self.hasNeighbor(board, x, y, radius):
                    mscore, oscore = self.heuristics.evaluatePointScore(board, x, y, mine, opponent)
                    point = (max(mscore, oscore), x, y)

                    if mscore >= SCORE5 or oscore >= SCORE5:
                        fives.append(point)
                    elif mscore >= SCORE4:
                        mfours.append(point)
                    elif oscore >= SCORE4:
                        ofours.append(point)
                    elif mscore >= SCORE4_hole:
                        msfours.append(point)
                    elif oscore >= SCORE4_hole:
                        osfours.append(point)

                    moves.append(point)
        if len(fives) > 0: 
            return fives

        if len(mfours) > 0: 
            return mfours

        if len(ofours) > 0:
            if len(msfours) == 0:
                return ofours
            else:
                return ofours + msfours

        moves.sort(reverse=True)
        if self.maxdepth > 2 and len(moves) > 20:
            moves = moves[:20]
        return moves
    
    def __search(self, board, turn, depth, alpha = MIN, beta = MAX):
        score = self.heuristics.evaluate(board, turn)
        if depth <= 0 or abs(score) >= 10000: 
            return score

        moves = self.genmove(board, turn)
        bestmove = None
        self.alpha += len(moves)
        if len(moves) == 0:
            return score

        for _, x, y in moves:
            board[y][x] = turn
            
            if turn == MAP_ENTRY_TYPE.MAP_PLAYER_ONE:
                op_turn = MAP_ENTRY_TYPE.MAP_PLAYER_TWO
            else:
                op_turn = MAP_ENTRY_TYPE.MAP_PLAYER_ONE

            score = - self.__search(board, op_turn, depth - 1, -beta, -alpha)

            board[y][x] = 0
            self.belta += 1
            if score > alpha:
                alpha = score
                bestmove = (x, y)
                if alpha >= beta:
                    break

        if depth == self.maxdepth and bestmove:
            self.bestmove = bestmove
                
        return alpha

    def search(self, board, turn, depth = 4):
        self.maxdepth = depth
        self.bestmove = None
        score = self.__search(board, turn, depth)
        if self.bestmove is None:
            self.bestmove = self.get_random_pos()
        x, y = self.bestmove
        return score, x, y
        
    def findBestChess(self, board, turn):
        self.alpha = 0
        self.belta = 0
        score, x, y = self.search(board, turn, depth)
        return (x, y)
    
    def findBestRandom(self,board, turn):
        self.alpha = 0
        self.belta = 0
        score, x, y = self.search(board, turn, depth)
        return (x, y)
