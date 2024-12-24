import pygame
from model import SpaceColony
from settings import WIDTH, HEIGHT, CELL_SIZE
from settings import STEPS
from settings import WHITE, BLACK, FARMER_COLOR, MINER_COLOR, ENGINEER_COLOR
from settings import LIFEPOD_COLOR, GREENHOUSE_COLOR, DRILL_COLOR


def visualize_space_colony():
    # Initialize PyGame
    pygame.init()

    cell_size = CELL_SIZE
    screen_width = WIDTH * cell_size
    screen_height = HEIGHT * cell_size

    # Initialize the display surface
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Space Colony Simulation")

    # Set the clock object for timing and framerate management
    clock = pygame.time.Clock()

    # Initialize the simulation model
    model = SpaceColony(width=WIDTH, height=HEIGHT)

    # Set up the font for rendering text
    font = pygame.font.Font(None, cell_size - 4)

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
        screen.fill(BLACK)

        # Draw the grid and agents
        for contents, (x, y) in model.grid.coord_iter():
            for agent in contents:
                # Determine the appropriate color and label for the agent
                if type(agent).__name__ == "Farmer":
                    color = FARMER_COLOR
                    label = "F"
                elif type(agent).__name__ == "Miner":
                    color = MINER_COLOR
                    label = "M"
                elif type(agent).__name__ == "Engineer":
                    color = ENGINEER_COLOR
                    label = "E"
                elif type(agent).__name__ == "Lifepod":
                    color = LIFEPOD_COLOR
                    label = "L"
                elif type(agent).__name__ == "Greenhouse":
                    color = GREENHOUSE_COLOR
                    label = "G"
                elif type(agent).__name__ == "Drill":
                    color = DRILL_COLOR
                    label = "D"
                else:
                    color = WHITE  # Default color for unknown agents
                    label = "?"

                # Draw the rectangle for the agent
                pygame.draw.rect(
                    screen,
                    color,
                    (x * cell_size, y * cell_size, cell_size, cell_size),
                )

                # Render the label and blit it onto the rectangle
                text_surface = font.render(label, True, BLACK)
                text_rect = text_surface.get_rect(
                    center=(
                        x * cell_size + cell_size // 2,
                        y * cell_size + cell_size // 2,
                    )
                )
                screen.blit(text_surface, text_rect)

        # Update the display
        pygame.display.flip()

        # Wait for 1 second before the next step
        clock.tick(1)

    # Quit PyGame when done
    pygame.quit()


def main():
    visualize_space_colony()


if __name__ == "__main__":
    main()
