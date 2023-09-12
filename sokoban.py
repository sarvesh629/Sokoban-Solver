import os
import copy
from IPython.display import clear_output
import sys
import time
import numpy as np
import heapq as hq
import math

def floor_log(x):
    return math.frexp(x)[1] - 1

class nodes:
    def __init__(self,parent,state,pos,he,mov=""):  
        self.parent = parent   
        self.state = state
        self.pos = pos
        self.he = he
        self.str = ""
        self.box = []
        a = len(state)
        b = len(state[0])
        target = []
        player = tuple(self.pos)
        for i in range(0,a):
            line = state[i]
            for j in range(0,b):
                if line[j]==3:
                    self.box.append((i,j))
                elif line[j]==4:
                    target.append((i,j))
        self.box.append(tuple(target))
        self.box.append(player)
        self.box = tuple(self.box)
        if(parent==None):
            self.depth = 0
            self.mov = ""
        else:
            self.depth = parent.depth + 1
            self.mov = parent.mov + mov

class Linked_list:
    def __init__(self,node):  
        self.node = node
        self.next = None
        
class FibonacciTree:
    def __init__(self,value,node):
        self.value = value
        self.node = node
        self.child = []
        self.order = 0
    def add_at_end(self, t):
        self.child.append(t)
        self.order = self.order + 1
class FibonacciHeap:
    def __init__(self):
        self.trees = []
        self.least = None
        self.count = 0
    def insert_node(self,value,node):
        new_tree = FibonacciTree(value,node)
        self.trees.append(new_tree)
        if (self.least is None or value < self.least.value):
            self.least = new_tree
        self.count = self.count + 1

    # Extract the minimum value
    def extract_min(self):
        smallest = self.least
        if smallest is not None:
            for child in smallest.child:
                self.trees.append(child)
            self.trees.remove(smallest)
            if self.trees == []:
                self.least = None
            else:
                self.least = self.trees[0]
                self.consolidate()
            self.count = self.count - 1
            return smallest.node

    # Consolidate the tree
    def consolidate(self):
        aux = (floor_log(self.count) + 1) * [None]

        while self.trees != []:
            x = self.trees[0]
            order = x.order
            self.trees.remove(x)
            while aux[order] is not None:
                y = aux[order]
                if x.value > y.value:
                    x, y = y, x
                x.add_at_end(y)
                aux[order] = None
                order = order + 1
            aux[order] = x

        self.least = None
        for k in aux:
            if k is not None:
                self.trees.append(k)
                if (self.least is None or k.value < self.least.value):
                    self.least = k

# class PriorityQueue:
#     """Define a PriorityQueue data structure that will be used"""
#     def  __init__(self):
#         self.Heap = []
#         self.Count = 0

#     def push(self, item, priority):
#         entry = (priority, self.Count, item)
#         heapq.heappush(self.Heap, entry)
#         self.Count += 1

#     def pop(self):
#         (_, _, item) = heapq.heappop(self.Heap)
#         return item

#     def isEmpty(self):
#         return len(self.Heap) == 0
def printpu(state):
    numTochar = {0:' ',1:'@',2:'#',3:'$',4:'.',5:'*',6:'+'}
    string = ""
    for x in state:
        line_str = ""
        for y in x:
            line_str += numTochar[y]
        line_str += "\n"
        string += line_str
    return string


class Board():
    charTonum = {' ': 0, '@': 1,'#': 2,'$': 3,'.': 4,'*': 5,'+': 6}
    numTochar = {0:' ',1:'@',2:'#',3:'$',4:'.',5:'*',6:'+'}
    directions = [(0,-1),(0, 1),(-1, 0),(1,0)]
    dir = {(0,-1):"u",(0, 1):"d",(-1, 0):"l",(1,0):"r"}
    box = []
    wall = []
    goal=[]
    # In x,y format
    # UP Down Left Right 
    
    def isGoalNode(self,b):
        for i in b:
            for j in i:
                if j==3:return False
        return True

    def __init__(self, text):
        player = [0,0]
        self.lines = text.split("\n")
        Max = 0
        for i in range(0,len(self.lines)):
            if Max<len(self.lines[i]):
                Max = len(self.lines[i])
        self.width = Max
        self.height = len(self.lines)
        self.board = [[0 for i in range(self.width)]for j in range(0,self.height)]
        for i in range(0,self.height):
            line = self.lines[i]
            for j in range(0,len(line)):
                self.board[i][j] = self.charTonum[line[j]]
                if line[j]=='$' or line[j]=='*':
                    self.box.append((i,j))
                if line[j]=='.' or line[j]=='*':
                    self.goal.append((i,j))
                elif line[j]=='#':
                    self.wall.append((i,j))
                elif line[j]=='@' or line[j]=='+':
                    player[0] = j
                    player[1] = i
        self.cur = nodes(None,self.board.copy(),player,self.heuristic(self.board))
    
    def heuristic(self,state):
        goal = []
        box = []
        player = []
        for i in range(self.height):
            for j in range(self.width):
                if state[i][j] in [4,6]:
                    goal.append((i,j))
                elif state[i][j] in [3]:
                    box.append((i,j))
                if state[i][j] in [2,6]:
                    player.append((i,j))
        sum = 0
        # for i in box:
        #     for j in goal:
        #         if i[0]!=j[0]:
        #             sum+=1
        #         if  i[1]!=j[1]:
        #             sum+=1
        for i in range(0,len(goal)):
            x = goal[i]
            #print(x)
            min = 3000
            index = 0
            for j in range(0,len(box)):
                y = box[j]
                n=abs(x[0]-y[0])+abs(x[1]-y[1])
                if n<min:
                    min = n
                    index = j
            box.pop(index)
            sum+=min
        # if len(box)==1:
        #     for y in box:
        #         sum+=math.ceil(math.dist([player[0][0], player[0][1]], [y[0], y[1]]))
        return sum

    def printpuz(self):
        string = ""
        for x in range(self.height):
            line_str = ""
            for y in range(self.width):
                line_str += self.numTochar[self.cur.state[x][y]]
            line_str += "\n"
            string += line_str
        return string

    def end_test(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.numTochar[self.board[x][y]] == "$":
                    return False
        return True
    
    def posbox(self,initial):
        l = [0]*len(self.box)
        c=0
        for y in range(self.height):
            for x in range(self.width):
                if initial[y][x] in [3,5]:
                    l[c]=(y,x)
                    c+=1
        return l

    def deadlock_prune(self,y,x,initial):
    #def deadlock_prune(self,initial):
        rotatePattern = [[0,1,2,3,4,5,6,7,8],
                    [2,5,8,1,4,7,0,3,6],
                    [0,1,2,3,4,5,6,7,8][::-1],
                    [2,5,8,1,4,7,0,3,6][::-1]]
        flipPattern = [[2,1,0,5,4,3,8,7,6],
                        [0,3,6,1,4,7,2,5,8],
                        [2,1,0,5,4,3,8,7,6][::-1],
                        [0,3,6,1,4,7,2,5,8][::-1]]
        allPattern = rotatePattern + flipPattern
        posofBox = self.posbox(initial)
        for box in posofBox:
            if box not in self.goal:
                board = [(box[0] - 1, box[1] - 1), (box[0] - 1, box[1]), (box[0] - 1, box[1] + 1), 
                        (box[0], box[1] - 1), (box[0], box[1]), (box[0], box[1] + 1), 
                        (box[0] + 1, box[1] - 1), (box[0] + 1, box[1]), (box[0] + 1, box[1] + 1)]
                for pattern in allPattern:
                    newBoard = [board[i] for i in pattern]
                    # print(printpu(newBoard))
                    # time.sleep(2)
                    if newBoard[1] in self.wall and newBoard[5] in self.wall: 
                        #print(printpu(initial))
                        return True
                    elif newBoard[1] in posofBox and newBoard[2] in self.wall and newBoard[5] in self.wall:
                        #print(printpu(initial))
                        return True
                    elif newBoard[1] in posofBox and newBoard[2] in self.wall and newBoard[5] in posofBox: 
                        #print(printpu(initial))
                        return True
                    elif newBoard[1] in posofBox and newBoard[2] in posofBox and newBoard[5] in posofBox: 
                        #print(printpu(initial))
                        return True
                    elif newBoard[1] in posofBox and newBoard[6] in posofBox and newBoard[2] in self.wall and newBoard[3] in self.wall and newBoard[8] in self.wall: 
                        #print(printpu(initial))
                        return True
        
        # direc = [1,-1]
        # for i in direc:
        #     for j in direc:
        #         if initial[y+i][x] in [2,3,5] and initial[y+i][x+j] in [2,3,5] and initial[y][x+j] in [2,3,5] :
        #             return True
        # direc = [1,-1]
        # l = 0
        # r = 0
        # for i in range(x+1,self.width):
        #     if initial[y][i]==2:
        #         r = i
        #         break
        #     if initial[y][i] in [3,5]:
        #         if initial[y+1][i] not in [2,3,5] or initial[y-1][i] not in [2,3,5]:
        #             return False
        #         else:
        #             r = i
        #             break
        # i = x-1
        # while(i>=0):
        #     if initial[y][x-i]==2:
        #         l = x-i
        #         break
        #     if initial[y][x-i] in [3,5]:
        #         if initial[y+1][x-i] not in [2,3,5] or initial[y-1][x-i] not in [2,3,5]:
        #             return False
        #         else:
        #             l = x-i
        #             break
        #     i-=1
        # flag1=0
        # flag2=0
        # if l!=0 and r!=0:
        #     for i in range(l,r+1):
        #         if initial[y+1][i] not in [2,3]:
        #             flag1=1
        #         if initial[y-1][i] not in [2,3]:
        #             flag2=1
        #     if flag1==0:
        #         return True
        #     if flag2==0:
        #         return True


        # i = 0
        # j = 0
        # try:
        #     while(x+i<self.width):
        #         if initial[y][x+i] in [2,3,5]:
        #             while(x-i>=0):
        #                 if initial[y][x+i] in [0,2,3,5,6]:
        #                     flag1 = 1
        #                     flag2 = 1
        #                     for m in range(j,i):
        #                         if initial[y+1][m] not in [2,3,5]:
        #                             flag1 = 0
        #                         if initial[y-1][m] not in [2,3,5]:
        #                             flag2 = 0
        #                     if flag1==0 or flag2==0:
        #                         return True
        #                     else:
        #                         return False
        #         i+=1
        #         j+=1
        # except IndexError:
        #     print(printpu(self.cur.index))
        #     time.sleep(20)
        return False

    def NextMovePos(self,dir_num):
        move = self.directions[dir_num]
        currentX, currentY = self.cur.pos
        target_pos_x, target_pos_y = currentX + move[0], currentY + move[1]

        if dir_num == 0:  # Up
            future_pos_x = target_pos_x
            future_pos_y = target_pos_y - 1
        elif dir_num == 1:  # down
            future_pos_x = target_pos_x
            future_pos_y = target_pos_y + 1
        elif dir_num == 2:  # left
            future_pos_x = target_pos_x - 1
            future_pos_y = target_pos_y
        else:  # right
            future_pos_x = target_pos_x + 1
            future_pos_y = target_pos_y

        return future_pos_x, future_pos_y

    
    def get_moves(self):
        currentX = self.cur.pos[0]
        currentY = self.cur.pos[1]
        moves = []
        for move in self.directions:
            targetx = currentX + move[0]
            targety = currentY + move[1]
            l = self.NextMovePos(self.directions.index(move))
            futurex = l[0]
            futurey = l[1]
            if(targetx<self.width-1 and targety<self.height-1):
                targetcharacter = self.cur.state[targety][targetx]
                futurecharacter = self.cur.state[futurey][futurex]

                if targetcharacter in [self.charTonum['$'], self.charTonum['*']]:
                    if futurecharacter != self.charTonum['#']:
                        moves.append(move)
                elif targetcharacter != self.charTonum["#"]:
                    moves.append(move)
        return moves
    
    def PlayerPos(self,state):
        for y in range(self.height):
            for x in range(self.width):
                if state[y][x] == self.charTonum["@"] or state[y][x] == self.charTonum["+"]:
                    return (x, y)
        return None
    
    def can_move(self,x,y,move):
        if move in self.get_moves() and self.numTochar[self.cur.state[y+move[1]][x+move[0]]] not in ["$","*","#"]:
            return True
        return False
    
    def can_push(self,x,y,move):
        if move in self.get_moves() and self.numTochar[self.cur.state[y+move[1]][x+move[0]]] in ["*","$"] and self.numTochar[self.cur.state[y+move[1]*2][x+move[0]*2]] in [" ","."]:
            return True
        return False

    def move_box(self,x,y,a,b,initial):
        current_box = self.numTochar[initial[y][x]]
        future_box = self.numTochar[initial[y+b][x+a]]
        if current_box == '$' and future_box == ' ':
            initial[y+b][x+a] = self.charTonum["$"]
            initial[y][x] = self.charTonum[" "]
            
        elif current_box == '$' and future_box == '.':
            initial[y+b][x+a] = self.charTonum["*"]
            initial[y][x] = self.charTonum[" "]
            
        elif current_box == '*' and future_box == ' ':
            initial[y+b][x+a] = self.charTonum["$"]
            initial[y][x] = self.charTonum["."]
            
        elif current_box == '*' and future_box == '.':
            initial[y+b][x+a] = self.charTonum["*"]
            initial[y][x] = self.charTonum["."]
    
    def move_player(self,x,y,a,b,initial):
        current_box = self.numTochar[initial[y][x]]
        future_box = self.numTochar[initial[y+b][x+a]]
        if current_box == '@' and future_box == ' ':
            initial[y+b][x+a] = self.charTonum["@"]
            initial[y][x] = self.charTonum[" "]
            return True
        elif current_box == '@' and future_box == '.':
            initial[y+b][x+a] = self.charTonum["+"]
            initial[y][x] = self.charTonum[" "]
            return True
        elif current_box == '+' and future_box == ' ':
            initial[y+b][x+a] = self.charTonum["@"]
            initial[y][x] = self.charTonum["."]
            return True
        elif current_box == '+' and future_box == '.':
            initial[y+b][x+a] = self.charTonum["*"]
            initial[y][x] = self.charTonum["."]
            return True
            
    def domove(self,move):
        currentX, currentY = self.cur.pos
        player = [currentX,currentY]
        currentcharacter = self.cur.state[currentY][currentX]
        target_pos_x = currentX + move[0]
        target_pos_y = currentY + move[1]
        targetcharacter = self.cur.state[target_pos_y][target_pos_x]
        initial = copy.deepcopy(self.cur.state)
        root = self.cur

        if self.can_move(currentX,currentY,move):
            if self.move_player(currentX,currentY,move[0],move[1],initial):
                player[1] = currentY+move[1]
                player[0] = currentX+move[0]
                return (initial,self.dir[move],player,self.heuristic(initial))

        elif self.can_push(currentX,currentY,move):
            y = currentY+move[1]
            x = currentX+move[0]
            future = self.numTochar[initial[y][x]]
            futurey = y+move[1]
            futurex = x+move[0]
            future_box = self.numTochar[initial[futurey][futurex]]
            if self.numTochar[currentcharacter] == '@' and future == '$' and future_box in [' ','.']:
                self.move_box(x,y,move[0],move[1],initial)
                if self.move_player(currentX,currentY,move[0],move[1],initial):
                    player[1] = currentY+move[1]
                    player[0] = currentX+move[0]
                initial[currentY][currentX] = self.charTonum[" "]
                initial[y][x] = self.charTonum["@"]
                player[1] = y
                player[0] = x
                if (self.deadlock_prune(futurey,futurex,initial)):
                    return True
                else:
                    self.cur = root
                return (initial,self.dir[move].upper(),player,self.heuristic(initial))
                
            elif self.numTochar[currentcharacter] == '@' and future == '*' and future_box in [' ','.']:
                self.move_box(x,y,move[0],move[1],initial)
                initial[currentY][currentX] = self.charTonum[" "]
                initial[y][x] = self.charTonum["+"]
                player[1] = y
                player[0] = x
                if (self.deadlock_prune(futurey,futurex,initial)):
                    return True
                else:
                    return (initial,self.dir[move].upper(),player,self.heuristic(initial))

            if self.numTochar[currentcharacter] == '+' and future == '$' and future_box in [' ','.']:
                self.move_box(x,y,move[0],move[1],initial)
                initial[currentY][currentX] = self.charTonum["."]
                initial[y][x] = self.charTonum["@"]
                player[1] = y
                player[0] = x
                if (self.deadlock_prune(futurey,futurex,initial)):
                    return True
                else:
                    return (initial,self.dir[move].upper(),player,self.heuristic(initial))

            elif self.numTochar[currentcharacter] == '+' and future == '*' and future_box in [' ','.']:
                self.move_box(x,y,move[0],move[1],initial)
                initial[currentY][currentX] = self.charTonum["."]
                initial[y][x] = self.charTonum["+"]
                player[1] = y
                player[0] = x
                if (self.deadlock_prune(futurey,futurex,initial)):
                    return True
                else:
                    return (initial,self.dir[move].upper(),player,self.heuristic(initial))

        return True

    def children(self):
        chi = self.get_moves()
        children = []
        for x in chi:
            check = self.domove(x)
            if check!=True:
                if self.isGoalNode(check[0]):
                    self.cur = nodes(self.cur,check[0],check[2],check[1])
                    return 0
                if(self.cur.parent!=None):
                    if (check[0]!=self.cur.parent.state):
                        children.append(nodes(self.cur,check[0],check[2],check[3],check[1]))
                else:
                    children.append(nodes(self.cur,check[0],check[2],check[3],check[1]))
        return children

    def Astar(self):
        c = 0
        t = 0
        visited  = {}
        v = set()
        notVisited = FibonacciHeap()
        notVisited.insert_node(self.cur.he,self.cur)
        while notVisited.count!=0 and self.cur.he!=0:
            c+=1
            if c==5000:
                print(printpu(self.cur.state))
                print(len(visited))
                c=0
            self.cur = notVisited.extract_min()
            visited[self.cur.box]=self.cur.he+self.cur.depth
            childnodes = self.children()
            if childnodes!=0:
                for i in childnodes:
                    feChild = i.he+i.depth
                    if i.box in visited:
                        if visited[i.box]>feChild:
                            del visited[i.box]
                            notVisited.insert_node(feChild,i)
                    else:
                        notVisited.insert_node(feChild,i)
            else:
                break
        print(self.cur.mov)
        print(c)
        print(printpu(self.cur.state))



f = open("C:\\Users\\Sarvesh\\OneDrive\\Desktop\\Sokoban\\data\\test.txt", "r")
text = f.read()
y = Board(text)
print(y.printpuz())
y.Astar()