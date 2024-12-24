"""This module is not in use right now.
"""

import pygame
from settings import CELL_SIZE, WHITE


def load_images():
    # Dictionary to store all images to avoid reloading them during the game loop
    images = {}

    # Load background images
    images["bg_day"] = pygame.transform.scale(
        pygame.image.load("./assets/mars.png"), (CELL_SIZE, CELL_SIZE)
    )
    images["bg_night"] = pygame.transform.scale(
        pygame.image.load("./assets/mars-night.jpg"), (CELL_SIZE, CELL_SIZE)
    )

    # Load structure images
    images["lifepod"] = pygame.transform.scale(
        pygame.image.load("./assets/lifepod.png"), (CELL_SIZE, CELL_SIZE)
    )
    images["drill"] = pygame.transform.scale(
        pygame.image.load("./assets/drill.png"), (CELL_SIZE, CELL_SIZE)
    )
    images["greenhouse"] = pygame.transform.scale(
        pygame.image.load("./assets/greenhouse.gif"), (CELL_SIZE, CELL_SIZE)
    )

    # Load human images
    images["engineer"] = pygame.transform.scale(
        pygame.image.load("./assets/engineer.webp"), (CELL_SIZE, CELL_SIZE)
    )
    images["farmer"] = pygame.transform.scale(
        pygame.image.load("./assets/farmer.webp"), (CELL_SIZE, CELL_SIZE)
    )
    images["miner"] = pygame.transform.scale(
        pygame.image.load("./assets/miner.webp"), (CELL_SIZE, CELL_SIZE)
    )

    # Other images
    images["zzz"] = pygame.transform.scale(
        pygame.image.load("./assets/zzz.png"), (CELL_SIZE, CELL_SIZE)
    )
    images["asteroid_strike"] = pygame.transform.scale(
        pygame.image.load("./assets/mars-red.png"), (CELL_SIZE, CELL_SIZE)
    )

    # Mute/unmute button images
    images["mute"] = pygame.transform.scale(
        pygame.image.load("./assets/buttons/mute.png"), (50, 50)
    )
    images["unmute"] = pygame.transform.scale(
        pygame.image.load("./assets/buttons/unmute.png"), (50, 50)
    )

    return images


def render_stats(screen, stats, stats_font, screen_width):
    stats_x = screen_width - 150
    stats_y = 10
    line_spacing = 20

    for i, (key, value) in enumerate(stats.items()):
        stats_text = f"{key}: {value}"
        stats_surface = stats_font.render(stats_text, True, WHITE)
        screen.blit(stats_surface, (stats_x, stats_y + i * line_spacing))


def render_agents(screen, model, images, lifepod_positions, cell_size):
    for contents, (x, y) in model.grid.coord_iter():
        # Draw background image
        bg_image = (
            images["bg_night"]
            if model.datacollector.get_model_vars_dataframe().iloc[-1]["Is Night"]
            else images["bg_day"]
        )
        screen.blit(bg_image, (x * cell_size, y * cell_size))

        # Check for agent presence and draw accordingly
        lifepod_present = any(type(agent).__name__ == "Lifepod" for agent in contents)
        if lifepod_present:
            lifepod_positions.append((x, y))

        asteroid_strike_present = any(
            type(agent).__name__ == "AsteroidStrike" for agent in contents
        )

        for agent in contents:
            agent_type = type(agent).__name__
            if agent_type == "Farmer":
                screen.blit(images["farmer"], (x * cell_size, y * cell_size))
            elif agent_type == "Miner":
                screen.blit(images["miner"], (x * cell_size, y * cell_size))
            elif agent_type == "Engineer":
                screen.blit(images["engineer"], (x * cell_size, y * cell_size))
            elif agent_type == "Greenhouse":
                screen.blit(images["greenhouse"], (x * cell_size, y * cell_size))
            elif agent_type == "Drill":
                screen.blit(images["drill"], (x * cell_size, y * cell_size))
            elif agent_type == "Lifepod":
                screen.blit(images["lifepod"], (x * cell_size, y * cell_size))
            elif agent_type == "AsteroidStrike":
                screen.blit(images["asteroid_strike"], (x * cell_size, y * cell_size))


if __name__ == "__main__":
    pass
