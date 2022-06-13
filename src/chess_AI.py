import init_
import copy
import numpy as np

def judgepoint(evalst,act):
    """启发式评估:判断单个位置的分数

    """
    SCORE_FIVE, SCORE_FOUR, SCORE_SFOUR= 10000, 2000, 1000
    SCORE_THREE_COUNT_B,SCORE_THREE_COUNT_W = 0,0
    SCORE_SFOUR_COUNT_B,SCORE_SFOUR_COUNT_W = 0,0
    lfive_count,lfour_count = 0,0

    for elem in evalst:
        lfive_count += elem.count("11111")+elem.count("00000") 
        lfour_count += elem.count("Y1111Y")+elem.count("Y0000Y")
        SCORE_SFOUR_COUNT_B += elem.count("Y11110")+elem.count("1Y111")+elem.count("111Y1")+elem.count("01111Y")
        SCORE_SFOUR_COUNT_W += elem.count("Y00001")+elem.count("0Y000")+elem.count("000Y0")+elem.count("10000Y")
        SCORE_THREE_COUNT_B += elem[1:8].count("Y111Y") + elem.count("Y1Y11Y")+elem.count("Y11Y1Y")
        SCORE_THREE_COUNT_W += elem[1:8].count("Y000Y") + elem.count("Y0Y00Y")+elem.count("Y00Y0Y")

        if lfive_count > 0 : # 如果有活5
            return SCORE_FIVE
        elif lfour_count> 0 : # 如果有活四
            return SCORE_FOUR

    if (SCORE_THREE_COUNT_B > 0 and SCORE_SFOUR_COUNT_B>0) or (SCORE_THREE_COUNT_W > 0 and SCORE_SFOUR_COUNT_W>0):
        return SCORE_FOUR
    elif SCORE_THREE_COUNT_B > 1 or SCORE_THREE_COUNT_W > 1:
        return 1500
    elif SCORE_SFOUR_COUNT_B > 0 or SCORE_SFOUR_COUNT_W > 0:
        return SCORE_SFOUR
    elif SCORE_THREE_COUNT_B > 0  or SCORE_THREE_COUNT_W> 0:
        return 100

    else:
        neighbourhood = evalst[act[0]-1:act[0]+2][act[1]-1:act[1]+2]
        return max(neighbourhood.count(1),neighbourhood.count(0))

def evalpoint(act,chesslist,chesscolor):
    '''启发式评估函数'''
    directions = [[1,0],[1,1],[0,1],[-1,1]]
    i, j = act[0], act[1]
    chesslist[i][j] = chesscolor
    evalst = []
    for direction in directions:
        try:
            elem = ""
            for k in range(max(4-i,-4),min(5,19-j)):
                pos = np.array([i, j]) + np.array(direction) * k
                elem += str(chesslist[pos[0]][pos[1]])
            evalst.append(elem)
        except:  # 越界
            continue
    chesslist[i][j] = 'Y'
    return judgepoint(evalst,act)

def trim_actions(chesslist,actions,computer_color):
    """初步修剪,挑选出15个最优的选点,可能牺牲一定的准确度
    """

    AI_LIMITED_MOVE_NUM = 15
    score_dict = {}

    for act in actions:
        computerscore = evalpoint(act,chesslist,computer_color) # 不一定真的是computer
        humanscore = evalpoint(act,chesslist,int(not computer_color))

        score_dict[act] = max(computerscore,humanscore) # 存储分数

    trimmed_actions = sorted(score_dict.items(), key=lambda x: x[1], reverse=True)
    if len(trimmed_actions) > AI_LIMITED_MOVE_NUM:
        trimmed_actions = trimmed_actions[:AI_LIMITED_MOVE_NUM]
    rt_list = [act[0] for act in trimmed_actions]
    return rt_list

def alphabeta(board,depth,alpha,beta,color:int,computercolor:int): # 人工智能走子
    """Alpha-Beta Pruning
    """

    if depth == 0:
        A = evalBoard(board,computercolor)
        return A.get_score()

    if color == computercolor: # 当前是电脑方

        maxEval=init_.ninf
        trimmedactions = trim_actions(board,actions(board),computercolor)

        for action in trimmedactions:

            tmpboard = copy.deepcopy(board)
            tmpboard[action[0]][action[1]] = color

            # 特殊情况，赢了
            if win(tmpboard,action[0],action[1]):
                if depth == 3:
                    return action
                else:
                    return 10000

            evaluate = alphabeta(tmpboard,depth-1,alpha,beta,int(not color),computercolor) # 将position的child赋给eval。传参时，处理的子树会获知[已处理子树的根节点的取值信息]。
            tmp = maxEval
            maxEval = max(evaluate,maxEval) 
            if maxEval > tmp and depth == 3: # 如果当前节点的值比最大值大，则更新最优选择
                bestAct = action
            alpha = max(alpha,evaluate) # 一棵子树清理完毕，就更新一次alpha。
            if beta <= alpha: # 如果在某个节点处，对方的最小值小于我方最大，那么对面肯定不会选这一支（因为传的alphabeta值>=alpha）,剪掉这一action.
                break
        if depth == 3: # 如果是最大深度，则返回最优选择
            print ('Maximum score for the computer is %d' % maxEval)
            return bestAct
        else: # 否则继续搜索
            return maxEval

    else:

        minEval=init_.pinf
        trimmedactions = trim_actions(board,actions(board),computercolor)

        for action in trimmedactions:

            tmpboard = copy.deepcopy(board)
            tmpboard[action[0]][action[1]] = color

            if win(tmpboard,action[0],action[1]):
                return -10000

            evaluate = alphabeta(tmpboard,depth-1,alpha,beta,int(not color),computercolor)
            minEval = min(evaluate,minEval)
            beta = min(beta,evaluate)
            if beta <= alpha:
                break
        return minEval

def actions(board):
    """返回当前board的所有可能的子树.将棋盘中所有距离已有棋子2格之内的点加入actions中.

    """
    actions = set()
    for i in range(4,19): 
        for j in range(4,19):
            if board[i][j] == 0 or board[i][j] == 1:
                for k in range(max(4,i-1),min(i+2,19)):
                    for l in range(max(4,j-1),min(j+2,19)):
                        if board[k][l] == 'Y':
                            actions.add((k,l))
    return actions

class evalBoard():
    """评估棋盘的分数

    """
    def __init__(self,chesslist:list,color:int):
        self.chesslist = chesslist
        self.x = str(color) # 电脑执黑为1
        self.y = str(int(not color))
        self.score = 0
        self.potential = 0
        self.bcf = [0] # list是可变的，此处利用作为传值
        self.wcf = [0]
        self.bif = [0]
        self.wif = [0]
        self.blf = [0]
        self.wlf = [0]
        self.wdf = [0]
        self.blt = [0]
        self.wlt = [0]
        self.bst = [0]
        self.wst = [0]

        self.tuple_dict = {

            "111113": self.bcf,
            "000003": self.wcf,

            "Y1111Y": self.blf,     # 黑棋活四

            "Y0000Y": self.wlf,     # 白棋活四

            "111Y10": self.bif,
            "11Y110": self.bif,
            "Y11110": self.bif,    # 黑棋冲四
 
            "000Y01": self.wif,
            "00Y001": self.wif,
            "Y00001": self.wif,     # 白棋冲四

            "100001": self.wdf,    # 白棋死四
            "N00001": self.wdf,

            "Y111Y3": self.blt,
            "y11Y1Y": self.blt,     # 黑棋活三

            "Y000Y3": self.wlt ,
            "Y00Y0Y": self.wlt , # 白棋活三

            "Y11103": self.bst,    # 黑棋眠三

            "Y00013": self.wst    # 白棋眠三
        }
            
 
    def match_tuple(self,Tup:str):
        '''匹配tuple_dict中的tuple,并返回分数.'''

        Tup = Tup.replace(self.x,"3")
        Tup = Tup.replace(self.y,"0")
        Tup = Tup.replace("3","1")

        if Tup in self.tuple_dict:
            self.tuple_dict[Tup][0] += 0.5
        else:
            Tup = Tup[:5]+"3" # 错误写法：Tup[6] = 3 'str' object does not support item assignment
            if Tup in self.tuple_dict:
                self.tuple_dict[Tup][0] += 0.5



    def get_score(self):
        """
        按照习惯，将作为优化主体的“电脑”称为“黑棋”
        黑棋两个冲四可以当成一个活四
        白棋有活四，评分为 -9050
        白棋有冲四，评分为 -9040
        黑棋有活四，评分为 9030
        黑棋有冲四和活三，评分为 9020
        黑棋没有冲四，且白棋有活三，评分为 -9010
        黑棋有2个活三, 且白棋没有活三,评分为 9000
        下面针对黑棋或白棋的活三，眠三，活二，眠二的个数依次增加分数，评分为（黑棋得分 - 白棋得分）
        """
        # 分别计算横、竖、左下、右下四个方向的六元组
        directions = [[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1]]
        for i in range(4,19):
            for j in range(4,19):
                for direction in directions:
                    try:
                        elem = ""
                        for k in range(6):
                            pos = np.array([i,j])+np.array(direction)*k
                            elem += str(self.chesslist[pos[0]][pos[1]]) 
                        self.match_tuple(elem)
                    except: # 越界
                        continue
        if self.wcf[0] > 0:
            return -10000
        elif self.bcf[0] > 0:
            return 10000
        elif self.wlf[0] > 0: # 白棋活4，输
            return -9050
        elif self.wif[0] > 0: # 白棋冲四，输
            return -9040
        elif self.bif[0] > 1 or self.blf[0] > 0: # 黑棋冲四多于1个或黑棋活四
            return 9030
        elif self.bif[0] > 0 and self.blt[0] > 0: # 黑棋冲四和活三，赢
            return 9020
        elif self.wlt[0] > 0: # 白棋活三，输
            return -9010
        elif self.blt[0] > 1: # 黑棋双活三，白棋无活三，赢
            return 9000
        # elif self.wdf[0] > 0: # 最初防止遇三不堵，白棋死四，惩罚
        #     return -100*(self.wdf[0])
        else:
            return max(-99,(self.blt[0]-self.wlt[0])*5+(self.bst[0]-self.wst[0]))

def win(lst,x,y):
    """判断是否胜利，只要判断(i,j)附近是否有五子连珠即可

    """
    # 横，纵，两个对角五子连珠
    chesscolor = lst[x][y]
    for i in range(max(4,x-4),min(15,x+1)):
        if  lst[i][y] == lst[i+1][y] == lst[i+2][y] == lst[i+3][y] == lst[i+4][y] == chesscolor:
            return True
    for j in range(max(4,y-4),min(15,y+1)):
        if lst[x][j] == lst[x][j+1] == lst[x][j+2] == lst[x][j+3] == lst[x][j+4] == chesscolor :
            return True
    for i in range(5):
        if lst[x+i][y+i] == lst[x+i-1][y+i-1] == lst[x+i-2][y+i-2] == lst[x+i-3][y+i-3] == lst[x+i-4][y+i-4] == chesscolor:
            return True
    for j in range(5):
        if lst[x+j][y-j] == lst[x+j-1][y-j+1] == lst[x+j-2][y-j+2] == lst[x+j-3][y-j+3] == lst[x+j-4][y-j+4] == chesscolor :
            return True
    return False