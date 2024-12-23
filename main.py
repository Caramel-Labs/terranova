import pygame
from model import ZombieApocalypse
from settings import WIDTH, HEIGHT, CELL_SIZE
from settings import INITIAL_ZOMBIES, INITIAL_HUMANS, STEPS
from settings import WHITE, BLACK, HUMAN_COLOR, ZOMBIE_COLOR


def visualize_simulation():
    # Initialize PyGame
    pygame.init()

    cell_size = CELL_SIZE
    screen_width = WIDTH * cell_size
    screen_height = HEIGHT * cell_size

    # Initialize the display surface
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Zombie Apocalypse Simulation")

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

        # Clear the screen
        screen.fill(WHITE)

        # Draw the grid and agents
        for contents, (x, y) in model.grid.coord_iter():
            if contents:
                for agent in contents:
                    color = (
                        HUMAN_COLOR
                        if type(agent).__name__ == "HumanAgent"
                        else ZOMBIE_COLOR
                    )
                    pygame.draw.rect(
                        screen,
                        color,
                        pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size),
                    )

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
