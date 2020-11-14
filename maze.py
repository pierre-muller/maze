import os
import random
import time

# Define maze size
NUM_ROWS = 30
NUM_COLS = 40
TIME_RES = 0.1

class maze():

    def __init__(self):
        self.rows = NUM_ROWS
        self.cols = NUM_COLS
        self.maze = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append("X")
            self.maze.append(row)


    def __str__(self):
        """
        return formatted maze with coordinates
        """
        ret = "XX\t"  + "".join(["{}".format(i%10) for i in range(self.cols)]) + os.linesep *2
        for i in range(self.rows):
            ret += "{}".format(i) + "\t" + "".join(self.maze[i]) + os.linesep
        return ret

    def generate(self):
        """
        Based on randomized Prim's algorithm
        description available at https://en.wikipedia.org/wiki/Maze_generation_algorithm#Randomized_Prim's_algorithm
        """
        # seed random func
        random.seed()
        # open door on left side at random position
        leftDoorRowIdx = random.randint(1, self.rows -2)
        self.maze[leftDoorRowIdx][0] = " "
        # initialize walls list with neighbour of the door
        walls = []
        walls.append((leftDoorRowIdx, 1))
        self.maze[leftDoorRowIdx][1] = "+" # mark this wall as active
        exitFound = False
        yield self

        while walls:
            # get random cell from walls list
            idx = random.randint(0, len(walls) -1)
            x, y = walls[idx]
            del walls[idx]
            if x== 0 or x == self.rows-1 or y ==0 or (y == self.cols -1 and exitFound):
                self.maze[x][y] = "X"
                continue # do not open walls on boundary of maze (except exit)
            if y == self.cols-1 and not exitFound: 
                # open exit
                self.maze[x][y] = " " 
                exitFound = True
                continue
            # check if wall has only 1 neighbour (out of four: left, right, up, down) that is part of the maze
            neighbours = [(x-1, y), (x+1, y), (x,y-1), (x, y+1)]
            if [self.maze[k][l] for k, l in neighbours].count(" ") == 1:
                # if true add wall to maze
                self.maze[x][y] = " "
                # add walls of the new cell to the walls list
                for (k, l) in [ (k, l) for (k,l) in neighbours if self.maze[k][l] != " "]:
                    walls.append((k, l))
                    self.maze[k][l] = "+"
                yield self
            else:
                self.maze[x][y] = "X"

    def generateAnimate(self):
        g = self.generate()
        for _ in g:
            print(self)
            time.sleep(TIME_RES)
        print(self)

    def generateFinal(self):
        g = self.generate()
        for _ in g:
            pass
        print(self)

    def solve(self):
        """
        Solve maze using Trémaux's algorithm (depth first search)
        https://en.wikipedia.org/wiki/Maze_solving_algorithm#Tr%C3%A9maux's_algorithm
        """
        
        rowIdxStart = [self.maze[i][0] for i in range(self.rows) ].index(" ")
        self.maze[rowIdxStart][0] = "."       
        self.maze[rowIdxStart][1] = "."       
        # store current cell coordinates in x and y
        x, y = rowIdxStart, 1
        yield self
        while True:
            neighbours = [(x-1, y), (x+1, y), (x,y-1), (x, y+1)]
            # next possible move is a neighbour that is unmarked
            nextPossibleMoves = [(k, l) for (k,l) in neighbours if self.maze[k][l] == " "]
            if not nextPossibleMoves:
                # mark as dead-end and go back
                self.maze[x][y] = ":"
                for k, l in neighbours:
                    if self.maze[k][l] == ".":
                        x, y = k, l
                        yield self
                        break
            else:
                idxNext = random.randint(0, len(nextPossibleMoves)-1)
                x, y = nextPossibleMoves[idxNext]
                self.maze[x][y] = "."
                if y==self.cols-1:
                    return self
                yield self


    def solveAnimate(self):
        g = self.solve()
        for _ in g:
            print(self)
            time.sleep(TIME_RES)
        print(self)

    def solveFinal(self):
        g = self.solve()
        for _ in g:
            pass
        print(self)


    def resetSolution(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.maze[i][j] == "." or self.maze[i][j] == ":" :
                    self.maze[i][j] = " "
