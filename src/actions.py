import display
import init_
import main
import win32ui
import copy
import sys
import pygame
import chess_AI
import time
from pygame.locals import *
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
                            display.print_message(screen,"Save Failed!")
                        else:
                            display.draw_chessboard_with_chessman(chesslist, screen)
                            display.print_message(screen,"Save Successful!")
                            pygame.time.wait(1000)
                            main()
                    choose_button(x, y)


def choose_turn(screen):
    """
    绘制方框突出显示最近的落子；选择人机先手还是玩家先手, 1为电脑,0为玩家
    """
    pygame.draw.rect(screen, init_.button, [640, 130, 100, 30], 3)
    pygame.draw.rect(screen, init_.button, [640, 170, 100, 30], 3)
    s_font = pygame.font.Font(init_.resource_path('fonts\\font1.ttf'), 25)
    text1 = s_font.render("电脑先手", True, init_.button)
    text2 = s_font.render("玩家先手", True, init_.button)
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
        init_.button_sound.play(0)
        # 重新开始
        main()

    # 点击‘退出游戏’,退出游戏
    elif 650 < x < 790 and 560 < y < 610:
        # 播放音效
        init_.button_sound.play(0)
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
        display.print_message(screen,"Save Failed!")
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
        display.print_message(screen,"Open Failed!")
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

        pygame.draw.rect(screen, init_.button, [640, 340, 140, 50], 5)
        s_font = pygame.font.Font(init_.resource_path('fonts\\font1.ttf'), 30)
        text = s_font.render("ALEX推荐", True, init_.button) # 命名参考Amazon公司的语音助手Alexa,并且Alex是常见的男性名（MC的女性角色名），富有亲和力。
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
                        display.draw_chessboard_with_chessman(Chessmap[k], screen)
                        init_.play_chess_sound.play(0)
                        temp_color = 1-temp_color
                        
                   
                if (key == pygame.K_RIGHT) and k < k_max:
                        flag = 1
                        k += 1
                        display.draw_chessboard_with_chessman(Chessmap[k], screen)
                        init_.play_chess_sound.play(0)
                        temp_color = 1-temp_color
                        if k == k_max:
                           init_.victor_sound.play(0)
                        

            if event.type == MOUSEBUTTONDOWN :
                choose_button(event.pos[0], event.pos[1])
                if event.button == 1: # 如果点击鼠标左键
                    x, y = event.pos[0], event.pos[1] # 获取鼠标点击位置

                    if 640 < x < 700 and 290 < y < 320 and k > 0:
                        flag = 1
                        k -= 1
                        display.draw_chessboard_with_chessman(Chessmap[k], screen)
                        temp_color = 1-temp_color
                        init_.play_chess_sound.play(0)

                    if 720 < x < 780 and 290 < y < 320 and k < k_max:
                        flag = 1
                        k += 1
                        display.draw_chessboard_with_chessman(Chessmap[k], screen)
                        temp_color = 1-temp_color
                        init_.play_chess_sound.play(0)

                    if 650 < x < 790 and 350 < y < 380:   # AI落子
                        display.print_message (screen,"Alex思考中...")
                        pygame.display.update()
                        if(flag):
                            ktmpcolor = temp_color
                            flag = 0
                        time1 = time.time()
                        a = chess_AI.alphabeta(Chessmap[k],3,init_.ninf,init_.pinf,ktmpcolor,ktmpcolor)
                        time2 = time.time()
                        print('Thought Process Lasted %.0f ms' % (1000*(time2-time1)))
                        init_.play_chess_sound.play(0)
                        Chessmap[k][a[0]][a[1]] = ktmpcolor
                        display.draw_chessman(a[0], a[1], screen, ktmpcolor)
                        ktmpcolor = 1 - ktmpcolor
                        display.draw_chessboard_with_chessman(Chessmap[k], screen)
                        pygame.draw.rect(screen, init_.button, [(a[0] - 4) * 40 + 15, (a[1]- 4) * 40 + 15, 30, 30], 3)

                    else: #人类落子
                        for i in range(4, 19):
                            for j in range(4, 19):
                                if ((i-4) * 40 + 15) < x < ((i-4) * 40 + 55) and ((j-4) * 40 + 15) < y < ((j-4) * 40 + 55) and chessmap[k][i][j] == 'Y': 
                                    if(flag):
                                        ktmpcolor = temp_color
                                        flag = 0
                                    display.draw_chessman(i, j, screen, ktmpcolor)
                                    pygame.display.update()
                                    pygame.draw.rect(screen, init_.button, [(i - 4) * 40 + 15, (j- 4) * 40 + 15, 30, 30], 3)
                                    Chessmap[k][i][j] = ktmpcolor
                                    ktmpcolor = 1 - ktmpcolor
                                    init_.play_chess_sound.play(0)
                                    break
                            else:
                                continue
                            break

        pygame.display.update()