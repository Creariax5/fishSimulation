import math

import pygame
from bob import Bob
from map import Map
from food import Food
from shark import Shark
from toggleButton import ToggleButton

# pygame setup
width, height = 2400, 2000

pygame.init()
screen = pygame.display.set_mode((1200, 1000))
clock = pygame.time.Clock()
running = True
dt = 0

show_buttons = ToggleButton(20, 20, 60, 20, 'show GUI')
show_buttons.clicked()

show_direction = ToggleButton(20, 50, 80, 20, 'show direction')

chunk_size = 40
map = Map(width, height, chunk_size=chunk_size)

bobs = []
for i in range(400):
    my_bob = Bob(map, distance_de_vue=chunk_size)
    bobs.append(my_bob)
    map.assign_bob_to_grid(my_bob)

foods = []

shark = Shark(map, champ_de_vision=300, distance_de_vue=chunk_size * 3)

i = 0


def handle_direction(state, bobs, shark):
    shark.show_direction = state
    for bob in bobs:
        bob.show_direction = state


while running:
    i += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        show_buttons.handle_event(event)
        state = show_direction.handle_event(event)
        if state is not None:
            handle_direction(state, bobs, shark)

    # interactions
    if i % 60 == 0:
        foods.append(Food(map))

    for bob in bobs:
        bob.manage_bob(map, foods, bobs, shark)

    shark.manage(map, bobs)

    # grid refresh
    map.grid = map.create_grid()
    for bob in bobs:
        map.assign_bob_to_grid(bob)
    for food in foods:
        map.assign_bob_to_grid(food)

    # render
    screen.fill("black")
    map.draw(screen)

    for food in foods:
        food.draw(screen)

    for bob in bobs:
        bob.draw(screen, map, dt)

    shark.draw(screen, map, dt)
    # Draw buttons
    show_buttons.draw(screen)
    if show_buttons.active:
        show_direction.draw(screen)

    pygame.display.flip()
    dt = clock.tick(60) / 1000
    pygame.display.set_caption("fps: " + str(round(clock.get_fps())) + "    bobs: " + str(len(bobs)))

pygame.quit()
