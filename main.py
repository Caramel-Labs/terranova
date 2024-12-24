import pygame
from model import SpaceColony
from settings import STEPS, WIDTH, HEIGHT, CELL_SIZE, BLACK
from graphics import load_images, render_stats, render_agents


def initialize_space_colony():
    pygame.init()
    pygame.mixer.init()

    # Load images once
    images = load_images()

    # Initialize display
    screen = pygame.display.set_mode((WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE))
    pygame.display.set_caption("Space Colony Simulation")

    # Set up simulation model
    model = SpaceColony(width=WIDTH, height=HEIGHT)

    # Set up fonts
    font = pygame.font.Font(None, 24)
    stats_font = pygame.font.Font(None, 20)

    # Mute/unmute music functionality
    music_playing = True
    pygame.mixer.music.load("./assets/music/music.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    # Main game loop
    running = True
    step_count = 0
    while running and step_count < STEPS:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 10 <= mouse_x <= 60 and 10 <= mouse_y <= 60:
                    music_playing = not music_playing
                    if music_playing:
                        pygame.mixer.music.play(-1)
                    else:
                        pygame.mixer.music.stop()

        # Take a simulation step
        model.step()
        step_count += 1

        # Get the current simulation state
        model_data = model.datacollector.get_model_vars_dataframe()
        current_data = model_data.iloc[-1]
        is_night = current_data["Is Night"]

        # Render the grid and agents
        lifepod_positions = []
        screen.fill(BLACK)
        render_agents(screen, model, images, lifepod_positions, CELL_SIZE)

        # Render the zzz image during nighttime
        if is_night:
            for lifepod_x, lifepod_y in lifepod_positions:
                zzz_x = lifepod_x + 1
                zzz_y = lifepod_y - 1
                if 0 <= zzz_x < WIDTH and 0 <= zzz_y < HEIGHT:
                    screen.blit(images["zzz"], (zzz_x * CELL_SIZE, zzz_y * CELL_SIZE))

        # Render stats
        stats = {
            "Total Food": current_data["Total Food"],
            "Total Iron": current_data["Total Iron"],
            "Drill Health": current_data["Drill Health"],
            "Drill Fuel": current_data["Drill Fuel"],
            "Greenhouse Food": current_data["Greenhouse Food"],
            "Miner Stamina": current_data["Miner Stamina"],
            "Engineer Stamina": current_data["Engineer Stamina"],
            "Farmer Stamina": current_data["Farmer Stamina"],
            "Time": "Night" if is_night else "Day",
        }
        render_stats(screen, stats, stats_font, WIDTH * CELL_SIZE)

        # Draw the mute/unmute button
        screen.blit(images["unmute"] if music_playing else images["mute"], (10, 10))

        # Update display
        pygame.display.flip()

        pygame.time.Clock().tick(1)

    pygame.quit()


def main():
    initialize_space_colony()


if __name__ == "__main__":
    main()
