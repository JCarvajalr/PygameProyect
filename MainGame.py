import pygame, random

import pygame.image

#Clases
class Enemie(pygame.sprite.Sprite):
    velocidad = 0
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Icons/Meteor.png").convert()
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()    
    def update(self):
        self.rect.y += self.velocidad
        if (self.rect.y > height):
            self.rect.y = -10
            self.rect.x = random.randrange(10, width-50)
class Player(pygame.sprite.Sprite):
    vida = 5
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Icons/spaceShip.png").convert()
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()   
class BarraVida(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Icons/Vida5.png").convert()
        self.rect = self.image.get_rect() 
class Disparo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Icons/Disparo.png").convert()
        #self.image.set_colorkey([254, 254, 254])
        self.rect = self.image.get_rect()   
    def update(self):
        self.rect.y -= 5
def crearEnemigo(enemiesSprites, spriteList):
    enemie = Enemie()
    enemie.rect.x = random.randrange(10, width-50)
    enemie.rect.y = random.randrange(-700, -20)
    enemiesSprites.add(enemie)
    spriteList.add(enemie)
    enemie.velocidad = random.randrange(2, 4) #Velocidad de enemigos

def mostrarTexto(texto, fuente, size, posX, posY):
    fuente = pygame.font.SysFont(fuente, size)
    superficie = fuente.render(texto, True, white)
    pos = superficie.get_rect()
    pos.midtop = (posX, posY)
    screen.blit(superficie, pos)

pygame.init()
## - Constantes -
width = 900
height = 800
colorBg = (0, 0, 0)
white = (255, 255, 255)
velocidadJugador = 5
## --
screen = pygame.display.set_mode([width, height])
clock = pygame.time.Clock()
backgroundGame = pygame.image.load("Icons/Background.png").convert()
backgroundMenu = pygame.image.load("Icons/MenuBackground.png").convert()
def menu():
    #quitGame = False
    #while not quitGame:
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed():
                    if event.key == pygame.K_x:
                        pygame.quit()
                        quit()
                    menu = False 
        screen.blit(backgroundMenu, (-150, -80))       
        mostrarTexto("Python Game", "Arial Black", 70, width/2, height/4)
        mostrarTexto("Presiona cualquier tecla para jugar", None, 45, width/2, height/2)
        mostrarTexto("Presiona 'X' para salir", "None", 30, width/2, height/2 + 50)
        pygame.display.flip()
        clock.tick(15)
    start()

def start():
    score = 0
    gameState = True
    #initPlayer
    spriteList = pygame.sprite.Group()
    player = Player()
    player.rect.x = (width/2)-40
    player.rect.y = height-120
    spriteList.add(player)
    barraVida = BarraVida()
    spriteList.add(barraVida)
    #Creación de enemigos
    enemiesSprites = pygame.sprite.Group()
    for i in range (20):
        crearEnemigo(enemiesSprites, spriteList)
    #Configuraciones de disparo
    balas = pygame.sprite.Group()
    tiempoUltimoDisparo = pygame.time.get_ticks()
    reloadTime = 300
    while gameState:
        currentTime = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameState = False
        # - Eventos teclado -
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_SPACE]:
            if currentTime - tiempoUltimoDisparo > reloadTime:
                disparo = Disparo()
                disparo.rect.center = player.rect.center
                balas.add(disparo)
                spriteList.add(disparo)
                tiempoUltimoDisparo = currentTime

        #Movimiento jugador
        if teclas[pygame.K_LEFT] and player.rect.left > 0:
            player.rect.x -= velocidadJugador
        if teclas[pygame.K_RIGHT] and player.rect.right < width:
            player.rect.x += velocidadJugador
        screen.blit(backgroundGame, [0, 0])
        spriteList.update()

        ## - Dibujo -
        mostrarTexto(f"Score: {score}", "Arial Black", 30, width-80, height-50)
        barraVida.rect.centerx = player.rect.centerx
        barraVida.rect.y = player.rect.bottom
        spriteList.draw(screen)

        #Colision de jugador con enemigo (Perder vida)
        for enemie in enemiesSprites:
            if player.rect.colliderect(enemie):
                spriteList.remove(enemie)
                enemiesSprites.remove(enemie)
                crearEnemigo(enemiesSprites, spriteList)
                player.vida -= 1
                #FIN DEL JUEGO
                if player.vida == 0: 
                    gameState = False
                    break
                barraVida.image = pygame.image.load(f"Icons/Vida{player.vida}.png").convert()   
                print(player.vida)        
                
        #Colision balas con enemigos
        for bala in balas:
            for enemie in enemiesSprites:
                if bala.rect.colliderect(enemie):
                    spriteList.remove(enemie, bala)
                    enemiesSprites.remove(enemie)
                    balas.remove(bala)
                    score += 1
                    crearEnemigo(enemiesSprites, spriteList)
            if bala.rect.y < 0:
                spriteList.remove(bala)
                balas.remove(bala)
        #Actualizacion de pantalla
        pygame.display.flip()
        clock.tick(60)
    if player.vida == 0: 
        print("Pierde")
        gameOver(score)

def gameOver(score):
    continuar = False
    while not continuar:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuar = True
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                continuar = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    pygame.quit()
                    quit()
        screen.fill(colorBg)
        mostrarTexto("Game Over", "Arial Black", 70, width/2, height/4)
        mostrarTexto("Click para continuar", None, 45, width/2, height/2)
        mostrarTexto(f"Score: {score}", "None", 30, width/2, height/2 + 50)
        mostrarTexto(f"Presiona X para salir", "None", 30, width/2, height - 50)
        pygame.display.flip()
        clock.tick(15)
    menu()

menu()