import sys, pygame
pygame.init()

RED = (255,0,0)
RECT_WIDTH = 23
RECT_HEIGHT = 15
BLACK = 0, 0, 0
SCREEN = pygame.display.set_mode([800, 600])
top = 1

class Rect(pygame.sprite.Sprite):
  def __init__(self, x, y, color):
    super(Rect, self).__init__()
    self.image = pygame.Surface([RECT_WIDTH, RECT_HEIGHT])
    self.image.fill(color)
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y

class Ball(pygame.sprite.Sprite):
  def __init__(self, x, y, color):


rects = pygame.sprite.Group()

for row in range(15):
  for column in range(32):
    rect = Rect(column * (RECT_WIDTH + 2) + 1, top, RED)
    rects.add(rect)
  top += RECT_HEIGHT + 2



def main():

  while 1:
    for event in pygame.event.get():
      if event.type == pygame.QUIT: sys.exit()

    SCREEN.fill(BLACK)
    rects.draw(SCREEN)
    pygame.display.flip()

main()