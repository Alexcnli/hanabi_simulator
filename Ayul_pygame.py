import pygame

#Global Variable
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 1600
FPS = 60
WHITE = (255,255,255)

CARD_WIDTH = 81
CARD_HEIGHT = 232

CARD_INDEX_LIST = {1:(0,0,81,232)}

#Game initiation
pygame.init()
pygame.display.set_caption("Hanabi in Pygame")
screen = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
clock = pygame.time.Clock()

card_image = pygame.image.load('cardlist.png').convert_alpha()

def get_card_image(sheet, card_index):
    image = pygame.Surface((81, 232)).convert_alpha()
    image.blit(sheet, (0,0), CARD_INDEX_LIST[card_index])
    return image

frame = get_card_image(card_image, 1)

# class Card(pygame.sprite.Sprite):
#     def __init__(self):
#         pygame.sprite.Sprite.__init__(self)
#         self.image = pygame.Surface((40,40))
#         self.image.fill((0,255,0))
#         self.rect = self.image.get_rect()
#         self.rect.center = (WINDOW_HEIGHT/2, WINDOW_WIDTH/2)
    
#     def update(self):
#         key = pygame.key.get_pressed()
#         if pygame.mouse.get_pressed():
#             self.rect.move(2,0)
#         if key[pygame.K_a]:
#             self.rect.move(2,0)

# all_aprites = pygame.sprite.Group()
# card = Card()
# all_aprites.add(card)

running = True

while running:
    clock.tick(FPS)

    screen.fill(WHITE)
    screen.blit(frame, (50,50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # all_aprites.update()
    # all_aprites.draw(screen)

    pygame.display.update()

pygame.quit()
