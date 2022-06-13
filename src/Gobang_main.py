'''
    Name:DeltaGobang
    Function:五子棋游戏主程序,支持人人/人机对战/保存棋谱/悔棋
    Author:吴霄鹤
    Last edit at: 2022-06-13
'''
# from asyncio.windows_events import NULL
import time
import pygame
from pygame.locals import *
import sys
#import headers
import init_
import display
import chess_AI
import actions
'''
    加载图片和背景音乐
'''

def key_control(screen, mode,background_music):
    """用于接收用户鼠标的信息

    """
    global running, i_temp1, j_temp1, i_temp2, j_temp2, order, wincolor, choose_turn_result, index, load, chessindex, \
        repent
    if order: 
        color = 0
    else:
        color = 1
    display.tip(screen, lst, color, mode[0], i_temp1, j_temp1, i_temp2, j_temp2)
    if choose_turn_result: # 如果电脑先手（初始值由choose_turn得出）
        lst[11][11] = int(color)
        display.draw_chessman(8, 8, screen, color) # 画最中间
        order = not order
        choose_turn_result = not choose_turn_result # order与choose_turn_result取反
        chessindex[11][11] = index # 将最中间的棋子索引记录为0
        index += 1
    display.draw_AI_takeover(screen,1)
    # 人类玩家开始落子
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_F1:
                background_music.stop()

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1: # 按左键
                x, y = event.pos[0], event.pos[1]
                if 650 < x < 790 and 350 < y < 380:
                    mode[0] = 1 -  mode[0]
                    display.tip(screen, lst, color, mode[0], i_temp1, j_temp1, i_temp2, j_temp2)
                    display.draw_AI_takeover(screen,1)
                    display.print_message(screen,"切换成功！")
                    pygame.time.wait(500)
                for i in range(4, 19):
                    for j in range(4, 19):
                        # 如果点击的位置无棋子，游戏运行中，且当前落子方为人类玩家
                        if ((i-4) * 40 + 15) < x < ((i-4) * 40 + 55) and ((j-4) * 40 + 15) < y < ((j-4) * 40 + 55) and lst[i][j] == 'Y' and running and not choose_turn_result: 
                            lst[i][j] = int (color) # 更新棋盘
                            repent = True # 悔棋为真
                            display.draw_chessman(i, j, screen, color)
                            init_.play_chess_sound.play(0)
                            pygame.display.update()
                            # (i_temp1,j_temp1)为本次落子的位置
                            i_temp1 = i
                            j_temp1 = j
                            wincolor = int(color) # 更新可能的胜利方
                            chessindex[i][j] = index
                            index += 1
                            if chess_AI.win(lst,i,j):
                                init_.victor_sound.play(0)
                                display.displaywin(screen,wincolor,lst,chessindex,index)
                            # 将电脑方操作放在了这里，是为了防止误触。即当人类方落子无效时，电脑方便不会行动。
                            if not mode[0] and running:
                                display.print_message(screen,"Alex思考中...")
                                time1 = time.time()
                                a = chess_AI.alphabeta(lst,3,init_.ninf,init_.pinf,int(not color),int(not color))
                                time2 = time.time()
                                print('Thought Process Lasted %.0f ms' % (1000*(time2-time1)))
                                repent = True
                                display.draw_chessman(a[0], a[1], screen,not color)
                                init_.play_chess_sound.play(0)
                                lst[a[0]][a[1]] = int(not color)
                                i_temp2 = a[0]
                                j_temp2 = a[1]
                                wincolor = int(not color)
                                chessindex[a[0]][a[1]] = index
                                index += 1
                                if chess_AI.win(lst,a[0],a[1]):
                                    init_.victor_sound.play(0)
                                    display.displaywin(screen,wincolor,lst,chessindex,index)
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
                    display.draw_chessboard_with_chessman(lst, screen)

                actions.choose_button(x, y)

        # 点X也退出游戏
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()


def main():
    '''主函数'''
    global order, lst, score, running, background_jpg, wincolor, i_temp1, j_temp1, \
        i_temp2, j_temp2, choose_turn_result, index, chessindex, load, repent, i_temp3, j_temp3,mode
    pygame.display.set_caption('五子不行V2')
    screen = pygame.display.set_mode((800, 624))
    screen.fill(init_.background)
    screen.blit(init_.background_jpg, (0, 0))
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
    display.draw_chessboard(screen)
    pygame.display.update()
    # 选择电脑先手还是玩家先手
    choose_turn_result = 0
    # 选择人人还是人机
    mode = [1]
    mode[0], load = actions.choose_mode()
    init_.background_music.stop()
    init_.background_music.play(-1) # -1是循环播放

    if not mode[0]: # 人人对战
        choose_turn_result = actions.choose_turn(screen) #选择先手
    if load:
        try:
            c_map = actions.load_chess(screen) # 读取棋谱
            display.print_message(screen,"Open Successful!") 
            actions.play_chess(screen, c_map)
            main()
        except:
            display.print_message(screen,"Open Failed!")
            pygame.time.wait(1000)
            main()
    
    while True:
        key_control(screen, mode,init_.background_music)
        pygame.display.update()


if __name__ == "__main__":
    main()
