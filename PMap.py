from PGridspace import Gridspace
import Queue

class Map:
    """
    This class will oversee the state of the current screen
    """
    __gridspaces = []
    __enemies = None
    __finished = None
    
    def __init__(self, __enemies = [], __finished = False):
        for i in range(16):
            col=[]
            for j in range(13):
                col.append(Gridspace())
            self.__gridspaces.append(col)
        for i in range(6):
            self.__gridspaces[15][2*i+1].set_occupiable(False)
        self.__enemies = __enemies
        self.__finished = __finished
        
    def get_gridspaces(self):
        return self.__gridspaces
    
    def set_gridspaces(self, __gridspaces):
        self.__gridspaces = __gridspaces
        
    def get_enemies(self):
        return self.__enemies
    
    def set_enemies(self, __enemies):
        self.__enemies = __enemies
        
    def get_finished(self):
        return self.__finished
    
    def set_finished(self, __finished):
        self.__finished = __finished
        
    #calculates path from gridspace(x1,y1) to gridspace(x2,y2)
    #returns a list of index pairs
    def calculate_path(self, pos_x1, pos_y1, pos_x2, pos_y2):
        maze = []
        for i in range(16):
            col=[]
            for j in range(13):
                if self.__gridspaces[i][j].get_occupiable():
                    col.append(0)
                else:
                    col.append(1)
            maze.append(col)
        q = Queue.Queue()
        q.put([pos_x1,pos_y1])
        maze[pos_x1][pos_y1] = 2
        maze[pos_x2][pos_y2] = 3
        found = False
        while not(found):
            next = q.get()
            if next[1] > 0:
                if maze[next[0]][next[1]-1] == 3:
                    found = True
                    maze[next[0]][next[1]-1] = [next[0], next[1]]
                elif maze[next[0]][next[1]-1] == 0:
                    maze[next[0]][next[1]-1] = [next[0], next[1]]
                    q.put([next[0],next[1]-1])
            if next[0] > 0:
                if maze[next[0]-1][next[1]] == 3:
                    found = True
                    maze[next[0]-1][next[1]] = [next[0], next[1]]
                elif maze[next[0]-1][next[1]] == 0:
                    maze[next[0]-1][next[1]] = [next[0], next[1]]
                    q.put([next[0]-1,next[1]])
            if next[1] < 12:
                if maze[next[0]][next[1]+1] == 3:
                    found = True
                    maze[next[0]][next[1]+1] = [next[0], next[1]]
                elif maze[next[0]][next[1]+1] == 0:
                    maze[next[0]][next[1]+1] = [next[0], next[1]]
                    q.put([next[0],next[1]+1])
            if next[0] < 15:
                if next[1] > 0:
                    if maze[next[0]+1][next[1]-1] == 3:
                        found = True
                        maze[next[0]+1][next[1]-1] = [next[0], next[1]]
                    elif maze[next[0]+1][next[1]-1] == 0:
                        maze[next[0]+1][next[1]-1] = [next[0], next[1]]
                        q.put([next[0]+1,next[1]-1])
                if next[1] < 12
                    if maze[next[0]+1][next[1]+1] == 3:
                        found = True
                        maze[next[0]+1][next[1]+1] = [next[0], next[1]]
                    elif maze[next[0]+1][next[1]+1] == 0:
                        maze[next[0]+1][next[1]+1] = [next[0], next[1]]
                        q.put([next[0]+1,next[1]+1])
                if maze[next[0]+1][next[1]] == 3:
                    found = True
                    maze[next[0]+1][next[1]] = [next[0], next[1]]
                elif maze[next[0]+1][next[1]] == 0:
                    maze[next[0]+1][next[1]] = [next[0], next[1]]
                    q.put([next[0]+1,next[1]])
        there = False
        curr = [pos_x2,pos_y2]
        path = []
        while not(there):
            path.append(curr)
            curr = maze[curr[0]][curr[1]]
            if curr == 2:
                there = True
        path.append([pos_x1, pos_y1])
        return path.reverse()