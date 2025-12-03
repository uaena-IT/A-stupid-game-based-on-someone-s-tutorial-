import pygame
import time
import random
import os
import sys

# 添加资源路径处理函数
def resource_path(relative_path):
    """获取资源的绝对路径，用于开发环境和打包后环境"""
    try:
        # PyInstaller 创建的临时文件夹
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

# 初始化pygame
pygame.init()

# 加载资源时使用 resource_path 函数
carImg = pygame.image.load(resource_path('racecar.png'))
gameIcon = pygame.image.load(resource_path('carIcon.png'))

# 游戏窗口尺寸
display_width = 800
display_height = 600

# 定义颜色
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
bright_red = (255,0,0)  # 高亮红色（用于按钮悬停效果）
bright_green = (0,255,0)  # 高亮绿色（用于按钮悬停效果）
block_color = (53,115,255)  # 障碍物颜色
car_width = 73  # 汽车宽度

# 创建游戏窗口
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('A bit Racey')  # 设置窗口标题
clock = pygame.time.Clock()  # 创建时钟对象用于控制帧率

# 设置窗口图标
pygame.display.set_icon(gameIcon)

# 游戏状态变量
pause = False  # 暂停状态

# 显示躲避障碍物数量的函数
def things_dodged(count):
    font = pygame.font.SysFont("comicsansms", 25)
    text = font.render("Dodged: "+str(count), True, black)
    gameDisplay.blit(text,(0,0))  # 在左上角显示躲避数量

# 绘制障碍物的函数
def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])

# 绘制汽车的函数
def car(x,y):
    gameDisplay.blit(carImg,(x,y))

# 创建文本对象的函数
def text_objects(text, font):
    textSurface = font.render(text, True, black)  # 渲染文本
    return textSurface, textSurface.get_rect()  # 返回文本表面和矩形区域

# 显示消息的函数
def message_display(text):
    largeText = pygame.font.SysFont("comicsansms",115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))  # 文本居中
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()  # 更新显示
    time.sleep(2)  # 暂停2秒
    game_loop()  # 重新开始游戏

# 碰撞处理函数
def crash():
    largeText = pygame.font.SysFont("comicsansms",115)
    TextSurf, TextRect = text_objects("You Crashed", largeText)
    TextRect.center = ((display_width/2),(display_height/2))  # 文本居中
    gameDisplay.blit(TextSurf, TextRect)

    # 碰撞后的循环
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 检测退出事件
                pygame.quit()
                sys.exit()  # 使用 sys.exit() 替代 quit()
                
        # 创建"重新开始"和"退出"按钮
        button("Play Again",150,450,100,50,green,bright_green,game_loop)
        button("Quit",550,450,100,50,red,bright_red,quitgame)

        pygame.display.update()  # 更新显示
        clock.tick(15)  # 控制帧率

# 创建按钮的函数
def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()  # 获取鼠标位置
    click = pygame.mouse.get_pressed()  # 获取鼠标点击状态

    # 检查鼠标是否在按钮上
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))  # 使用激活颜色
        if click[0] == 1 and action != None:  # 如果点击了按钮且有指定动作
            action()  # 执行动作         
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))  # 使用默认颜色
        
    # 创建按钮文本
    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )  # 文本居中
    gameDisplay.blit(textSurf, textRect)  # 绘制文本

# 退出游戏函数
def quitgame():
    pygame.quit()
    sys.exit()  # 使用 sys.exit() 替代 quit()

# 取消暂停函数
def unpause():
    global pause
    pause = False  # 设置暂停状态为False

# 暂停界面函数
def paused():
    largeText = pygame.font.SysFont("comicsansms",115)
    TextSurf, TextRect = text_objects("Paused", largeText)
    TextRect.center = ((display_width/2),(display_height/2))  # 文本居中
    gameDisplay.blit(TextSurf, TextRect)

    # 暂停循环
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 检测退出事件
                pygame.quit()
                sys.exit()  # 使用 sys.exit() 替代 quit()

        # 创建"继续"和"退出"按钮
        button("Continue",150,450,100,50,green,bright_green,unpause)
        button("Quit",550,450,100,50,red,bright_red,quitgame)

        pygame.display.update()  # 更新显示
        clock.tick(15)  # 控制帧率

# 游戏开始界面函数
def game_intro():
    intro = True  # 开始界面状态

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 检测退出事件
                pygame.quit()
                sys.exit()  # 使用 sys.exit() 替代 quit()
                
        gameDisplay.fill(white)  # 填充白色背景
        
        # 显示游戏标题
        largeText = pygame.font.SysFont("comicsansms",115)
        TextSurf, TextRect = text_objects("A bit Racey", largeText)
        TextRect.center = ((display_width/2),(display_height/2))  # 文本居中
        gameDisplay.blit(TextSurf, TextRect)

        # 创建"开始"和"退出"按钮
        button("GO!",150,450,100,50,green,bright_green,game_loop)
        button("Quit",550,450,100,50,red,bright_red,quitgame)

        pygame.display.update()  # 更新显示
        clock.tick(15)  # 控制帧率

# 游戏主循环函数
def game_loop():
    global pause  # 使用全局暂停变量
    
    # 设置汽车的初始位置
    x = (display_width * 0.45)
    y = (display_height * 0.8)
 
    x_change = 0  # 汽车水平移动速度
 
    # 设置障碍物的初始属性
    thing_startx = random.randrange(0, display_width)  # 随机水平位置
    thing_starty = -600  # 从屏幕上方开始
    thing_speed = 4  # 下落速度
    thing_width = 100  # 宽度
    thing_height = 100  # 高度
 
    thingCount = 1  # 障碍物数量
    dodged = 0  # 躲避计数
    gameExit = False  # 游戏退出标志
 
    # 游戏主循环
    while not gameExit:
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 检测退出事件
                pygame.quit()
                sys.exit()  # 使用 sys.exit() 替代 quit()
 
            if event.type == pygame.KEYDOWN:  # 键盘按下事件
                if event.key == pygame.K_LEFT:  # 左箭头键
                    x_change = -5
                if event.key == pygame.K_RIGHT:  # 右箭头键
                    x_change = 5
                if event.key == pygame.K_p:  # P键暂停
                    pause = True
                    paused()
 
            if event.type == pygame.KEYUP:  # 键盘释放事件
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0  # 停止移动
 
        # 更新汽车位置
        x += x_change
        
        # 填充背景色
        gameDisplay.fill(white)
 
        # 绘制障碍物
        things(thing_startx, thing_starty, thing_width, thing_height, block_color)
 
        # 更新障碍物位置
        thing_starty += thing_speed
        
        # 绘制汽车和躲避计数
        car(x,y)
        things_dodged(dodged)
 
        # 检测汽车是否撞到左右边界
        if x > display_width - car_width or x < 0:
            crash()  # 调用碰撞处理函数
 
        # 当障碍物移出屏幕底部时，重置到顶部
        if thing_starty > display_height:
            thing_starty = 0 - thing_height  # 重置到屏幕上方
            thing_startx = random.randrange(0,display_width)  # 随机水平位置
            dodged += 1  # 增加躲避计数
            thing_speed += 1  # 增加障碍物速度
            thing_width += (dodged * 1.2)  # 增加障碍物宽度
 
        # 检测汽车与障碍物的碰撞
        if y < thing_starty+thing_height:
            # 检查x轴方向是否重叠
            if x > thing_startx and x < thing_startx + thing_width or x+car_width > thing_startx and x + car_width < thing_startx+thing_width:
                crash()  # 碰撞处理
        
        pygame.display.update()  # 更新显示
        clock.tick(60)  # 控制帧率为60FPS

# 启动游戏
game_intro()  # 显示开始界面
game_loop()  # 开始游戏主循环
pygame.quit()  # 退出pygame
sys.exit()  # 退出程序