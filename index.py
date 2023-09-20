import pygame
# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
ANCHO = 800
ALTO = 600

# Colores
AZUL = (0, 0, 255)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
MORADO = (128, 0, 128)
NARANJA = (255, 165, 0)

# Velocidades de las paletas y la pelota
VELOCIDAD_PALETAS = 10
VELOCIDAD_PELOTA = 4

# Tamaño de las paletas y la pelota
ANCHO_PALETAS = 10
ALTO_PALETAS = 60
ANCHO_PELOTA = 10
ALTO_PELOTA = 10

# Posiciones iniciales de las paletas
POSICION_PALETA_IZQUIERDA = (ANCHO_PALETAS, ALTO/2 - ALTO_PALETAS/2)
POSICION_PALETA_DERECHA = (ANCHO - ANCHO_PALETAS*2, ALTO/2 - ALTO_PALETAS/2)

# Posición inicial de la pelota
POSICION_PELOTA = (ANCHO/2 - ANCHO_PELOTA/2, ALTO/2 - ALTO_PELOTA/2)

# Puntuaciones iniciales
puntuacion_izquierda = 0
puntuacion_derecha = 0
puntuacion_jugador = 0
puntuacion_maquina = 0

# Variables para el movimiento continuo de las paletas
mover_paleta_izquierda_arriba = False
mover_paleta_izquierda_abajo = False
mover_paleta_derecha_arriba = False
mover_paleta_derecha_abajo = False

# Crear la pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Ping Pong")

# Función para mostrar el contador en pantalla
def mostrar_contador():
    fuente = pygame.font.Font(None, 50)
    texto = fuente.render(f"{puntuacion_izquierda} - {puntuacion_derecha}", True, BLANCO)
    pantalla.blit(texto, (ANCHO/2 - texto.get_width()/2, 20))
def mostrar_mensaje_modjuego():
    fuente = pygame.font.Font(None, 60)
    texto = fuente.render("Selecciona el número de jugadores", True, BLANCO)
    pantalla.blit(texto, (ANCHO/2 - texto.get_width()/2, ALTO/5 - texto.get_height()/5))
# Función para mostrar mensaje de victoria
def mostrar_mensaje_victoria():
    fuente = pygame.font.Font(None, 60)
    texto = fuente.render("¡Has ganado!", True, BLANCO)
    pantalla.blit(texto, (ANCHO/2 - texto.get_width()/2, ALTO/2 - texto.get_height()/2))

# Función para mostrar mensaje de derrota
def mostrar_mensaje_derrota():
    fuente = pygame.font.Font(None, 60)
    texto = fuente.render("¡Has perdido!", True, BLANCO)
    pantalla.blit(texto, (ANCHO/2 - texto.get_width()/2, ALTO/2 - texto.get_height()/2))

# Clase para crear las paletas
class Paleta:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, ANCHO_PALETAS, ALTO_PALETAS)
        self.color = MORADO

    def dibujar(self):
        pygame.draw.rect(pantalla, self.color, self.rect)

    def mover_arriba(self):
        if self.rect.y > 0:
            self.rect.y -= VELOCIDAD_PALETAS

    def mover_abajo(self):
        if self.rect.y < ALTO - ALTO_PALETAS:
            self.rect.y += VELOCIDAD_PALETAS

    def seguir_pelota(self, pelota):
        if self.rect.centery < pelota.rect.centery:
            self.mover_abajo()
        elif self.rect.centery > pelota.rect.centery:
            self.mover_arriba()

# Clase para crear la pelota
class Pelota:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, ANCHO_PELOTA, ALTO_PELOTA)
        self.color = NARANJA
        self.velocidad_x = VELOCIDAD_PELOTA
        self.velocidad_y = VELOCIDAD_PELOTA

    def dibujar(self):
        pygame.draw.rect(pantalla, self.color, self.rect)

    def mover(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

        # Rebotar la pelota en los bordes superior e inferior
        if self.rect.y <= 0 or self.rect.y >= ALTO - ALTO_PELOTA:
            self.velocidad_y *= -1

        # Rebotar la pelota en las paletas
        if self.rect.colliderect(paleta_izquierda.rect) or self.rect.colliderect(paleta_derecha.rect):
            self.velocidad_x *= -1

        # Actualizar la puntuación si la pelota sale de la pantalla
        if self.rect.x <= 0:
            self.rect.x = ANCHO/2 - ANCHO_PELOTA/2
            self.rect.y = ALTO/2 - ALTO_PELOTA/2
            self.velocidad_x = VELOCIDAD_PELOTA
            self.velocidad_y = VELOCIDAD_PELOTA
            self.actualizar_puntuacion("derecha")

        elif self.rect.x >= ANCHO - ANCHO_PELOTA:
            self.rect.x = ANCHO/2 - ANCHO_PELOTA/2
            self.rect.y = ALTO/2 - ALTO_PELOTA/2
            self.velocidad_x = -VELOCIDAD_PELOTA
            self.velocidad_y = -VELOCIDAD_PELOTA
            self.actualizar_puntuacion("izquierda")

    def actualizar_puntuacion(self, lado):
        global puntuacion_izquierda, puntuacion_derecha
        if lado == "izquierda":
            puntuacion_izquierda += 1
            if puntuacion_izquierda >= 15:
                mostrar_mensaje_victoria()
        elif lado == "derecha":
            puntuacion_derecha += 1
            if puntuacion_derecha >= 15:
                mostrar_mensaje_derrota()
    
# Crear las paletas
paleta_izquierda = Paleta(*POSICION_PALETA_IZQUIERDA)
paleta_derecha = Paleta(*POSICION_PALETA_DERECHA)

# Crear la pelota
pelota = Pelota(*POSICION_PELOTA)

# Botones "Un jugador" y "Dos jugadores"
class Boton:
    def __init__(self, x, y, ancho, alto, color, texto, tamaño_texto, accion):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color = color
        self.texto = texto
        self.tamaño_texto = tamaño_texto
        self.accion = accion

    def dibujar(self):
        pygame.draw.rect(pantalla, self.color, self.rect, border_radius=10)
        mostrar_texto(self.texto, self.tamaño_texto, self.rect.x + 10, self.rect.y + 10)

    def verificar_clic(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.accion()

# Acción para el botón "Un jugador"
def accion_un_jugador():
    global paleta_izquierda, paleta_derecha, pelota, puntuacion_izquierda, puntuacion_derecha
    paleta_izquierda = Paleta(*POSICION_PALETA_IZQUIERDA)
    paleta_derecha = Paleta(*POSICION_PALETA_DERECHA)
    pelota = Pelota(*POSICION_PELOTA)
    puntuacion_izquierda = 0
    puntuacion_derecha = 0
    un_jugador = True
    while un_jugador:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                un_jugador = False
            # Verificar el clic en los botones
            boton_un_jugador.verificar_clic(event)
            boton_dos_jugadores.verificar_clic(event)
            # Manejar eventos de teclado
            manejar_eventos_teclado(event)
        # Movimiento de la paleta de la máquina siguiendo la pelota
        paleta_derecha.seguir_pelota(pelota)
        # Mover las paletas (solo si se selecciona "Dos jugadores")
        if un_jugador:
            if mover_paleta_izquierda_arriba:
                paleta_izquierda.mover_arriba()
            elif mover_paleta_izquierda_abajo:
                paleta_izquierda.mover_abajo()
        # Rellenar la pantalla con color azul
        pantalla.fill(AZUL)
        # Dibujar las paletas y la pelota
        paleta_izquierda.dibujar()
        paleta_derecha.dibujar()
        pelota.dibujar()
        # Mover la pelota
        pelota.mover()
        # Mostrar el contador en pantalla
        mostrar_contador()
        # Actualizar la pantalla
        pygame.display.flip()
        # Limitar la velocidad de fotogramas
        pygame.time.Clock().tick(70)
        # Finalizar el juego si se alcanza la puntuación máxima
        if puntuacion_izquierda >= 15 or puntuacion_derecha >= 15:
            mostrar_mensaje_derrota()
            mostrar_mensaje_victoria()
            un_jugador = False
# Acción para el botón "Dos jugadores"
def accion_dos_jugadores():
    global paleta_izquierda, paleta_derecha, pelota, puntuacion_izquierda, puntuacion_derecha

    paleta_izquierda = Paleta(*POSICION_PALETA_IZQUIERDA)
    paleta_derecha = Paleta(*POSICION_PALETA_DERECHA)
    pelota = Pelota(*POSICION_PELOTA)
    puntuacion_izquierda = 0
    puntuacion_derecha = 0

    # Bucle del juego para dos jugadores
    dos_jugadores = True
    while dos_jugadores:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                dos_jugadores = False

            # Verificar el clic en los botones
            boton_un_jugador.verificar_clic(event)
            boton_dos_jugadores.verificar_clic(event)

            # Manejar eventos de teclado
            manejar_eventos_teclado(event)

        # Rellenar la pantalla con color azul
        pantalla.fill(AZUL)

        # Dibujar las paletas y la pelota
        paleta_izquierda.dibujar()
        paleta_derecha.dibujar()
        pelota.dibujar()

        # Mover las paletas (solo si se selecciona "Dos jugadores")
        if dos_jugadores:
            if mover_paleta_izquierda_arriba:
                paleta_izquierda.mover_arriba()
            elif mover_paleta_izquierda_abajo:
                paleta_izquierda.mover_abajo()
            if mover_paleta_derecha_arriba:
                paleta_derecha.mover_arriba()
            elif mover_paleta_derecha_abajo:
                paleta_derecha.mover_abajo()

        # Mover la pelota
        pelota.mover()

        # Mostrar el contador en pantalla
        mostrar_contador()

        # Actualizar la pantalla
        pygame.display.flip()

        # Limitar la velocidad de fotogramas
        pygame.time.Clock().tick(60)

        # Finalizar el juego si se alcanza la puntuación máxima
        if puntuacion_izquierda >= 15 or puntuacion_derecha >= 15:
            dos_jugadores = False

# Crear los botones "Un jugador" y "Dos jugadores"
boton_un_jugador = Boton(ANCHO/2 - 100, ALTO/2, 200, 50, BLANCO, "Un jugador", 30, accion_un_jugador)
boton_dos_jugadores = Boton(ANCHO/2 - 100, ALTO/2 + 70, 200, 50, BLANCO, "Dos jugadores", 30, accion_dos_jugadores)

# Función para mostrar el texto en pantalla
def mostrar_texto(texto, tamaño, x, y):
    fuente = pygame.font.Font(None, tamaño)
    superficie_texto = fuente.render(texto, True, NEGRO)
    pantalla.blit(superficie_texto, (x, y))

# Función para manejar los eventos de teclado en ambos modos de juego
def manejar_eventos_teclado(event):
    global mover_paleta_izquierda_arriba, mover_paleta_izquierda_abajo, mover_paleta_derecha_arriba, mover_paleta_derecha_abajo
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_w:
            mover_paleta_izquierda_arriba = True
        elif event.key == pygame.K_s:
            mover_paleta_izquierda_abajo = True
        elif event.key == pygame.K_UP:
            mover_paleta_derecha_arriba = True
        elif event.key == pygame.K_DOWN:
            mover_paleta_derecha_abajo = True
    elif event.type == pygame.KEYUP:
        if event.key == pygame.K_w:
            mover_paleta_izquierda_arriba = False
        elif event.key == pygame.K_s:
            mover_paleta_izquierda_abajo = False
        elif event.key == pygame.K_UP:
            mover_paleta_derecha_arriba = False
        elif event.key == pygame.K_DOWN:
            mover_paleta_derecha_abajo = False
            
# Bucle principal del juego
ejecutando = True
dos_jugadores = False
while ejecutando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecutando = False

        # Verificar el clic en los botones
        boton_un_jugador.verificar_clic(event)
        boton_dos_jugadores.verificar_clic(event)

        # Manejar eventos de teclado
        manejar_eventos_teclado(event)

    # Rellenar la pantalla con color azul
    pantalla.fill(AZUL)

    # Dibujar los botones
    mostrar_mensaje_modjuego()
    boton_un_jugador.dibujar()
    boton_dos_jugadores.dibujar()

    # Actualizar la pantalla
    pygame.display.flip()

# Cerrar Pygame al salir del juego
pygame.quit()
