from pygame import *
from random import *

# Инициализация шрифтов
font.init()

win_width, win_height = 700, 500
window = display.set_mode((win_width, win_height))
display.set_caption('ping pong(boba team)')
background = transform.scale(image.load('abstract-textured-backgound.jpg'), (win_width, win_height))

# Шрифты
font_main = font.SysFont('Arial', 36)
font_score = font.SysFont('Arial', 50)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class PlayerL(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - self.rect.height - 5:
            self.rect.y += self.speed

class PlayerR(GameSprite):
    def update(self, ball, bot_difficulty):
        # Если выбран режим "Игрок" (0)
        if bot_difficulty == 0:
            keys = key.get_pressed()
            if keys[K_UP] and self.rect.y > 5:
                self.rect.y -= self.speed
            if keys[K_DOWN] and self.rect.y < win_height - self.rect.height - 5:
                self.rect.y += self.speed
        
        # Если выбран бот
        else:
            # Настройка точности/скорости бота в зависимости от сложности
            if bot_difficulty == 1:    # Легкий
                bot_speed = 3
            elif bot_difficulty == 2:  # Средний
                bot_speed = 5
            elif bot_difficulty == 3:  # Сложный
                bot_speed = 7

            # Логика слежения за мячом
            if self.rect.centery < ball.rect.centery and self.rect.y < win_height - self.rect.height - 5:
                self.rect.y += bot_speed
            elif self.rect.centery > ball.rect.centery and self.rect.y > 5:
                self.rect.y -= bot_speed

# Создание объектов
paddle_l = PlayerL('ping-pong_13026182.png', 0, 200, 75, 100, 5)
paddle_r = PlayerR('ping-pong_13026182.png', 625, 200, 75, 100, 5)
ball = GameSprite('pingpong.png', 350, 250, 20, 20, 4) 

ball_speed_x = ball.speed 
ball_speed_y = ball.speed 

# Переменные счета
score_l = 0
score_r = 0

clock = time.Clock()

# Состояния игры: 'menu' или 'game'
state = 'menu'
# 0 - Второй игрок, 1 - Легкий бот, 2 - Средний бот, 3 - Сложный бот
bot_mode = 0 

# Кнопки меню (Прямоугольники для кликов)
btn_player = Rect(250, 150, 200, 50)
btn_easy = Rect(250, 220, 200, 50)
btn_medium = Rect(250, 290, 200, 50)
btn_hard = Rect(250, 360, 200, 50)

game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        
        # Обработка кликов в меню
        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            mouse_pos = e.pos
            if state == 'menu':
                if btn_player.collidepoint(mouse_pos):
                    bot_mode = 0
                    state = 'game'
                elif btn_easy.collidepoint(mouse_pos):
                    bot_mode = 1
                    state = 'game'
                elif btn_medium.collidepoint(mouse_pos):
                    bot_mode = 2
                    state = 'game'
                elif btn_hard.collidepoint(mouse_pos):
                    bot_mode = 3
                    state = 'game'

    if state == 'menu':
        window.blit(background, (0, 0))
        
        # Отрисовка кнопок
        draw.rect(window, (100, 100, 255), btn_player)
        draw.rect(window, (100, 255, 100), btn_easy)
        draw.rect(window, (255, 255, 100), btn_medium)
        draw.rect(window, (255, 100, 100), btn_hard)
        
        # Текст на кнопках
        window.blit(font_main.render('2 Players', True, (255, 255, 255)), (285, 155))
        window.blit(font_main.render('Easy Bot', True, (0, 0, 0)), (295, 225))
        window.blit(font_main.render('Medium Bot', True, (0, 0, 0)), (275, 295))
        window.blit(font_main.render('Hard Bot', True, (255, 255, 255)), (295, 365))
        
        # Заголовок
        window.blit(font_main.render('Select Game Mode:', True, (255, 255, 255)), (230, 80))

    elif state == 'game':
        window.blit(background, (0, 0))
        draw.line(window, (255, 255, 255), (win_width // 2, 0), (win_width // 2, win_height), 4)

        # Отображение счета
        text_score = font_score.render(f"{score_l} : {score_r}", True, (255, 255, 255))
        window.blit(text_score, (win_width // 2 - text_score.get_width() // 2, 20))

        # Обновление спрайтов
        paddle_l.update()
        paddle_r.update(ball, bot_mode) # Передаем мяч и режим бота

        # Движение мяча
        ball.rect.x += ball_speed_x
        ball.rect.y += ball_speed_y

        # Отскок от верхних/нижних границ
        if ball.rect.y <= 0 or ball.rect.y >= win_height - ball.rect.height:
            ball_speed_y *= -1
        
        # Отскок от ракеток
        if sprite.collide_rect(ball, paddle_l) or sprite.collide_rect(ball, paddle_r):
            ball_speed_x *= -1  
            
        # Гол левому игроку (очко правому)
        if ball.rect.x < 0:
            score_r += 1
            ball.rect.x, ball.rect.y = 350, 250
            ball_speed_x *= -1

        # Гол правому игроку (очко левому)
        if ball.rect.x > win_width:
            score_l += 1
            ball.rect.x, ball.rect.y = 350, 250
            ball_speed_x *= -1

        # Отрисовка
        paddle_l.reset()
        paddle_r.reset()
        ball.reset()

    display.update()
    clock.tick(60)


























































































































































































































     