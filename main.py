import pygame
from model import SpaceColony
from settings import WIDTH, HEIGHT, CELL_SIZE
from settings import STEPS
from settings import WHITE, BLACK, FARMER_COLOR, MINER_COLOR
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

    # Load and scale the day background image to fit one grid cell
    bg_day_image = pygame.image.load("./assets/mars.png")
    bg_day_image = pygame.transform.scale(bg_day_image, (cell_size, cell_size))

    # Load and scale the night background image to fit one grid cell
    bg_night_image = pygame.image.load("./assets/mars-night.jpg")
    bg_night_image = pygame.transform.scale(bg_night_image, (cell_size, cell_size))

    # Load and scale the lifepod image to fit a 1x1 grid
    lifepod_image = pygame.image.load("./assets/lifepod.png")
    lifepod_image = pygame.transform.scale(lifepod_image, (cell_size, cell_size))

    # Load and scale the drill image to fit a 1x1 grid
    drill_image = pygame.image.load("./assets/drill.png")
    drill_image = pygame.transform.scale(drill_image, (cell_size, cell_size))

    # Load and scale the greenhouse image to fit a 1x1 grid
    greenhouse_image = pygame.image.load("./assets/greenhouse.gif")
    greenhouse_image = pygame.transform.scale(greenhouse_image, (cell_size, cell_size))

    # Load and scale the engineer image to fit a 1x1 grid
    engineer_image = pygame.image.load("./assets/engineer.webp")
    engineer_image = pygame.transform.scale(engineer_image, (cell_size, cell_size))

    # Load and scale the farmer image to fit a 1x1 grid
    farmer_image = pygame.image.load("./assets/farmer.webp")
    farmer_image = pygame.transform.scale(farmer_image, (cell_size, cell_size))

    # Load and scale the miner image to fit a 1x1 grid
    miner_image = pygame.image.load("./assets/miner.webp")
    miner_image = pygame.transform.scale(miner_image, (cell_size, cell_size))

    # Load and scale the zzz image for nighttime effect
    zzz_image = pygame.image.load("./assets/zzz.png")
    zzz_image = pygame.transform.scale(zzz_image, (cell_size, cell_size))

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

        # Determine if it's night
        is_night = current_data["Is Night"]

        # Choose the appropriate background image
        bg_image = bg_night_image if is_night else bg_day_image

        # Clear the screen
        screen.fill(BLACK)

        lifepod_positions = []  # Track lifepod positions for rendering effects

        # Draw the grid and agents
        for contents, (x, y) in model.grid.coord_iter():
            # Draw the background image for the cell
            screen.blit(bg_image, (x * cell_size, y * cell_size))

            # Check if a Lifepod is present in the cell
            lifepod_present = any(
                type(agent).__name__ == "Lifepod" for agent in contents
            )
            if lifepod_present:
                lifepod_positions.append((x, y))

            # Draw the agents in the cell
            for agent in contents:
                if lifepod_present and type(agent).__name__ in [
                    "Farmer",
                    "Miner",
                    "Engineer",
                ]:
                    # Skip rendering human images if Lifepod is present
                    continue
                elif type(agent).__name__ == "Farmer":
                    # Draw the farmer image
                    screen.blit(farmer_image, (x * cell_size, y * cell_size))
                elif type(agent).__name__ == "Miner":
                    # Draw the miner image
                    screen.blit(miner_image, (x * cell_size, y * cell_size))
                elif type(agent).__name__ == "Engineer":
                    # Draw the engineer image
                    screen.blit(engineer_image, (x * cell_size, y * cell_size))
                elif type(agent).__name__ == "Greenhouse":
                    # Draw the greenhouse image
                    screen.blit(greenhouse_image, (x * cell_size, y * cell_size))
                elif type(agent).__name__ == "Drill":
                    # Draw the drill image
                    screen.blit(drill_image, (x * cell_size, y * cell_size))
                elif type(agent).__name__ == "Lifepod":
                    # Draw the lifepod image
                    screen.blit(lifepod_image, (x * cell_size, y * cell_size))

        # Render the zzz image during nighttime diagonally top-right of Lifepods
        if is_night:
            for lifepod_x, lifepod_y in lifepod_positions:
                zzz_x = lifepod_x + 1
                zzz_y = lifepod_y - 1
                if 0 <= zzz_x < WIDTH and 0 <= zzz_y < HEIGHT:
                    screen.blit(zzz_image, (zzz_x * cell_size, zzz_y * cell_size))

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
            "Is Night": "Yes" if is_night else "No",
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
