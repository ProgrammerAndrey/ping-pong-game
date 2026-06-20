from pygame import *
from random import *

font.init()
mixer.init()

win_width, win_height = 700, 500
window = display.set_mode((win_width, win_height))
display.set_caption('ping pong(boba team)')

font_main = font.SysFont('Arial', 28)
font_score = font.SysFont('Arial', 50)
font_small = font.SysFont('Arial', 16)
font_win = font.SysFont('Arial', 60)
font_desc = font.SysFont('Arial', 18)



mixer.music.load('music_.ogg')
mixer.music.play(-1)

class GameSprite(sprite.Sprite):
    def __init__(self, color, player_x, player_y, size_x, size_y, player_speed, is_ball=False):
        super().__init__()
        self.color = color
        self.size_x = size_x
        self.size_y = size_y
        self.speed = player_speed
        self.is_ball = is_ball
        self.rect = Rect(player_x, player_y, size_x, size_y)

    def reset(self):
        if self.is_ball:
            draw.circle(window, self.color, (self.rect.x + self.size_x // 2, self.rect.y + self.size_y // 2), self.size_x // 2)
        else:
            draw.rect(window, self.color, self.rect)

class PlayerL(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - self.rect.height - 5:
            self.rect.y += self.speed

class PlayerR(GameSprite):
    def update(self, ball, bot_difficulty):
        if bot_difficulty == 0:
            keys = key.get_pressed()
            if keys[K_UP] and self.rect.y > 5:
                self.rect.y -= self.speed
            if keys[K_DOWN] and self.rect.y < win_height - self.rect.height - 5:
                self.rect.y += self.speed
        else:
            if bot_difficulty == 1:
                bot_speed = 3
            elif bot_difficulty == 2:
                bot_speed = 5
            elif bot_difficulty == 3:
                bot_speed = 7

            if self.rect.centery < ball.rect.centery and self.rect.y < win_height - self.rect.height - 5:
                self.rect.y += bot_speed
            elif self.rect.centery > ball.rect.centery and self.rect.y > 5:
                self.rect.y -= bot_speed

paddle_l = PlayerL((255, 255, 255), 10, 200, 20, 100, 5)
paddle_r = PlayerR((255, 255, 255), 670, 200, 20, 100, 5)
ball = GameSprite((223, 255, 0), 350, 250, 20, 20, 4, is_ball=True) 

ball_speed_x = ball.speed 
ball_speed_y = ball.speed 

score_l = 0
score_r = 0
game_over = False

clock = time.Clock()

state = 'menu'
bot_mode = 0 

btn_player = Rect(225, 140, 250, 45)
btn_easy = Rect(225, 200, 250, 45)
btn_medium = Rect(225, 260, 250, 45)
btn_hard = Rect(225, 320, 250, 45)

btn_info = Rect(225, 410, 250, 35)
btn_back = Rect(win_width // 2 - 50, win_height - 50, 100, 30)

game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            mouse_pos = e.pos
            if state == 'menu':
                if btn_player.collidepoint(mouse_pos):
                    bot_mode = 0
                    state = 'game'

                    mixer.music.stop()
                    mixer.music.load('game_music.mp3')
                    mixer.music.play(-1)

                elif btn_easy.collidepoint(mouse_pos):
                    bot_mode = 1
                    state = 'game'

                    mixer.music.stop()
                    mixer.music.load('game_music.mp3')
                    mixer.music.play(-1)

                elif btn_medium.collidepoint(mouse_pos):
                    bot_mode = 2
                    state = 'game'

                    mixer.music.stop()
                    mixer.music.load('game_music.mp3')
                    mixer.music.play(-1)

                elif btn_hard.collidepoint(mouse_pos):
                    bot_mode = 3
                    state = 'game'

                    mixer.music.stop()
                    mixer.music.load('game_music.mp3')
                    mixer.music.play(-1)
            
            elif state == 'description':
                if btn_back.collidepoint(mouse_pos):
                    state = 'menu'

            elif state == 'game':
                if btn_back.collidepoint(mouse_pos):
                    state = 'menu'

                    mixer.music.stop()
                    mixer.music.load('music_.ogg')
                    mixer.music.play(-1)

                    score_l = 0
                    score_r = 0
                    game_over = False
                    ball.rect.x, ball.rect.y = 350, 250

                    mixer.music.stop()
                    mixer.music.load('music_.ogg')
                    mixer.music.play(-1)

                    score_l = 0
                    score_r = 0
                    game_over = False
                    ball.rect.x, ball.rect.y = 350, 250

    if state == 'menu':
        window.fill((34, 110, 63))
        
        title_text = font_main.render('ПИНГ-ПОНГ (BOBA TEAM)', True, (223, 255, 0))
        window.blit(title_text, (win_width // 2 - title_text.get_width() // 2, 30))
        
        mode_text = font_main.render('Выберите режим игры:', True, (255, 255, 255))
        window.blit(mode_text, (win_width // 2 - mode_text.get_width() // 2, 90))
        
        draw.rect(window, (255, 255, 255), btn_player, 2)
        draw.rect(window, (255, 255, 255), btn_easy, 2)
        draw.rect(window, (255, 255, 255), btn_medium, 2)
        draw.rect(window, (255, 255, 255), btn_hard, 2)
        draw.rect(window, (223, 255, 0), btn_info, 1)
        
        txt1 = font_main.render('Мультиплеер', True, (255, 255, 255))
        txt2 = font_main.render('Лёгкий бот', True, (255, 255, 255))
        txt3 = font_main.render('Средний бот', True, (255, 255, 255))
        txt4 = font_main.render('Сложный бот', True, (255, 255, 255))
        txt_info = font_small.render('Описание', True, (223, 255, 0))
        
        window.blit(txt1, (btn_player.x + (btn_player.width - txt1.get_width()) // 2, btn_player.y + 5))
        window.blit(txt2, (btn_easy.x + (btn_easy.width - txt2.get_width()) // 2, btn_easy.y + 5))
        window.blit(txt3, (btn_medium.x + (btn_medium.width - txt3.get_width()) // 2, btn_medium.y + 5))
        window.blit(txt4, (btn_hard.x + (btn_hard.width - txt4.get_width()) // 2, btn_hard.y + 5))
        window.blit(txt_info, (btn_info.x + (btn_info.width - txt_info.get_width()) // 2, btn_info.y + 7))

    elif state == 'description':
        window.fill((34, 110, 63))
        
        title_text = font_main.render('ОПИСАНИЕ И ПРАВИЛА', True, (223, 255, 0))
        window.blit(title_text, (win_width // 2 - title_text.get_width() // 2, 40))
        
        desc1 = font_desc.render('Классический пинг-понг для игры вдвоём и с ботами.', True, (255, 255, 255))
        window.blit(desc1, (40, 110))
        
        desc_rules = font_main.render('Правила:', True, (223, 255, 0))
        window.blit(desc_rules, (40, 160))
        
        desc2 = font_desc.render('Игрок 1 (Слева): управление кнопками W и S.', True, (255, 255, 255))
        desc3 = font_desc.render('Игрок 2 (Справа): управление СТРЕЛКАМИ вверх и вниз.', True, (255, 255, 255))
        desc4 = font_desc.render('Матч ведется до 5 набранных очков.', True, (255, 255, 255))
        desc5 = font_desc.render('Отбивайте шарик ракеткой и защищайте свой край поля.', True, (255, 255, 255))
        desc6 = font_desc.render('Доступна игра против одного из 3 уровней сложности ботов.', True, (255, 255, 255))
        
        window.blit(desc2, (40, 210))
        window.blit(desc3, (40, 245))
        window.blit(desc4, (40, 280))
        window.blit(desc5, (40, 315))
        window.blit(desc6, (40, 350))
        
        draw.rect(window, (255, 255, 255), btn_back, 1)
        txt_back = font_small.render('Назад', True, (255, 255, 255))
        window.blit(txt_back, (btn_back.x + (btn_back.width - txt_back.get_width()) // 2, btn_back.y + 5))

    elif state == 'game':
        window.fill((34, 110, 63))
        draw.line(window, (255, 255, 255), (win_width // 2, 0), (win_width // 2, win_height), 4)

        draw.rect(window, (255, 255, 255), btn_back, 1)
        txt_back = font_small.render('В меню', True, (255, 255, 255))
        window.blit(txt_back, (btn_back.x + (btn_back.width - txt_back.get_width()) // 2, btn_back.y + 5))

        text_score = font_score.render(f"{score_l} : {score_r}", True, (255, 255, 255))
        window.blit(text_score, (win_width // 2 - text_score.get_width() // 2, 20))

        if not game_over:
            paddle_l.update()
            paddle_r.update(ball, bot_mode)

            ball.rect.x += ball_speed_x
            ball.rect.y += ball_speed_y

            if ball.rect.y <= 0 or ball.rect.y >= win_height - ball.rect.height:
                ball_speed_y *= -1
            
            if sprite.collide_rect(ball, paddle_l) or sprite.collide_rect(ball, paddle_r):
                ball_speed_x *= -1  
                
            if ball.rect.x < 0:
                score_r += 1
                if score_r >= 5:
                    game_over = True
                else:
                    ball.rect.x, ball.rect.y = 350, 250
                    ball_speed_x *= -1

            if ball.rect.x > win_width:
                score_l += 1
                if score_l >= 5:
                    game_over = True
                else:
                    ball.rect.x, ball.rect.y = 350, 250
                    ball_speed_x *= -1

        else:
            if score_l >= 5:
                win_text = font_win.render('WIN!', True, (223, 255, 0))
            else:
                if bot_mode == 0:
                    win_text = font_win.render('LOSE:(', True, (223, 255, 0))
                else:
                    win_text = font_win.render('BOT WIN!!', True, (255, 100, 100))
            window.blit(win_text, (win_width // 2 - win_text.get_width() // 2, win_height // 2 - win_text.get_height() // 2))

        paddle_l.reset()
        paddle_r.reset()
        ball.reset()

    display.update()
    clock.tick(60)
