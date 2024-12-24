import pygame
from model import ZombieApocalypse
from settings import WIDTH, HEIGHT, CELL_SIZE
from settings import INITIAL_ZOMBIES, INITIAL_HUMANS, STEPS
from settings import WHITE, BLACK, HUMAN_COLOR, ZOMBIE_COLOR
from settings import BACKGROUND_IMAGE_PATH, HUMAN_IMAGE_PATH, ZOMBIE_IMAGE_PATH


def visualize_simulation():
    # Initialize PyGame
    pygame.init()

    cell_size = CELL_SIZE
    screen_width = WIDTH * cell_size
    screen_height = HEIGHT * cell_size

    # Initialize the display surface
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Zombie Apocalypse Simulation")

    # Load the background texture
    background_texture = pygame.image.load(BACKGROUND_IMAGE_PATH)
    background_texture = pygame.transform.scale(
        background_texture, (cell_size, cell_size)
    )

    # Load images for zombies and humans
    zombie_image = pygame.image.load(ZOMBIE_IMAGE_PATH)
    human_image = pygame.image.load(HUMAN_IMAGE_PATH)
    zombie_image = pygame.transform.scale(zombie_image, (cell_size, cell_size))
    human_image = pygame.transform.scale(human_image, (cell_size, cell_size))

    # Set the clock object for timing and framerate management
    clock = pygame.time.Clock()

    # Initialize the simulation model
    model = ZombieApocalypse(
        width=WIDTH,
        height=HEIGHT,
        initial_zombies=INITIAL_ZOMBIES,
        initial_humans=INITIAL_HUMANS,
    )

    # Main game loop
    running = True
    step_count = 0
    while running and step_count < STEPS:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Take a simulation step
        model.step()
        step_count += 1

        # Draw the tiled background
        for y in range(0, screen_height, cell_size):
            for x in range(0, screen_width, cell_size):
                screen.blit(background_texture, (x, y))

        # Draw the grid and agents
        for contents, (x, y) in model.grid.coord_iter():
            if contents:
                for agent in contents:
                    # Determine the appropriate image for the agent
                    if type(agent).__name__ == "HumanAgent":
                        screen.blit(human_image, (x * cell_size, y * cell_size))
                    elif type(agent).__name__ == "ZombieAgent":
                        screen.blit(zombie_image, (x * cell_size, y * cell_size))

        # Update the display
        pygame.display.flip()

        # Wait for 1 second before the next step
        clock.tick(1)

    # Quit PyGame when done
    pygame.quit()


def main():
    visualize_simulation()


if __name__ == "__main__":
    main()
