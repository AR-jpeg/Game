"""The game."""

import settings
import sprites
import pygame


pygame.init()
win = pygame.display.set_mode((500, 480))
pygame.display.set_caption("First Game")

bg = pygame.image.load('images/bg.jpg')
clock = pygame.time.Clock()
score = 0


class platform:
    """All platforms."""

    def __init__(self, x, y, width=100, height=100):
        """Init the platform."""
        self.color = (255, 0, 0)
        self.height = height
        self.rect = (x, y, width, height)
        self.hitbox = self.rect
        self.temp = 0
        self.width = width
        self.x = x
        self.y = y

    def test(self, player):
        """Test collision with the player."""
        # if (self.x < (player.x + player.width)) and ((self.x + self.width) > player.x):
        if (self.y > (player.y + player.height)) and ((self.y + self.height) > player.y):
            print(f'The player is touching the platform. {self.temp}\n\n')
            self.temp += 1

    def draw(self, win):
        """Draw the platform."""
        pygame.draw.rect(win, self.color, self.rect)


def redrawGameWindow():
    """Redraw the the window."""
    win.blit(bg, (0, 0))
    text = font.render('Score: ' + str(score), 1, (0, 0, 0))
    win.blit(text, (390, 10))
    pf.draw(win)
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()


# mainloop
font = pygame.font.SysFont('oswald', 30, True)
man = sprites.player(200, 410, 64, 64)
goblin = sprites.enemy(100, 410, 64, 64, 450)
pf = platform(250, 350, 50, 50)
shootLoop = 0
bullets = []
run = True


while run:
    clock.tick(27)
    keys = pygame.key.get_pressed()

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 4:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Calculate the bullets.
    for bullet in bullets:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                if goblin.visible:
                    goblin.hit()
                    score += 1
                    bullets.pop(bullets.index(bullet))

        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
    # Calculate shooting the bullet.
    if keys[pygame.K_SPACE] and shootLoop == 0:
        if man.left:
            facing = -1
        else:
            facing = 1

        if len(bullets) < 5:
            bullets.append(sprites.projectile(round(man.x + man.width // 2),
                                              round(man.y + man.height//2), 6, (0, 0, 0), facing))

        shootLoop = 1

    man.move(keys)
    pf.test(man)
    redrawGameWindow()

pygame.quit()
