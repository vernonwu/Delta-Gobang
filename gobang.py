from asyncio.windows_events import NULL
import pygame
from pygame.locals import *
import sys
import win32ui
import copy
import numpy as np
import os
import random as rd

# define absolute path
# def resource_path(relative): 
#     if hasattr(sys, "_MEIPASS"): 
#         absolute_path = os.path.join(sys._MEIPASS, relative)
#     else: absolute_path = os.path.join(relative)
#     return absolute_path

pygame.init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
background = (201, 202, 187)
checkerboard = (80, 80, 80)
button = (52, 53, 44)
black_chessman = pygame.image.load('wuziqi/Black_chess.png')
white_chessman = pygame.image.load('wuziqi/White_chess.png')
# 音乐
play_chess_sound = pygame.mixer.Sound("music/play_chess.wav")
play_chess_sound.set_volume(0.2)
button_sound = pygame.mixer.Sound("music/button.wav")
button_sound.set_volume(0.2)
victor_sound = pygame.mixer.Sound("music/victory.wav")
victor_sound.set_volume(0.2)
pygame.display.set_caption('五子不行V2')

# 定义极限
pinf = float('inf')
ninf = float('-inf')


def draw_chessboard(screen):
    """绘制棋盘
    大小为15*15和一些功能按钮。
    """
    global background, checkerboard, button
    # 画棋盘
    for i in range(15):
        pygame.draw.line(screen, BLACK, (40 * i + 30, 30), (40 * i + 30, 590))
        pygame.draw.line(screen, BLACK, (30, 40 * i + 30), (590, 40 * i + 30))
    # 画边界
    pygame.draw.line(screen, BLACK, (2, 2), (2, 622), 4)
    pygame.draw.line(screen, BLACK, (622, 2), (622, 622), 4)
    pygame.draw.line(screen, BLACK, (2, 2), (622, 2), 4)
    pygame.draw.line(screen, BLACK, (2, 622), (622, 622), 4)
    # 画棋盘的定位点
    pygame.draw.circle(screen, checkerboard, (150, 150), 6)
    pygame.draw.circle(screen, checkerboard, (470, 150), 6)
    pygame.draw.circle(screen, checkerboard, (150, 470), 6)
    pygame.draw.circle(screen, checkerboard, (470, 470), 6)
    pygame.draw.circle(screen, checkerboard, (310, 310), 6)
    # 矩形参数由四个值构成的元组,分别是矩形左上角的x、y坐标,矩形的宽和高
    pygame.draw.rect(screen, button, [640, 10, 140, 50], 5)
    pygame.draw.rect(screen, button, [640, 70, 140, 50], 5)
    pygame.draw.rect(screen, button, [640, 440, 80, 50], 5)
    pygame.draw.rect(screen, button, [640, 500, 140, 50], 5)
    pygame.draw.rect(screen, button, [640, 560, 140, 50], 5)
    pygame.draw.rect(screen, button, [640, 230, 140, 50], 5)
    pygame.draw.rect(screen, button, [640, 295, 60, 30], 3)
    pygame.draw.rect(screen, button, [720, 295, 60, 30], 3)

    s_font = pygame.font.Font('font1.ttf', 30)
    d_font = pygame.font.Font('font1.ttf', 20)
    text1 = s_font.render("人人对战", True, button)
    text2 = s_font.render("人机对战", True, button)
    text3 = s_font.render("悔棋", True, button)
    text4 = s_font.render("重新开始", True, button)
    text5 = s_font.render("退出游戏", True, button)
    text6 = s_font.render("载入棋谱", True, button)
    text7 = d_font.render("前一步", True, button)
    text8 = d_font.render("后一步", True, button)
    screen.blit(text1, (650, 20))
    screen.blit(text2, (650, 80))
    screen.blit(text3, (650, 450))
    screen.blit(text4, (650, 510))
    screen.blit(text5, (650, 570))
    screen.blit(text6, (650, 240))
    screen.blit(text7, (640, 300))
    screen.blit(text8, (720, 300))


def draw_chessman(x, y, screen, color):
    """画棋子,当color = 0画黑子,color = 1时画白子

    """
    if color == 0:
        screen.blit(black_chessman, ((x - 4) * 40 + 15, (y - 4) * 40 + 15))
    elif color == 1:
        screen.blit(white_chessman, ((x - 4) * 40 + 15, (y - 4) * 40 + 15))


def draw_chessboard_with_chessman(chesslist, screen):
    screen.fill(background)
    screen.blit(background_jpg, (0, 0))
    draw_chessboard(screen)
    for i in range(4, 19):
        for j in range(4, 19):
                draw_chessman(i, j, screen, chesslist[i][j])


def choose_save(screen, chesslist, chessindex, index):
    pygame.draw.rect(screen, button, [640, 340, 140, 50], 5)
    s_font = pygame.font.Font('font1.ttf', 30)
    text = s_font.render("保存棋谱", True, button)
    screen.blit(text, (650, 350))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos[0], event.pos[1]
                    if 650 < x < 790 and 350 < y < 380:
                        try:
                            save_chess(chesslist, chessindex, index)
                        except:
                            print("Save Failed!")
                        else:
                            print("Save Succeeded!")
                    choose_button(x, y)


def choose_turn(screen):
    """
    选择人机先手还是玩家先手, 1为电脑,0为玩家
    :return:
    """
    pygame.draw.rect(screen, button, [640, 130, 100, 30], 3)
    pygame.draw.rect(screen, button, [640, 170, 100, 30], 3)
    s_font = pygame.font.Font('font1.ttf', 25)
    text1 = s_font.render("电脑先手", True, button)
    text2 = s_font.render("玩家先手", True, button)
    screen.blit(text1, (640, 130))
    screen.blit(text2, (640, 170))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos[0], event.pos[1]
                    if 640 < x < 740 and 130 < y < 160: # 电脑先手
                        return 1
                    elif 640 < x < 740 and 170 < y < 200: # 玩家先手
                        return 0
                    choose_button(x, y)


def choose_mode():
    """选择人人对战还是人机对战还是载入棋谱

    """
    mode = 1
    load = False
    while True:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos[0], event.pos[1]
                    # 如果点击人人对战
                    if 650 < x < 790 and 10 < y < 60:
                        mode = 1
                        return mode, load
                    elif 650 < x < 790 and 70 < y < 120:
                        mode = 0
                        return mode, load
                    elif 640 < x < 780 and 230 < y < 280:
                        load = True
                        return mode, load
                    choose_button(x, y)


def choose_button(x, y):
    """功能键:退出游戏和重新开始
    """
    # 如果点击‘重新开始’
    if 650 < x < 790 and 500 < y < 550:
        # # 取消阻止
        # running = True
        # 播放音效
        button_sound.play(0)
        # 重新开始
        main()

    # 点击‘退出游戏’,退出游戏
    elif 650 < x < 790 and 560 < y < 610:
        # 播放音效
        button_sound.play(0)
        pygame.quit()
        sys.exit()

def save_chess(chesslist, chessindex, index):
    dlg = win32ui.CreateFileDialog(0)
    dlg.SetOFNInitialDir(r"C:\Users\lenovo\Desktop")
    flag = dlg.DoModal()
    filename = dlg.GetPathName()
    if flag == 1:
        print("Save as", filename)
    else:
        print("Save Failed!")
    for i in range(23):
        for j in range(23):
            chesslist[i][j] = str(chesslist[i][j])
            chessindex[i][j] = str(chessindex[i][j])
    str1 = ''
    str2 = ''
    for i in range(23):
        if i == 0:
            str1 = ','.join(chesslist[i])
        str1 = str1 + '\n' + ','.join(chesslist[i])
        str2 = str2 + '\n' + ','.join(chessindex[i])
    f = open(filename, 'w+')
    f.write(str1)
    f.write(str2)
    f.write('\n' + str(index))
    f.close()


def load_chess():
    dlg = win32ui.CreateFileDialog(1)  # 1表示打开文件对话框
    dlg.SetOFNInitialDir(r"C:\Users\lenovo\Desktop")  # 设置打开文件对话框中的初始显示目录
    flag = dlg.DoModal() # 打开文件对话框
    filename = dlg.GetPathName()  # 获取选择的文件名称
    if flag == 1:
        print("Open", filename)
    else:
        print("Open Failed!")
    lst_tmp = []
    f = open(filename, 'r')
    # 读取文件内容
    for line in f.readlines():
        line = line.strip('\n')
        xt = [i for i in line.split(',')]
        lst_tmp.append(xt)
    c_list = lst_tmp[0: 23] # 第0行到第23行，棋盘
    c_index = lst_tmp[23: 46] # 棋子
    index_max = lst_tmp[47][0]
    f.close()
    chessmap = [[['N' for _ in range(23)] for _ in range(23)] for _ in range(int(index_max))]
    for i in range(4, 19):
        for j in range(4, 19):
            if c_list[i][j] != 'Y' and c_list[i][j] != 'N': 
                c_list[i][j] = int(c_list[i][j])
            if c_index[i][j] != 'Y' and c_index[i][j] != 'N':
                c_index[i][j] = int(c_index[i][j])
    num = int(index_max)
    while num > 0:
        for i in range(4, 19):
            for j in range(4, 19):
                if c_index[i][j] == num: # 如果该位置有棋子
                    c_list[i][j] = 'Y'
        for k in range(4, 19):
            for l in range(4, 19):
                chessmap[num - 1][k][l] = c_list[k][l]
        num = num - 1
    return chessmap


def play_chess(screen, chessmap): 
    '''
    播放棋谱
    '''
    k = -1
    k_max = len(chessmap) - 1
    while True:
        for event in pygame.event.get():

            if event.type == KEYDOWN:
                key = event.key
                if key == K_ESCAPE:
                    return
                if (key == pygame.K_LEFT) and k > 0:
                        k -= 1
                        draw_chessboard_with_chessman(chessmap[k], screen)
                        play_chess_sound.play(0)
                        
                   
                if (key == pygame.K_RIGHT) and k < k_max:
                        k += 1
                        draw_chessboard_with_chessman(chessmap[k], screen)
                        play_chess_sound.play(0)
                        pygame.time.delay(200)
                        

            if event.type == MOUSEBUTTONDOWN :
                if event.button == 1: # 如果点击鼠标左键
                    x, y = event.pos[0], event.pos[1] # 获取鼠标点击位置
                    if 640 < x < 700 and 290 < y < 320 and k > 0:
                        k -= 1
                        draw_chessboard_with_chessman(chessmap[k], screen)
                        play_chess_sound.play(0)
                    if 720 < x < 780 and 290 < y < 320 and k < k_max:
                        k += 1
                        draw_chessboard_with_chessman(chessmap[k], screen)
                        play_chess_sound.play(0)
                        choose_button(x, y) 

        pygame.display.update()

def pop_window(screen, color):
    """弹出胜利的界面

    """
    if not color:
        pygame.draw.rect(screen, RED, [110, 230, 400, 160], 5)
        s_font = pygame.font.Font('font1.ttf', 80)
        text1 = s_font.render("黑棋胜利!", True, RED)
        screen.blit(text1, (120, 270))
    elif color:
        pygame.draw.rect(screen, RED, [110, 230, 400, 160], 5)
        s_font = pygame.font.Font('font1.ttf', 80)
        text1 = s_font.render("白棋胜利!", True, RED)
        screen.blit(text1, (120, 270))


def tip(screen, chesslist, color, choose, wincolor, i1, j1, i2, j2, chessindex, index):
    """显示一些提示

    当前是什么模式,轮到谁落子,谁赢了
    """
    s_font = pygame.font.Font('font.ttf', 40)
    text1 = s_font.render("黑棋落子", True, button)
    text2 = s_font.render("白棋落子", True, button)
    s_font1 = pygame.font.Font('font1.ttf', 30)
    text3 = s_font1.render("人人对战", True, button, (100, 100, 100))
    text4 = s_font1.render("人机对战", True, button, (100, 100, 100))
    draw_chessboard_with_chessman(chesslist, screen)
    if not color: # 黑棋落子
        screen.blit(text1, (630, 140))
    else: # 白棋落子
        screen.blit(text2, (630, 140))
    if choose: # 如果是人机对战
        screen.blit(text3, (650, 20))
        pygame.draw.rect(screen, button, [(i1 - 4) * 40 + 15, (j1 - 4) * 40 + 15, 30, 30], 3)
    else:
        screen.blit(text4, (650, 80))
        pygame.draw.rect(screen, button, [(i1 - 4) * 40 + 15, (j1 - 4) * 40 + 15, 30, 30], 3)
        pygame.draw.rect(screen, button, [(i2 - 4) * 40 + 15, (j2 - 4) * 40 + 15, 30, 30], 3)

def alphabeta(board,depth,alpha,beta,color:int,computercolor:int): # 人工智能走子

    if depth == 0:
        A = evalBoard(board,computercolor)
        return A.get_score()

    if color == computercolor: # 当前是电脑方
        maxEval=ninf
        for action in actions(board):

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
            print ('Maximum score is %d' % maxEval)
            return bestAct
        else: # 否则继续搜索
            return maxEval
    else:
        minEval=pinf
        for action in actions(board):

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
            "111113": self.bcf,       # 黑棋连5

            "000003": self.wcf,       # 白棋连5
                                      # 黑棋连4
            "111Y10": self.bif,
            "11Y110": self.bif,
            "Y11110": self.bif,    # 黑棋冲四
 
            "000Y01": self.wif,
            "00Y001": self.wif,
            "Y00001": self.wif,     # 白棋冲四

            "Y1111Y": self.blf, # 黑棋活四

            "Y0000Y": self.wlf, # 白棋活四

            "100001": self.wdf, # 白棋死四
            "N00001": self.wdf,

            "Y111Y3": self.blt, # 黑棋活三

            "Y000Y3": self.wlt , # 白棋活三

            "Y11103": self.bst, # 黑棋眠三

            "Y00013": self.wst # 白棋眠三
        }
            
 
    def match_tuple(self,Tup:str):
        if Tup in self.tuple_dict:
            self.tuple_dict[Tup][0] += 1
        else:
            Tup[5] = 3
            if Tup in self.tuple_dict:
                self.tuple_dict[Tup][0] += 1

    def get_score(self):
        """
        黑棋连5,评分为10000
        白棋连5,评分为 -10000
        黑棋两个冲四可以当成一个活四
        白棋有活四，评分为 -9050
        白棋有冲四，评分为 -9040
        黑棋有活四，评分为 9030
        黑棋有冲四和活三，评分为 9020
        黑棋没有冲四，且白棋有活三，评分为 -9010
        黑棋有2个活三, 且白棋没有活三,评分为 9000
        下面针对黑棋或白棋的活三，眠三，活二，眠二的个数依次增加分数，评分为（黑棋得分 - 白棋得分）
        """
        # 分别计算横、竖、左下、右下四个方向的五元组
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

        if self.bcf[0] > 0: # 黑棋连5，赢
            self.score = 10000
        elif self.wcf[0] > 0 or self.wlf[0] > 0: # 白棋连5，输
            self.score = -10000
        elif self.wlf[0] > 0: # 白棋活4，输
            self.score = -9050
        elif self.wif[0] > 0: # 白棋冲四，输
            self.score = -9040
        elif self.bif[0] > 1 or self.blf[0] > 0: # 黑棋冲四多于1个或黑棋活四
            self.score = 9030
        elif self.blf[0] > 0 and self.blt[0] > 0: # 黑棋活四和活三，赢
            self.score = 9020
        elif self.wdf[0] > 0: # 白棋死四，惩罚
            self.score = -10
        elif self.wlt[0] > 0: # 白棋活三，输
            self.score = -9010
        elif self.blt[0] > 1: # 黑棋双活三，白棋无活三，赢
            self.score = 9000
        return self.score

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

def displaywin(screen,wincolor,chesslist,chessindex,index):
    '''
    显示胜利界面
    '''
    pop_window(screen, wincolor) # 弹出胜利的界面
    choose_save(screen, chesslist, chessindex, index) # 激活保存按钮

def key_control(screen, mode):
    """用于接收用户鼠标的信息

    """
    global running, i_temp1, j_temp1, i_temp2, j_temp2, order, wincolor, choose_turn_result, index, load, chessindex, \
        repent
    if order: 
        color = 0
    else:
        color = 1
    tip(screen, lst, color, mode,wincolor, i_temp1, j_temp1, i_temp2, j_temp2, chessindex, index)
    if choose_turn_result: # 如果电脑先手（初始值由choose_turn得出）
        lst[11][11] = int(color)
        draw_chessman(8, 8, screen, color) # 画最中间
        order = not order
        choose_turn_result = not choose_turn_result # order与choose_turn_result取反
        chessindex[11][11] = index # 将最中间的棋子索引记录为0
        index += 1

    # 人类玩家开始落子
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1: # 按左键
                x, y = event.pos[0], event.pos[1]
                for i in range(4, 19):
                    for j in range(4, 19):
                        # 如果点击的位置无棋子，游戏运行中，且当前落子方为人类玩家
                        if ((i-4) * 40 + 15) < x < ((i-4) * 40 + 55) and ((j-4) * 40 + 15) < y < ((j-4) * 40 + 55) and lst[i][j] == 'Y' and running and not choose_turn_result: 
                            repent = True # 悔棋为真
                            draw_chessman(i, j, screen, color)
                            play_chess_sound.play(0)
                            # (i_temp1,j_temp1)为本次落子的位置
                            i_temp1 = i
                            j_temp1 = j
                            lst[i][j] = int (color) # 更新棋盘
                            wincolor = int(color) # 更新可能的胜利方
                            chessindex[i][j] = index
                            index += 1
                            if win(lst,i,j):
                                victor_sound.play(0)
                                displaywin(screen,wincolor,lst,chessindex,index)
                            # 将电脑方操作放在了这里，是为了防止误触。即当人类方落子无效时，电脑方便不会行动。
                            if not mode and running:
                                print ("Calculating next move...")
                                a = alphabeta(lst,3,ninf,pinf,int(not color),int(not color))
                                repent = True
                                draw_chessman(a[0], a[1], screen,not color)
                                play_chess_sound.play(0)
                                lst[a[0]][a[1]] = int(not color)
                                i_temp2 = a[0]
                                j_temp2 = a[1]
                                wincolor = int(not color)
                                chessindex[a[0]][a[1]] = index
                                index += 1
                                if win(lst,a[0],a[1]):
                                    victor_sound.play(0)
                                    displaywin(screen,wincolor,lst,chessindex,index)
                            if mode and running: 
                                order = not order
                            break
                    else:
                        continue
                    break

                # 如果点击悔棋
                if 650 < x < 730 and 440 < y < 490 and running and repent:
                    if not mode: # 如果是人人对战
                        lst[i_temp1][j_temp1] = 'Y'
                        lst[i_temp2][j_temp2] = 'Y'
                    elif mode:
                        lst[i_temp1][j_temp1] = 'Y'
                        order = not order
                    draw_chessboard_with_chessman(lst, screen)
                choose_button(x, y)
        # 点X也退出游戏
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()


def main():
    # 定义全局变量
    global background, checkerboard, button, order, lst, score, running, background_jpg, wincolor, i_temp1, j_temp1, \
        i_temp2, j_temp2, choose_turn_result, index, chessindex, load, repent, i_temp3, j_temp3
    pygame.init()
    screen = pygame.display.set_mode((800, 624))
    background_jpg = pygame.image.load('wuziqi/Background.jpg')
    screen.fill(background)
    screen.blit(background_jpg, (0, 0))
    # order = False时黑棋先手
    order = True
    # 允许落子
    running = True
    # 不许载入棋谱
    load = False
    # 可以悔棋
    repent = True
    # 赢棋的颜色未定
    wincolor = 'Y'
    chessindex = [['N' for _ in range(23)] for _ in range(23)] # 存储棋子的位置，大小为23*23
    index = 0
    i_temp1 = j_temp1 = i_temp2 = j_temp2 = i_temp3 = j_temp3 = 0 # 存储落子的位置

    lst = [['N' for _ in range(23)] for _ in range(23)]
    for i in range(4, 19):
        for j in range(4, 19):
            lst[i][j] = 'Y' # 初始化棋盘为空
    draw_chessboard(screen)
    pygame.display.update()
    # 选择电脑先手还是玩家先手
    choose_turn_result = 0
    # 选择人人还是人机
    mode, load = choose_mode()
    if not mode: # 人人对战
        choose_turn_result = choose_turn(screen) #选择先手
    if load:
        try:
            c_map = load_chess() # 读取棋谱
            print("Open Succeeded!") 
            play_chess(screen, c_map)
            main()
        except:
            print("Open Failed!")
            main()
    
    while True:
        key_control(screen, mode)
        pygame.display.update()


if __name__ == "__main__":
    main()
