import pygame, math, sys
pygame.init()

RED = 255, 0, 0
RECT_WIDTH = 23
RECT_HEIGHT = 15
BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREEN = 0, 80, 40
BRIGHT_GREEN = 0, 90, 40
RED = 180, 0, 0
BRIGHT_RED = 200, 0, 0 
SCREEN = pygame.display.set_mode([800, 600])
SPEED = 6
top = 25
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

class Rect(pygame.sprite.Sprite):
  """ This class is the boxes that need to be destroyed in order to win """
  def __init__(self, x, y, color):
    super(Rect, self).__init__()
    self.image = pygame.Surface([RECT_WIDTH, RECT_HEIGHT])
    self.image.fill(color)
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y


class Ball(pygame.sprite.Sprite):
  """ This class is the ball that breaks rectangles and bounces off the player class """
  def __init__(self):
    super(Ball, self).__init__()
    self.width, self.height = 15, 15
    self.image = pygame.Surface([self.width, self.height])
    self.rect = self.image.get_rect()
    self.image.fill(WHITE)
    self.screen_width = pygame.display.get_surface().get_width()
    self.screen_height = pygame.display.get_surface().get_height()
    self.x = self.screen_width / 2 - 15 / 2
    self.y = self.screen_height - 47
    self.speed = 6
    self.direction = 0

  def bounce(self, diff):
    """ This function will bounce the ball
        off a horizontal surface (not a vertical one) """

    self.direction = (180 - self.direction) % 360
    self.direction -= diff

  def update(self):
    # Determine speed and direction of ball movement
    direction_radians = math.radians(self.direction)
    self.x += self.speed * math.sin(direction_radians)
    self.y -= self.speed * math.cos(direction_radians)

    # Move the image to where our x and y are
    self.rect.x = self.x
    self.rect.y = self.y

    # Do we bounce off the top of the screen?
    if self.y <= 0:
      self.bounce(0)
      self.y = 1

    # Do we bounce off the left of the screen?
    if self.x <= 0:
      self.direction = (360 - self.direction) % 360
      self.x = 1

    # Do we bounce of the right side of the screen?
    if self.x > self.screen_width - self.width:
      self.direction = (360 - self.direction) % 360
      self.x = self.screen_width - self.width - 1

class Player(pygame.sprite.Sprite):
  """ This class is the bar at the bottom of the screen that the player controls """
  def __init__(self):
    super(Player, self).__init__()
    self.height = 10
    self.width = 100
    self.image = pygame.Surface([self.width, self.height])
    self.image.fill(WHITE)
    self.rect = self.image.get_rect()
    self.screen_width = pygame.display.get_surface().get_width()
    self.screen_height = pygame.display.get_surface().get_height()
    self.rect.x = (self.screen_width / 2) - 50
    self.rect.y = self.screen_height - 30

  def update(self):
    if pygame.key.get_pressed()[pygame.K_LEFT] and self.rect.x != 0:
      self.rect.x -= SPEED
    if pygame.key.get_pressed()[pygame.K_RIGHT] and self.rect.x != 800 - self.width:
      self.rect.x += SPEED


def text_objects(msg, font):
  """ Render given text onto the screen """
  text = font.render(msg, True, WHITE)
  
  return text, text.get_rect()

def button(msg, x, y, w, h, ic, ac, action=None):
  """ Render start/quit buttons that detect click and fire a given action """
  mouse = pygame.mouse.get_pos()
  click = pygame.mouse.get_pressed()

  if ((x + w > mouse[0] > x) and (y + h > mouse[1] > y)):
    pygame.draw.rect(SCREEN, ac, (x, y, w, h))

    if click[0] == 1 and action != None:
      action()
  else:
    pygame.draw.rect(SCREEN, ic, (x, y, w, h))

  sm_text = pygame.font.Font(None, 30)
  textSurf, textRect = text_objects(msg, sm_text)
  textRect.center = ((x + (w / 2)), (y + (h / 2)))

  SCREEN.blit(textSurf, textRect)


def game_intro():
  intro = True

  # first render the intro screen
  while intro:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()

    # renders title and start/quit buttons
    SCREEN.fill(BLACK)
    large_text = pygame.font.Font(None, 100)
    text = large_text.render("Brick Breaker", True, WHITE)
    text_width, text_height = large_text.size('Brick Breaker')
    text_pos = [(400 - text_width/2), (300 - text_height)]
    SCREEN.blit(text, text_pos)

    mouse = pygame.mouse.get_pos()

    button("Start", 270, 370, 120, 40, GREEN,  BRIGHT_GREEN, game_loop)
    button("Quit", 420, 370, 120, 40, RED,  BRIGHT_RED, quit)

    pygame.display.update()
    clock.tick(15)

# If game is over render "Game Over"
def game_end(score):
  global font
  game_over = True

  SCREEN.fill(BLACK)

  while game_over:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()

    global RUNNING
    RUNNING = False

    text = font.render("Game Over!", True, WHITE)
    text_pos = text.get_rect(centerx=800/2)
    text_pos.top = 300
    SCREEN.blit(text, text_pos)

    score_text = font.render("Score: {0}".format(score), True, WHITE)
    score_pos = [1, 1]
    SCREEN.blit(score_text, score_pos)

    button("Start", 270, 370, 120, 40, GREEN,  BRIGHT_GREEN, game_loop)
    button("Quit", 420, 370, 120, 40, RED,  BRIGHT_RED, quit)

    pygame.display.update()
    clock.tick(15)

def game_loop():
  global top, font
  game_over = False
  score = 0

  RUNNING, PAUSE = True, False
  state = RUNNING

  # Sprite group for rectangles
  rects = pygame.sprite.Group()

  # Initialize player
  player = Player()

  # Initialize ball
  balls = pygame.sprite.Group()
  ball = Ball()
  balls.add(ball)

  # Group to render all sprites
  allsprites = pygame.sprite.Group()
  allsprites.add(player)
  allsprites.add(ball)

  # Create the rectangles to be rendered
  for row in range(16):
    for column in range(32):
      rect = Rect(column * (RECT_WIDTH + 2) + 1, top, RED)
      rects.add(rect)
      allsprites.add(rect)
    top += RECT_HEIGHT + 2

  pause_text = font.render("Paused", True, WHITE)

  while not game_over:
    SCREEN.fill(BLACK)

    for event in pygame.event.get():
      if event.type == pygame.QUIT: sys.exit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_p: state = PAUSE
        if event.key == pygame.K_s: state = RUNNING

    # While game isn't over update player and ball position
    if state == RUNNING:
      ball.update()
      player.update()
    elif state == PAUSE:
      SCREEN.blit(pause_text, (350, 300))

    # If ball collides with player change the direction, takes into account left and right sides for diagonal movement
    if pygame.sprite.spritecollide(player, balls, False):
      diff = (player.rect.x + player.width / 2) - (ball.rect.x + ball.width / 2)
      ball.bounce(diff)

    # Add rects that ball collides with to new group
    dead_rects = pygame.sprite.spritecollide(ball, rects, True)

    # Keep moving ball as long as there are rects
    if len(dead_rects) > 0:
      ball.bounce(0)
    # End game if rects are 0 or if ball falls off bottom of screen
    if len(rects) == 0 or ball.y >= 600:
      game_over = True

    # Increase speed of ball as more rects get hit for difficulty
    for rect in dead_rects:
      ball.speed += 0.001
      score += 2

    score_text = font.render("Score: {0}".format(score), True, WHITE)
    score_pos = [1, 1]
    SCREEN.blit(score_text, score_pos)

    allsprites.draw(SCREEN)
    pygame.display.flip()
    clock.tick(60)
  
  if game_over:
    top = 25
    game_end(score)

game_intro()
game_loop()