from PGridspace import Gridspace
import Queue

class Map:
    """
    This class will oversee the state of the current screen
    """
    __gridspaces = []
    __global_gridspaces = []
    __finished = None
    
    def __init__(self, __global_gridspaces = [], __finished = False):
        self.__global_gridspaces = __global_gridspaces
	counter = 201
	for i in range(16):
		self.__gridspaces.append([])
	for j in range(13):
		for i in range(16):
			if i == 15 and j%2==1:
				self.__gridspaces[i].append(1)
			else:
				if self.__global_gridspaces[counter].get_occupiable():
					self.__gridspaces[i].append(0)
					counter = counter - 1
				else:
					self.__gridspaces[i].append(1)
					counter = counter - 1
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
        
    #calculates path from gridspace1 to gridspace2
    #returns a list of indexes
    def calculate_path(self, gridspace1, gridspace2):
    	gridspace1 = 201 - gridspace1
	gridspace2 = 201 - gridspace2
        pos_x1 = (gridspace1 % 31) % 16
	pos_y1 = (gridspace1/31)*2+(gridspace1 % 31)/16
        pos_x2 = (gridspace2 % 31) % 16
	pos_y2 = (gridspace2/31)*2+(gridspace2 % 31)/16
	maze = []
        for i in range(16):
            col=[]
            for j in range(13):
                if self.__gridspaces[i][j] == 0:
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
	    	if next[1] > 0 and next[1] % 2 == 0:
			if maze[next[0]-1][next[1]-1] == 3:
				found = True
				maze[next[0]-1][next[1]-1] = [next[0],next[1]]
			elif maze[next[0]-1][next[1]-1] == 0:
				maze[next[0]-1][next[1]-1] = [next[0],next[1]]
				q.put([next[0]-1,next[1]-1])
		if next[1] < 12 and next[1] % 2 == 0:
			if maze[next[0]-1][next[1]+1] == 3:
				found = True
				maze[next[0]-1][next[1]+1] = [next[0],next[1]]
			elif maze[next[0]-1][next[1]+1] == 0:
				maze[next[0]-1][next[1]+1] = [next[0],next[1]]
				q.put([next[0]-1,next[1]+1])
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
                if next[1] > 0 and next[1] % 2 == 1:
                    if maze[next[0]+1][next[1]-1] == 3:
                        found = True
                        maze[next[0]+1][next[1]-1] = [next[0], next[1]]
                    elif maze[next[0]+1][next[1]-1] == 0:
                        maze[next[0]+1][next[1]-1] = [next[0], next[1]]
                        q.put([next[0]+1,next[1]-1])
		if next[1] < 12 and next[1] % 2 == 1:
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
        path.reverse()
	path_length = len(path)
	true_path = []
	for i in range(path_length):
		true_path.append(201-(path[i][1] * 16 + path[i][0] - path[i][1] / 2))
	return true_path

    def to_string(self):
        data = []
	for i in range (16):
	    for j in range (13):
	        data.append(self.__gridspaces[i][j].get_occupiable())
	return str(data)
