import pygame
import random

pygame.init() #Инициализация игрового модуля 
running = True 
pygame.display.set_caption("Воздушный бой")

currentImg =0 #Текущее фоновое изображение
sprites=[] #Массив изображений
for i in range(0,60):
    sprite = pygame.image.load("sky/"+str(i)+".gif") #Импорт изображений
    sprite = pygame.transform.rotate(sprite,-90) #Поворот на 90 градусов
    sprites.append(sprite) #Заполнение массива изображений

#ScoreBoard
highscore = 0 #Лучший результат

font = pygame.font.Font('freesansbold.ttf',32) #Инициализация шрифта


def startGame(): #Функция начала игры
    screen = pygame.display.set_mode((800,600)) #Инициализация игрового экрана
    def showScore(string,value,x,y): #Функия отображения текста
        Text = font.render((string+str(value)),True,(225,225,225))
        screen.blit(Text,(x,y)) #Рендеринг

    #ScoreBoard
    global highscore
    global font
    scores = 0 #Ну тут и так все понятно -_-
    level = 1
    lives = 5

    #Время
    paused = False #Игровое состояние
    clock = pygame.time.Clock() #Инициализацие игрового фрейма
    current_time = 0 #Текущее время
    time_point = pygame.time.get_ticks() #Точка временного отсчета
    spawn_time = 5 #Время спавна врагов

    global running
    #Игрок
    playerImg = pygame.image.load("plane.png") #Спрайт игрока
    playerX = 370 #Позиция игрока по осям
    playerY = 450
    def player(x,y): #Функция рендеринга игрока
        screen.blit(playerImg,(x,y))

    #Противники
    enemyImg = pygame.image.load("enemy.png") #Спрайт противника
    enemies = [] #Массив противников
    enemy = { #Первый противник
        "enemyX" : random.randint(0,650),
        "enemyY" : -100
        }
    enemies.append(enemy) #Добавление противника в мссив

    #При добавлении противника в массив он автоматически отображается на экране

    def spawnEnemy(): #Функция спавна противников
        enemies.append({"enemyX" : random.randint(0,650),"enemyY" : -100}) #Добавление противника в мссив
    def renderEnemy(x,y): #Рендер противника
        screen.blit(enemyImg,(x,y))
    speed = 1 #Скорость


    #Пули
    bulletImg = pygame.image.load("bullet.png") #Спрайт пули
    bullets = [] #Массив пуль
    bullet = { #Координаты пули
        "bulletX" : playerX+57,
        "bulletY" : playerX+40
        }
    bullet_is_ready = True #Состояние пули: true - можно стрелять; false - нельзя
    def spawnBullet(): #Спавн пуль
        bullets.append({"bulletX" : playerX+57,"bulletY" : playerY+40})
    def renderBullet(x,y):
        screen.blit(bulletImg,(x,y))

    #Проверка коллизий
    def isCollision(enemyX,enemyY,bulletX,bulletY): #Коллизия - это столкновение
        #Если координаты пули пересекаются с координатами противника
        if bulletX >= enemyX and bulletX <= enemyX+140: 
            if bulletY >= enemyY and bulletY <= enemyY+140:
                return True #Функция возвращает True
            else:
                return False
        else:
            return False
    frame = pygame.time.get_ticks() #Фрейм рендеринга заднего фона
    #Игровой цикл
    while running: #Выполняется каждый фрейм
        global currentImg
        current_time = pygame.time.get_ticks() #установка текущего времени
        #Всего имеется 59 фоновых изображений
        if currentImg>=60: 
            currentImg=0
        if current_time - frame >= 30 and not(paused):
            screen.blit(sprites[currentImg], [0, 0]) #Установка следующего фонового изображения каждые 30 мсек
            currentImg+=1
            frame = pygame.time.get_ticks()
        
        for event in pygame.event.get(): #Останавливаем игру если игрок выходит из программы
            if event.type == pygame.QUIT:
                running = false

        #Обработка нажатия клавиш
        if event.type == pygame.KEYDOWN: #Перемещаем игрока по оси Х при нажатии а кнопки
            if event.key == pygame.K_LEFT:
                playerX-=2
            elif event.key == pygame.K_RIGHT:
                playerX+=2

        #Ограничение координат игрока
        if playerX<=0: #Чтобы игрок не мог выйти за пределы экрана
            playerX =0
        elif playerX>=650:
            playerX=650

        #Цикл поведения врагов
        if not(paused): #Запускается только во время активной стадии игры
            if current_time - time_point >= spawn_time*1000: 
                spawnEnemy() #Спавн врагов через каждые spawn_time секунд
                time_point = pygame.time.get_ticks()
            if len(enemies)>0:
                for i in range(0,len(enemies)-1): #Движение противников
                    x = enemies[i]["enemyX"]
                    y = enemies[i]["enemyY"]
                    renderEnemy(x,y) #Рендер
                    enemies[i]["enemyY"]+=0.1*speed #Каждый фрейм противник приближается к игроку со скоростью speed
                    if y>600: #Если противник достиг нижнего края экрана
                        lives-=1 #Отнмаем у игрока одну жизнь
                        enemies.remove(enemies[i]) #И удаляем противника чтобы он не захламлял память
                    if len(bullets)>0:
                        for j in range(0,len(bullets)):
                            #Проверяем все пули на пересечение с противниками
                            #Если пуля попала в противника
                            if isCollision(x,y,bullets[j]['bulletX'],bullets[j]['bulletY']):
                                #Удаляем противника и пулю, попавшую в него
                                enemies.remove(enemies[i])
                                bullets.remove(bullets[j])
                                scores+=1 #Добавляем игроку одно очко
                                #Если игрок набрал число очков кратное трём
                                if scores%3==0: 
                                    level+=1 #Увеличиваем уровень
                                    if spawn_time>=1.5: #Убыстряем время спавна
                                        spawn_time*=0.8
                                    if speed<10: #Увеличиваем скорость противников
                                        speed+=1
                                bullet_is_ready = True #Устанавливаем готовность к выстрелу
        
        #Цикл поведения пуль
        if event.type == pygame.KEYDOWN:
            #Если мы нажали кнопку и игрок готов к выстрелу
            if event.key == pygame.K_UP and bullet_is_ready:
                spawnBullet() #Спавним пулю
                bullet_is_ready = False #Ставим игрока на перезарядку
        if len(bullets)>0:
            for i in range(0,len(bullets)): #Двигаем пулю по оси У вверх на 1 пиксель каждый фрейм
                x = bullets[i]["bulletX"]
                y = bullets[i]["bulletY"]
                renderBullet(x,y)
                bullets[i]["bulletY"]-=1
                if y<=0: #Если пуля вышла за пределы экрана
                    bullets.remove(bullets[i]) #Удаляем ее
                    bullet_is_ready = True #Устанавливаем готовность к выстрелу

        if lives<=0: #Если у игрока закончились жизни
            pygame.time.delay(30) #Останавливаем время каждый фрейм на 30 мсек 
            paused = True #Ставим игровой процесс на паузу
            if scores>highscore: #Если очки превышают рекорд
                highscore = scores #Устанавливаем новое рекордное значение
            showScore("GAME OVER","",300,250) #Результаты раунда
            showScore("highscore: ",highscore,300,280)
            showScore("press any key to restart","",220,310)
            if event.type == pygame.KEYDOWN: #Ожидаем нажатие игрока
                startGame() #Начинаем игру заново
                
        #Выводим очки на экран
        showScore("Scores: ",scores,10,10)
        showScore("Level: ",level,10,40)
        showScore("Lives: ",lives,10,70)
        player(playerX,playerY) #Рендерим игрока
        pygame.display.update() #Обновляем дисплей каждый фрейм
        clock.tick(300) #Устанавливаем такт в 300 мсек

startGame() #Вызываем функцию запуска игры