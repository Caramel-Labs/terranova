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

    # Load and scale the background image to fit one grid cell
    bg_image = pygame.image.load("./assets/mars.png")
    bg_image = pygame.transform.scale(bg_image, (cell_size, cell_size))

    # Set the clock object for timing and framerate management
    clock = pygame.time.Clock()

    # Initialize the simulation model
    model = SpaceColony(width=WIDTH, height=HEIGHT)

    # Set up the font for rendering text
    font = pygame.font.Font(None, 24)
    stats_font = pygame.font.Font(None, 20)

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

        # Get the current state of the model from the dataframe
        model_data = model.datacollector.get_model_vars_dataframe()
        current_data = model_data.iloc[-1]  # Get the latest row of data

        # Clear the screen
        screen.fill(BLACK)

        # Draw the grid and agents
        for contents, (x, y) in model.grid.coord_iter():
            # Draw the background image for the cell
            screen.blit(bg_image, (x * cell_size, y * cell_size))

            # Draw the agents in the cell
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

        # Render stats in the top-right corner
        stats = {
            "Total Food": current_data["Total Food"],
            "Total Iron": current_data["Total Iron"],
            "Drill Health": current_data["Drill Health"],
            "Drill Fuel": current_data["Drill Fuel"],
            "Greenhouse Food": current_data["Greenhouse Food"],
            "Miner Stamina": current_data["Miner Stamina"],
            "Engineer Stamina": current_data["Engineer Stamina"],
            "Farmer Stamina": current_data["Farmer Stamina"],
        }

        stats_x = screen_width - 150
        stats_y = 10
        line_spacing = 20

        for i, (key, value) in enumerate(stats.items()):
            stats_text = f"{key}: {value}"
            stats_surface = stats_font.render(stats_text, True, WHITE)
            screen.blit(stats_surface, (stats_x, stats_y + i * line_spacing))

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
