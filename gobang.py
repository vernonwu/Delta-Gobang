'''
    Name:DeltaGobang
    Function:五子棋游戏主程序,支持人人/人机对战/保存棋谱/悔棋
    Author:吴霄鹤
    Last edit at: 2022-06-10
'''
from asyncio.windows_events import NULL
from re import S
import pygame
from pygame.locals import *
import sys
import win32ui
import copy
import numpy as np
from tkinter import *
import os

# define absolute path
def resource_path(relative): 
    absolute_path = os.path.join(relative)
    return absolute_path
'''
    加载图片和背景音乐
'''
pygame.init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
background = (201, 202, 187)
checkerboard = (80, 80, 80)
button = (52, 53, 44)
black_chessman = pygame.image.load(resource_path('image\\Black_chess.png'))
white_chessman = pygame.image.load(resource_path('image\\White_chess.png'))
# 音乐
play_chess_sound = pygame.mixer.Sound(resource_path("music\\play_chess.wav"))
play_chess_sound.set_volume(0.2)
button_sound = pygame.mixer.Sound(resource_path("music\\button.wav"))
button_sound.set_volume(0.2)
victor_sound = pygame.mixer.Sound(resource_path("music\\victory.wav"))
victor_sound.set_volume(1)
background_music = pygame.mixer.Sound(resource_path("music\\Bgm.wav"))
background_music.set_volume(0.3)
pygame.display.set_caption('五子不行V2')

# 定义极限
pinf = float('inf')
ninf = float('-inf')

def print_message(screen,text):
    """打印文字"""
    font = pygame.font.Font('font1.ttf', 20)
    text = font.render(text, True, button)
    screen.blit(text, (640, 190))
    pygame.display.update()

def draw_chessboard(screen):
    """绘制棋盘,大小为15*15,和一些功能按钮。
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
    text4 = s_font.render("回主菜单", True, button)
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
    """全盘绘制(包括棋盘和棋子)"""
    screen.fill(background)
    screen.blit(background_jpg, (0, 0))
    draw_chessboard(screen)
    for i in range(4, 20):
        for j in range(4, 20):
                draw_chessman(i, j, screen, chesslist[i][j])

def draw_AI_takeover(screen,flag):
    """绘制托管按钮,复用为保存按钮"""
    pygame.draw.rect(screen, button, [640, 340, 140, 50], 5)
    s_font = pygame.font.Font('font1.ttf', 30)
    if(flag):
        text = s_font.render("切换模式", True, button)
    else:
        text = s_font.render("棋谱保存", True, button)
    screen.blit(text, (650, 350))
    pygame.display.update()

def choose_save(screen,chesslist, chessindex, index):
    """保存棋谱的按钮"""
    while True:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos[0], event.pos[1]
                    if 650 < x < 790 and 350 < y < 380:
                        try:
                            save_chess(screen,chesslist, chessindex, index)
                        except:
                            print_message(screen,"Save Failed!")
                        else:
                            draw_chessboard_with_chessman(chesslist, screen)
                            print_message(screen,"Save Successful!")
                            pygame.time.wait(1000)
                            main()
                    choose_button(x, y)


def choose_turn(screen):
    """
    绘制方框突出显示最近的落子；选择人机先手还是玩家先手, 1为电脑,0为玩家
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
    """选择人人对战/人机对战/载入棋谱

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

def save_chess(screen,chesslist, chessindex, index):
    """保存棋谱"""
    dlg = win32ui.CreateFileDialog(0)
    dlg.SetOFNInitialDir(r"C:\Users\lenovo\Desktop")
    flag = dlg.DoModal()
    filename = dlg.GetPathName()
    if flag == 1:
        print("Saved as", filename)
    else:
        print_message(screen,"Save Failed!")
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


def load_chess(screen):
    """载入棋谱"""
    dlg = win32ui.CreateFileDialog(1)  # 1表示打开文件对话框
    dlg.SetOFNInitialDir(r"C:\Users\lenovo\Desktop")  # 设置打开文件对话框中的初始显示目录
    flag = dlg.DoModal() # 打开文件对话框
    filename = dlg.GetPathName()  # 获取选择的文件名称
    if flag == 1:
        print("Open", filename)
    else:
        print_message(screen,"Open Failed!")
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
    for i in range(4, 20):
        for j in range(4, 20):
            if c_list[i][j] != 'Y' and c_list[i][j] != 'N': 
                c_list[i][j] = int(c_list[i][j])
            if c_index[i][j] != 'Y' and c_index[i][j] != 'N':
                c_index[i][j] = int(c_index[i][j])
    num = int(index_max)
    while num > 0:
        for i in range(4, 20):
            for j in range(4, 20):
                if c_index[i][j] == num: # 如果该位置有棋子
                    c_list[i][j] = 'Y'
        for k in range(4, 20):
            for l in range(4, 20):
                chessmap[num - 1][k][l] = c_list[k+1][l]
        num = num - 1
    return chessmap


def play_chess(screen, chessmap): 
    '''
    播放棋谱,允许键盘控制/鼠标控制/人类和AI落子(不会污染原棋谱)
    '''
    global temp_color, ktmpcolor,flag
    k = -1
    k_max = len(chessmap) - 1
    temp_color = 0
    flag = 1
    Chessmap = copy.deepcopy(chessmap)

    while True:

        pygame.draw.rect(screen, button, [640, 340, 140, 50], 5)
        s_font = pygame.font.Font('font1.ttf', 30)
        text = s_font.render("ALEX推荐", True, button) # 命名参考Amazon公司的语音助手Alexa,并且Alex是常见的男性名（MC的女性角色名），富有亲和力。
        screen.blit(text, (650, 350))
        pygame.display.update()
        
        for event in pygame.event.get():

            if event.type == KEYDOWN:
                key = event.key
                if key == K_ESCAPE:
                    return
                if (key == pygame.K_LEFT) and k > 0:
                        flag = 1
                        k -= 1
                        draw_chessboard_with_chessman(Chessmap[k], screen)
                        play_chess_sound.play(0)
                        temp_color = 1-temp_color
                        
                   
                if (key == pygame.K_RIGHT) and k < k_max:
                        flag = 1
                        k += 1
                        draw_chessboard_with_chessman(Chessmap[k], screen)
                        play_chess_sound.play(0)
                        temp_color = 1-temp_color
                        if k == k_max:
                            victor_sound.play(0)
                        

            if event.type == MOUSEBUTTONDOWN :
                choose_button(event.pos[0], event.pos[1])
                if event.button == 1: # 如果点击鼠标左键
                    x, y = event.pos[0], event.pos[1] # 获取鼠标点击位置

                    if 640 < x < 700 and 290 < y < 320 and k > 0:
                        flag = 1
                        k -= 1
                        draw_chessboard_with_chessman(Chessmap[k], screen)
                        temp_color = 1-temp_color
                        play_chess_sound.play(0)

                    if 720 < x < 780 and 290 < y < 320 and k < k_max:
                        flag = 1
                        k += 1
                        draw_chessboard_with_chessman(Chessmap[k], screen)
                        temp_color = 1-temp_color
                        play_chess_sound.play(0)

                    if 650 < x < 790 and 350 < y < 380:   # AI落子
                        print_message (screen,"Alex思考中...")
                        pygame.display.update()
                        if(flag):
                            ktmpcolor = temp_color
                            flag = 0
                        a = alphabeta(Chessmap[k],3,ninf,pinf,ktmpcolor,ktmpcolor)
                        play_chess_sound.play(0)
                        Chessmap[k][a[0]][a[1]] = ktmpcolor
                        draw_chessman(a[0], a[1], screen, ktmpcolor)
                        ktmpcolor = 1 - ktmpcolor
                        draw_chessboard_with_chessman(Chessmap[k], screen)
                        pygame.draw.rect(screen, button, [(a[0] - 4) * 40 + 15, (a[1]- 4) * 40 + 15, 30, 30], 3)

                    else: #人类落子
                        for i in range(4, 19):
                            for j in range(4, 19):
                                if ((i-4) * 40 + 15) < x < ((i-4) * 40 + 55) and ((j-4) * 40 + 15) < y < ((j-4) * 40 + 55) and chessmap[k][i][j] == 'Y' and running: 
                                    if(flag):
                                        ktmpcolor = temp_color
                                        flag = 0
                                    draw_chessman(i, j, screen, ktmpcolor)
                                    pygame.display.update()
                                    pygame.draw.rect(screen, button, [(i - 4) * 40 + 15, (j- 4) * 40 + 15, 30, 30], 3)
                                    Chessmap[k][i][j] = ktmpcolor
                                    ktmpcolor = 1 - ktmpcolor
                                    play_chess_sound.play(0)
                                    break
                            else:
                                continue
                            break

        pygame.display.update()

def pop_window(screen, color):
    """弹出胜利的界面

    """
    if not color:
        pygame.draw.rect(screen, RED, [110, 230, 400, 160], 5)
        s_font = pygame.font.Font('font1.ttf', 80)
        text1 = s_font.render("黑棋胜利!", True, RED)
        screen.blit(text1, (120, 270))
        pygame.display.update()
    elif color:
        pygame.draw.rect(screen, RED, [110, 230, 400, 160], 5)
        s_font = pygame.font.Font('font1.ttf', 80)
        text1 = s_font.render("白棋胜利!", True, RED)
        screen.blit(text1, (120, 270))
        pygame.display.update()


def tip(screen, chesslist, color, choose, i1, j1, i2, j2):
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

def judgepoint(evalst,act):
    """启发式评估:判断单个位置的分数

    """
    SCORE_FIVE, SCORE_FOUR, SCORE_SFOUR= 10000, 2000, 1000
    SCORE_THREE_COUNT_B,SCORE_THREE_COUNT_W = 0,0
    SCORE_SFOUR_COUNT_B,SCORE_SFOUR_COUNT_W = 0,0
    lfive_count,lfour_count = 0,0

    for elem in evalst:
        lfive_count += elem.count("11111")+elem.count("00000") 
        lfour_count += elem[1:10].count("Y1111Y")+elem[1:10].count("Y0000Y")
        SCORE_SFOUR_COUNT_B += elem[1:10].count("Y11110")+elem[1:10].count("1Y111")+elem[1:10].count("111Y1")
        SCORE_SFOUR_COUNT_W += elem[1:10].count("Y00001")+elem[1:10].count("0Y000")+elem[1:10].count("000Y0")
        SCORE_THREE_COUNT_B += elem[2:9].count("Y111Y") + elem[2:9].count("Y1Y11Y")+elem[2:9].count("Y11Y1Y")
        SCORE_THREE_COUNT_W += elem[2:9].count("Y000Y") + elem[2:9].count("Y0Y00Y")+elem[2:9].count("Y00Y0Y")

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

        maxEval=ninf
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
            # print ('Maximum score for the computer is %d' % maxEval)
            return bestAct
        else: # 否则继续搜索
            return maxEval

    else:

        minEval=pinf
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
            Tup[5] = 3
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
        elif self.blf[0] > 0 and self.blt[0] > 0: # 黑棋活四和活三，赢
            return 9020
        elif self.wlt[0] > 0: # 白棋活三，输
            return -9010
        elif self.blt[0] > 1: # 黑棋双活三，白棋无活三，赢
            return 9000
        elif self.wdf[0] > 0: # 白棋死四，惩罚
            return -100*(self.wdf[0])
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

def displaywin(screen,wincolor,chesslist,chessindex,index):
    '''
    显示胜利界面
    '''
    draw_chessboard_with_chessman(chesslist,screen)
    pop_window(screen, wincolor) # 弹出胜利的界面
    draw_AI_takeover(screen,0)
    pygame.display.update()
    choose_save(screen,chesslist, chessindex, index) # 激活保存按钮

def key_control(screen, mode):
    """用于接收用户鼠标的信息

    """
    global running, i_temp1, j_temp1, i_temp2, j_temp2, order, wincolor, choose_turn_result, index, load, chessindex, \
        repent
    if order: 
        color = 0
    else:
        color = 1
    tip(screen, lst, color, mode[0], i_temp1, j_temp1, i_temp2, j_temp2)
    if choose_turn_result: # 如果电脑先手（初始值由choose_turn得出）
        lst[11][11] = int(color)
        draw_chessman(8, 8, screen, color) # 画最中间
        order = not order
        choose_turn_result = not choose_turn_result # order与choose_turn_result取反
        chessindex[11][11] = index # 将最中间的棋子索引记录为0
        index += 1
    draw_AI_takeover(screen,1)
    # 人类玩家开始落子
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1: # 按左键
                x, y = event.pos[0], event.pos[1]
                if 650 < x < 790 and 350 < y < 380:
                    mode[0] = 1 -  mode[0]
                    tip(screen, lst, color, mode[0], i_temp1, j_temp1, i_temp2, j_temp2)
                    draw_AI_takeover(screen,1)
                    print_message(screen,"切换成功！")
                    pygame.time.wait(500)
                for i in range(4, 19):
                    for j in range(4, 19):
                        # 如果点击的位置无棋子，游戏运行中，且当前落子方为人类玩家
                        if ((i-4) * 40 + 15) < x < ((i-4) * 40 + 55) and ((j-4) * 40 + 15) < y < ((j-4) * 40 + 55) and lst[i][j] == 'Y' and running and not choose_turn_result: 
                            lst[i][j] = int (color) # 更新棋盘
                            repent = True # 悔棋为真
                            draw_chessman(i, j, screen, color)
                            play_chess_sound.play(0)
                            pygame.display.update()
                            # (i_temp1,j_temp1)为本次落子的位置
                            i_temp1 = i
                            j_temp1 = j
                            wincolor = int(color) # 更新可能的胜利方
                            chessindex[i][j] = index
                            index += 1
                            if win(lst,i,j):
                                victor_sound.play(0)
                                displaywin(screen,wincolor,lst,chessindex,index)
                            # 将电脑方操作放在了这里，是为了防止误触。即当人类方落子无效时，电脑方便不会行动。
                            if not mode[0] and running:
                                print_message(screen,"Alex思考中...")
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
                            if mode[0] and running: 
                                order = not order
                            break
                    else:
                        continue
                    break

                # 如果点击悔棋
                if 650 < x < 730 and 440 < y < 490 and running and repent:
                    if not mode[0]: # 如果是人人对战
                        lst[i_temp1][j_temp1] = 'Y'
                        lst[i_temp2][j_temp2] = 'Y'
                    elif mode[0]:
                        lst[i_temp1][j_temp1] = 'Y'
                        order = not order
                    draw_chessboard_with_chessman(lst, screen)

                choose_button(x, y)

        # 点X也退出游戏
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()


def main():
    '''主函数'''
    global background, checkerboard, button, order, lst, score, running, background_jpg, wincolor, i_temp1, j_temp1, \
        i_temp2, j_temp2, choose_turn_result, index, chessindex, load, repent, i_temp3, j_temp3,mode
    pygame.init()
    screen = pygame.display.set_mode((800, 624))
    background_jpg = pygame.image.load(resource_path('image\\Background.jpg'))
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
    mode = [1]
    mode[0], load = choose_mode()
    background_music.stop()
    background_music.play(-1) # -1是循环播放

    if not mode[0]: # 人人对战
        choose_turn_result = choose_turn(screen) #选择先手
    if load:
        try:
            c_map = load_chess(screen) # 读取棋谱
            print_message(screen,"Open Successful!") 
            play_chess(screen, c_map)
            main()
        except:
            print_message(screen,"Open Failed!")
            pygame.time.wait(1000)
            main()
    
    while True:
        key_control(screen, mode)
        pygame.display.update()


if __name__ == "__main__":
    main()
