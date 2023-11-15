# Importar los librerias necesarios
import pygame, random, sys
# Definir constantes para la resolución de la pantalla y colores
WIDTH = 800 # Ancho
HEIGHT = 600 # Alto
BLACK = (0, 0, 0)  # Color negro en formato RGB
GREEN = (0, 255, 0)    # Color verde en formato RGB
WHITE = (255, 255, 255)  # Color blanco en formato RGB
RED = (255, 0, 0)   # Color rojo en formato RGB
BLUE = (0, 0, 255)   # Color celeste en formato RGB
# Inicializar Pygame y configurar la pantalla (RINA)
pygame.init()  # Inicializa Pygame
pygame.mixer.init()  # Inicializa el mezclador de sonido de Pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Configura la pantalla con las dimensiones WIDTH y HEIGHT
font = pygame.font.Font(None, 36)
pygame.display.set_caption("USB")  # Establece el título de la ventana del juego
# Carga el icono desde la ruta de tu archivo de icono
icon = pygame.image.load('assets/meteorGrey_med1.png')  # Reemplaza  con 
# Establece el icono de la ventana
pygame.display.set_icon(icon)
clock = pygame.time.Clock()  # Crea un objeto Clock para manejar el tiempo en el juego
# Definir una función para dibujar texto en la pantalla
def draw_text(surface, text, size, x, y):
    # Crea un objeto de fuente con el tipo de fuente "serif" y el tamaño dado
    font = pygame.font.SysFont("serif", size)
    # Renderiza el texto en una superficie con el color blanco (WHITE)
    text_surface = font.render(text, True, WHITE)
    # Obtiene el rectángulo que rodea el texto y lo posiciona en (x, y)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    # Dibuja la superficie de texto en la superficie especificada en las coordenadas dadas
    surface.blit(text_surface, text_rect)
# Funcion barra de progreso de la vida (MANUEL)
def draw_shield_bar(surface, x, y, percentage):
    # Definición de constantes para la barra de progreso
    BAR_LENGTH = 160  # Aumento en la longitud de la barra
    BAR_HEIGHT = 20   # Aumento en la altura de la barra
    TEXT_FONT = pygame.font.Font(None, 20)  # Fuente para el texto
    # Calcula la longitud de la barra de relleno basada en el porcentaje proporcionado
    fill = (percentage / 100) * BAR_LENGTH
    # Determina el color de la barra según el porcentaje
    if percentage > 50:
        bar_color = GREEN
    elif percentage >= 30:
        bar_color = BLUE
    else:
        bar_color = RED
    # Crea un rectángulo que representa el borde de la barra de progreso
    border = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    # Crea un rectángulo que representa la parte rellena de la barra de progreso
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    # Dibuja el relleno de la barra de progreso en la superficie dada (surface)
    pygame.draw.rect(surface, bar_color, fill_rect)
    # Dibuja el borde de la barra de progreso en la superficie dada (surface), con un ancho de línea de 2 píxeles
    pygame.draw.rect(surface, WHITE, border, 2)
    # Crea un objeto de texto con la palabra "semestre"
    text = TEXT_FONT.render("Semestre", True, BLACK)
    # Obtén las dimensiones del texto
    text_rect = text.get_rect()
    # Coloca el texto en el centro de la barra de progreso
    text_rect.center = (x + BAR_LENGTH // 2, y + BAR_HEIGHT // 2)
    # Dibuja el texto en la superficie
    surface.blit(text, text_rect)

# Jugador nave (EDSON)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Cargar la imagen del jugador desde el archivo "player.png"
        self.image = pygame.image.load("assets/player.png").convert()
        # Configurar el color transparente para la imagen (en este caso, el color negro)
        self.image.set_colorkey(BLACK)
        # Obtener el rectángulo que rodea al jugador y establecer su posición inicial
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        # Velocidad horizontal inicial del jugador
        self.speed_x = 0
        # Puntaje de escudo del jugador
        self.shield = 100
    # Función de actualización del jugador
    def update(self):
        # Restablecer la velocidad horizontal del jugador a cero
        self.speed_x = 0
        # Obtener el estado de las teclas presionadas
        keystate = pygame.key.get_pressed()
        # Actualizar la velocidad horizontal según las teclas presionadas
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        # Mover el jugador horizontalmente
        self.rect.x += self.speed_x
        # Limitar la posición del jugador dentro de la pantalla
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    # Función para realizar disparos
    def shoot(self):
        # Crear una instancia de la clase Bullet en la posición del jugador
        bullet = Bullet(self.rect.centerx, self.rect.top)
        # Agregar la bala a los grupos de sprites
        all_sprites.add(bullet)
        bullets.add(bullet)
        # Reproducir el sonido del disparo
        laser_sound.play()
# Meteoritos (JOEL)
class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        # Llamamos al constructor de la clase base (Sprite)
        super().__init__()
        # Elegimos una imagen de meteorito al azar de la lista 'meteor_images'
        self.image = random.choice(meteor_images)
        # Configuramos el color transparente de la imagen como negro (BLACK)
        self.image.set_colorkey(BLACK)
        # Obtenemos el rectángulo (área rectangular que ocupa el sprite) de la imagen
        self.rect = self.image.get_rect()
        # Colocamos el meteorito en una posición aleatoria en la parte superior de la pantalla
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-140, -100)
        # Asignamos velocidades aleatorias en los ejes x e y para simular el movimiento
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-5, 5)
    def update(self):
        # Actualizamos la posición del meteorito basado en sus velocidades
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        # Verificamos si el meteorito ha salido de la pantalla
        if self.rect.top > HEIGHT + 10 or self.rect.left < -40 or self.rect.right > WIDTH + 40:
            # Si el meteorito está fuera de la pantalla, lo volvemos a colocar en la parte superior
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-140, - 100)
            # Asignamos nuevas velocidades aleatorias para un movimiento variado
            self.speedy = random.randrange(1, 10)
# Disparos (MAURICIO)
class Bullet(pygame.sprite.Sprite):
    # Inicialización de la clase Bullet
    def __init__(self, x, y):
        # Llama al constructor de la clase base (pygame.sprite.Sprite)
        super().__init__()
        # Carga la imagen del proyectil desde el archivo "assets/laser1.png"
        self.image = pygame.image.load("assets/laser1.png")
        # Establece el color transparente (colorkey) de la imagen como negro (BLACK)
        self.image.set_colorkey(BLACK)
        # Obtiene el rectángulo que rodea la imagen y establece su posición inicial
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        # Establece la velocidad vertical del proyectil (hacia arriba en este caso)
        self.speedy = -10
    # Método para actualizar la posición del proyectil en cada fotograma
    def update(self):
        # Desplaza el rectángulo del proyectil en la dirección y velocidad especificadas
        self.rect.y += self.speedy
        # Si el proyectil se mueve fuera de la pantalla hacia arriba, se elimina
        if self.rect.bottom < 0:
            self.kill()
# Explosiones (ADAMS)
class Explosion(pygame.sprite.Sprite):
    # Constructor de la clase
    def __init__(self, center):
        super().__init__()
        # Configura la imagen de la explosión con el primer frame
        self.image = explosion_anim[0]
        # Obtiene el rectángulo que rodea la imagen y lo centra en el punto especificado
        self.rect = self.image.get_rect()
        self.rect.center = center
        # Inicializa el índice del frame actual, el tiempo del último update y la velocidad de la explosión
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50  # VELOCIDAD DE LA EXPLOSION
    # Método para actualizar la animación de la explosión
    def update(self):
        # Obtiene el tiempo actual
        now = pygame.time.get_ticks()
        # Comprueba si ha pasado el tiempo suficiente para cambiar de frame
        if now - self.last_update > self.frame_rate:
            # Actualiza el tiempo del último update
            self.last_update = now
            # Incrementa el índice del frame
            self.frame += 1
            # Comprueba si ha llegado al final de la animación
            if self.frame == len(explosion_anim):
                # Si es el último frame, elimina la explosión
                self.kill()
            else:
                # Si no es el último frame, actualiza la imagen y el rectángulo
                center = self.rect.center
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
# Pantalla de inicio (GABRIEL)
def show_go_screen():
    # Inicializamos la posición vertical del fondo
    bg_y = 0
    # Variable que indica si estamos esperando una acción del jugador
    waiting = True
    # Bucle principal de la pantalla de inicio
    while waiting:
        # Manejamos los eventos de pygame
        for event in pygame.event.get():
            # Si el evento es cerrar la ventana, salimos del juego
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Si el evento es soltar una tecla, dejamos de esperar
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    waiting = False
        # Movemos el fondo hacia abajo
        bg_y += 1
        # Si el fondo ha pasado la altura de la pantalla, lo reiniciamos
        if bg_y > HEIGHT:
            bg_y = 0
        # Mostramos el fondo en dos posiciones para crear un efecto de movimiento
        screen.blit(background, (0, bg_y - HEIGHT))
        screen.blit(background, (0, bg_y))
        # Mostramos varios textos en la pantalla de inicio
        draw_text(screen, "U. SALESIANA", 65, WIDTH // 2, HEIGHT // 4)
        draw_text(screen, "Ingenieria de Sistemas", 27, WIDTH // 2, HEIGHT // 2)
        draw_text(screen, "InnoCoders", 40, WIDTH // 2, HEIGHT // 2 + 40)
        draw_text(screen, "Enter Para Jugar", 20, WIDTH // 2, HEIGHT * 3/4)
        draw_text(screen, "Tecla \"P\" para pausar", 20, WIDTH // 2, HEIGHT * 3/4 + 40)
        # Actualizamos la pantalla
        pygame.display.flip()
        # Establecemos el límite de fotogramas por segundo a 60
        clock.tick(60)

# Lista para almacenar imágenes de meteoritos (SAUL)
meteor_images = []
# Lista de rutas de archivos de imágenes de meteoritos
meteor_list = ["assets/meteorGrey_big1.png", "assets/meteorGrey_big2.png", "assets/meteorGrey_big3.png", "assets/meteorGrey_big4.png",
				"assets/meteorGrey_med1.png", "assets/meteorGrey_med2.png", "assets/meteorGrey_small1.png", "assets/meteorGrey_small2.png",
				"assets/meteorGrey_tiny1.png", "assets/meteorGrey_tiny2.png"]
# Cargar cada imagen de meteorito y agregarla a la lista meteor_images
for img in meteor_list:
    meteor_images.append(pygame.image.load(img).convert())
# Lista para almacenar imágenes de explosiones
explosion_anim = []
# Cargar imágenes de explosiones y ajustarlas
for i in range(9):
    # Crear la ruta del archivo para cada imagen de explosión
    file = "assets/regularExplosion0{}.png".format(i)
    # Cargar la imagen y convertirla al formato adecuado
    img = pygame.image.load(file).convert()
    # Configurar el color transparente (color clave) de la imagen a negro (BLACK)
    img.set_colorkey(BLACK)
    # Escalar la imagen a un tamaño específico (70x70 en este caso)
    img_scale = pygame.transform.scale(img, (70, 70))
    # Agregar la imagen escalada a la lista explosion_anim
    explosion_anim.append(img_scale)
# --EJECUCION DEL JUEGO-- (ALEX)
# Cargar imagen de fondo
backgroundGame = pygame.image.load("assets/backgroundGame.png").convert()
background = pygame.image.load("assets/background.png").convert()
# Cargar sonidos
laser_sound = pygame.mixer.Sound("assets/laser5.ogg")
soud_explotion = pygame.mixer.Sound("assets/explosion.wav")
pygame.mixer.music.load("assets/music.ogg")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(loops=-1)  # Reproducir música en bucle
#GAME OVER
game_over = True
running = True
# Agregar una variable de estado de pausa y un mensaje
paused = False
pause_text = font.render("En pausa", True, WHITE)
while running:
    # Pantalla de inicio
    if game_over:
        show_go_screen()
        # Reiniciar el juego
        game_over = False
        all_sprites = pygame.sprite.Group()  # Grupo para todos los sprites
        meteor_list = pygame.sprite.Group()  # Grupo para meteoros
        bullets = pygame.sprite.Group()  # Grupo para balas
        player = Player()  # Crear instancia del jugador
        all_sprites.add(player)  # Agregar jugador al grupo de sprites
        for i in range(8):
            meteor = Meteor()  # Crear instancia de meteoro
            all_sprites.add(meteor)  # Agregar meteoro al grupo de sprites
            meteor_list.add(meteor)  # Agregar meteoro al grupo de meteoros
        score = 0
    clock.tick(60)  # Limitar el juego a 60 fotogramas por segundo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Salir del bucle si se cierra la ventana
        # Disparar al presionar la barra espaciadora
        elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
                elif event.key == pygame.K_p:  # Pausar/reanudar con la tecla 'P'
                    paused = not paused
                if paused:
                    pygame.mixer.pause()  # Pausar todos los sonidos
                else:
                    pygame.mixer.unpause()  # Reanudar todos los sonidos
    if not paused:            
        all_sprites.update()  # Actualizar todos los sprites en el grupo
        # Colisiones - Meteoro - Laser
        hits = pygame.sprite.groupcollide(meteor_list, bullets, True, True)  # Detectar colisiones
        for hit in hits:
            score += 10  # Incrementar puntaje por cada meteoro destruido
            # Reproducir sonido de explosión
            soud_explotion.play()
            soud_explotion.set_volume(0.2)
            explosion = Explosion(hit.rect.center)  # Crear instancia de explosión
            all_sprites.add(explosion)  # Agregar explosión al grupo de sprites
            meteor = Meteor()  # Crear nuevo meteoro
            all_sprites.add(meteor)  # Agregar nuevo meteoro al grupo de sprites
            meteor_list.add(meteor)  # Agregar nuevo meteoro al grupo de meteoros
        # Checar colisiones - Jugador - Meteoro
        hits = pygame.sprite.spritecollide(player, meteor_list, True)  # Detectar colisiones
        for hit in hits:
            player.shield -= 5  # Reducir el escudo del jugador por colisión
            meteor = Meteor()  # Crear nuevo meteoro
            all_sprites.add(meteor)  # Agregar nuevo meteoro al grupo de sprites
            meteor_list.add(meteor)  # Agregar nuevo meteoro al grupo de meteoros
            if player.shield <= 0:
                game_over = True  # Establecer game_over en True si el escudo es <= 0
        screen.blit(backgroundGame, [0, 0])  # Dibujar la imagen de fondo en la pantalla
        all_sprites.draw(screen)  # Dibujar todos los sprites en la pantalla
        # Marcador
        draw_text(screen, str(score), 25, WIDTH // 2, 10)  # Función para dibujar texto
        # Barra de escudo.
        draw_shield_bar(screen, 5, 5, player.shield)  # Función para dibujar la barra de escudo
    else:
        # Si el juego está en pausa, mostrar el mensaje en el centro de la pantalla
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - pause_text.get_height() // 2))
    pygame.display.flip()  # Actualizar la pantalla
pygame.quit()  # Salir del juego cuando se cierra la ventana