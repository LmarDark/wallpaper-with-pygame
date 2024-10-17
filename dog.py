import pygame
import ctypes
import time
import keyboard

# Definição da estrutura LASTINPUTINFO
class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint),
                ("dwTime", ctypes.c_ulong)]

# Função para obter a inatividade do mouse e do teclado
def get_idle_time():
    user32 = ctypes.windll.User32
    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    user32.GetLastInputInfo(ctypes.byref(lii))
    idle_time = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
    return idle_time / 1000.0  # Retorna em segundos

# Função principal para executar o Pygame
def run_game():
    # Inicializa o pygame
    pygame.init()

    # Configurações da janela
    width, height = 1920, 1080
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("dog.py")

    # Carrega a sprite sheet
    sprite_sheet = pygame.image.load("./dog-spinning.png").convert_alpha()

    # Configurações do sprite
    sprite_width = 128  # Largura de cada quadro na sprite sheet
    sprite_height = 128  # Altura de cada quadro na sprite sheet
    num_frames = 24  # Número total de quadros na sprite sheet

    # Extrai os quadros da sprite sheet e os armazena em uma lista
    sprite_frames = []
    for i in range(num_frames):
        frame = sprite_sheet.subsurface(pygame.Rect(i * sprite_width, 0, sprite_width, sprite_height))
        sprite_frames.append(frame)

    # Configurações de animação e posição
    sprite_index = 0
    sprite_rect = sprite_frames[0].get_rect(center=(width // 2, height // 2))
    sprite_speed = [5, 5]
    animation_speed = 5  # Número de frames antes de mudar a imagem
    frame_count = 0

    # Loop principal
    clock = pygame.time.Clock()
    running = True

    # Bloqueia as teclas ao iniciar o jogo
    valid_keys = [
        'esc', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12',
        'pause', 'insert', 'home', 'pageup', 'pagedown', 'end', 'up', 'down', 'left', 'right',
        'numlock', 'backspace', 'tab', 'q', 'w', 'a', 's', 'd', 'e', 'r', 't', 'y', 'u', 'i',
        'o', 'p', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm', 'comma', 'period',
        'slash', 'backslash', 'grave', 'space', 'windows'
    ]
    for key in valid_keys:
        keyboard.block_key(key)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Encerra a animação, mas não o programa

        # Atualiza a posição do sprite
        sprite_rect.x += sprite_speed[0]
        sprite_rect.y += sprite_speed[1]

        # Verifica colisão com as bordas e inverte a direção
        if sprite_rect.left <= 0 or sprite_rect.right >= width:
            sprite_speed[0] = -sprite_speed[0]
        if sprite_rect.top <= 0 or sprite_rect.bottom >= height:
            sprite_speed[1] = -sprite_speed[1]

        # Atualiza o índice do quadro do sprite para a animação
        frame_count += 1
        if frame_count >= animation_speed:
            frame_count = 0
            sprite_index = (sprite_index + 1) % len(sprite_frames)

        # Desenha na tela
        screen.fill("black")  # Limpa a tela
        screen.blit(sprite_frames[sprite_index], sprite_rect)  # Desenha o quadro atual do sprite
        pygame.display.flip()

        # Verifica se as teclas "Q" e "W" estão pressionadas para desbloquear e sair
        if keyboard.is_pressed('q') and keyboard.is_pressed('w'):
            running = False  # Encerra a animação, mas não o programa

        # Controla a taxa de atualização
        clock.tick(60)

    # Desbloqueia as teclas ao sair do jogo
    for key in valid_keys:
        keyboard.unblock_key(key)

    pygame.quit()  # Fecha a janela do Pygame, mas não o programa

# Tempo de espera e loop principal
idle_time_limit = 600  # 10 minutos em segundos

while True:
    idle_time = get_idle_time()
    if idle_time >= idle_time_limit:
        run_game()  # Chama a função do jogo se houver 10 minutos de inatividade
    time.sleep(1)  # Espera 1 segundo antes de verificar novamente
