
import init_
import pygame
import actions

def print_message(screen,text):
    """打印文字"""
    font = pygame.font.Font(init_.resource_path('fonts\\font1.ttf'), 20)
    text = font.render(text, True, init_.button)
    screen.blit(text, (640, 190))
    pygame.display.update()

def draw_chessboard(screen):
    """绘制棋盘,大小为15*15,和一些功能按钮。
    """
    global background, checkerboard, button
    # 画棋盘
    for i in range(15):
        pygame.draw.line(screen, init_.BLACK, (40 * i + 30, 30), (40 * i + 30, 590))
        pygame.draw.line(screen, init_.BLACK, (30, 40 * i + 30), (590, 40 * i + 30))
    # 画边界
    pygame.draw.line(screen, init_.BLACK, (2, 2), (2, 622), 4)
    pygame.draw.line(screen, init_.BLACK, (622, 2), (622, 622), 4)
    pygame.draw.line(screen, init_.BLACK, (2, 2), (622, 2), 4)
    pygame.draw.line(screen, init_.BLACK, (2, 622), (622, 622), 4)
    # 画棋盘的定位点
    pygame.draw.circle(screen, init_.checkerboard, (150, 150), 6)
    pygame.draw.circle(screen, init_.checkerboard, (470, 150), 6)
    pygame.draw.circle(screen, init_.checkerboard, (150, 470), 6)
    pygame.draw.circle(screen, init_.checkerboard, (470, 470), 6)
    pygame.draw.circle(screen, init_.checkerboard, (310, 310), 6)
    # 矩形参数由四个值构成的元组,分别是矩形左上角的x、y坐标,矩形的宽和高
    pygame.draw.rect(screen, init_.button, [640, 10, 140, 50], 5)
    pygame.draw.rect(screen, init_.button, [640, 70, 140, 50], 5)
    pygame.draw.rect(screen, init_.button, [640, 440, 80, 50], 5)
    pygame.draw.rect(screen, init_.button, [640, 500, 140, 50], 5)
    pygame.draw.rect(screen, init_.button, [640, 560, 140, 50], 5)
    pygame.draw.rect(screen, init_.button, [640, 230, 140, 50], 5)
    pygame.draw.rect(screen, init_.button, [640, 295, 60, 30], 3)
    pygame.draw.rect(screen, init_.button, [720, 295, 60, 30], 3)


    s_font = pygame.font.Font(init_.resource_path('fonts\\font1.ttf'), 30)
    d_font = pygame.font.Font(init_.resource_path('fonts\\font1.ttf'), 20)
    text1 = s_font.render("人人对战", True, init_.button)
    text2 = s_font.render("人机对战", True, init_.button)
    text3 = s_font.render("悔棋", True, init_.button)
    text4 = s_font.render("回主菜单", True, init_.button)
    text5 = s_font.render("退出游戏", True, init_.button)
    text6 = s_font.render("载入棋谱", True, init_.button)
    text7 = d_font.render("前一步", True, init_.button)
    text8 = d_font.render("后一步", True, init_.button)
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
        screen.blit(init_.black_chessman, ((x - 4) * 40 + 15, (y - 4) * 40 + 15))
    elif color == 1:
        screen.blit(init_.white_chessman, ((x - 4) * 40 + 15, (y - 4) * 40 + 15))


def draw_chessboard_with_chessman(chesslist, screen):
    """全盘绘制(包括棋盘和棋子)"""
    screen.fill(init_.background)
    screen.blit(init_.background_jpg, (0, 0))
    draw_chessboard(screen)
    for i in range(4, 20):
        for j in range(4, 20):
                draw_chessman(i, j, screen, chesslist[i][j])

def draw_AI_takeover(screen,flag):
    """绘制托管按钮,复用为保存按钮"""
    pygame.draw.rect(screen, init_.button, [640, 340, 140, 50], 5)
    s_font = pygame.font.Font(init_.resource_path('fonts\\font1.ttf'), 30)
    if(flag):
        text = s_font.render("切换模式", True, init_.button)
    else:
        text = s_font.render("棋谱保存", True, init_.button)
    screen.blit(text, (650, 350))
    pygame.display.update()

def pop_window(screen, color):
    """弹出胜利的界面

    """
    if not color:
        pygame.draw.rect(screen, init_.RED, [110, 230, 400, 160], 5)
        s_font = pygame.font.Font(init_.resource_path('fonts\\font1.ttf'), 80)
        text1 = s_font.render("黑棋胜利!", True, init_.RED)
        screen.blit(text1, (120, 270))
        pygame.display.update()
    elif color:
        pygame.draw.rect(screen, init_.RED, [110, 230, 400, 160], 5)
        s_font = pygame.font.Font(init_.resource_path('fonts\\font1.ttf'), 80)
        text1 = s_font.render("白棋胜利!", True, init_.RED)
        screen.blit(text1, (120, 270))
        pygame.display.update()


def tip(screen, chesslist, color, choose, i1, j1, i2, j2):
    """显示一些提示

    当前是什么模式,轮到谁落子,谁赢了
    """
    s_font = pygame.font.Font(init_.resource_path('fonts\\font.ttf'), 40)
    text1 = s_font.render("黑棋落子", True, init_.button)
    text2 = s_font.render("白棋落子", True, init_.button)
    s_font1 = pygame.font.Font(init_.resource_path('fonts\\font1.ttf'), 30)
    text3 = s_font1.render("人人对战", True, init_.button, (100, 100, 100))
    text4 = s_font1.render("人机对战", True, init_.button, (100, 100, 100))
    draw_chessboard_with_chessman(chesslist, screen)
    if not color: # 黑棋落子
        screen.blit(text1, (630, 140))
    else: # 白棋落子
        screen.blit(text2, (630, 140))
    if choose: # 如果是人机对战
        screen.blit(text3, (650, 20))
        pygame.draw.rect(screen, init_.button, [(i1 - 4) * 40 + 15, (j1 - 4) * 40 + 15, 30, 30], 3)
    else:
        screen.blit(text4, (650, 80))
        pygame.draw.rect(screen, init_.button, [(i1 - 4) * 40 + 15, (j1 - 4) * 40 + 15, 30, 30], 3)
        pygame.draw.rect(screen, init_.button, [(i2 - 4) * 40 + 15, (j2 - 4) * 40 + 15, 30, 30], 3)

def displaywin(screen,wincolor,chesslist,chessindex,index):
    '''
    显示胜利界面
    '''
    draw_chessboard_with_chessman(chesslist,screen)
    pop_window(screen, wincolor) # 弹出胜利的界面
    draw_AI_takeover(screen,0)
    pygame.display.update()
    actions.choose_save(screen,chesslist, chessindex, index) # 激活保存按钮