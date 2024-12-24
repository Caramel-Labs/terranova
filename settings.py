"""Configurations for the PyGame simulation.
"""

# Dimensions of the grid
WIDTH = 20
HEIGHT = 20

# Size of a single cell
CELL_SIZE = 48

# Initial count of zombies and humans when starting the simulation
INITIAL_ZOMBIES = 5
INITIAL_HUMANS = 20

# Number of iterations to run the simulation
STEPS = 100

# Colors for rendering
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HUMAN_COLOR = (0, 128, 255)  # For general human-like entities
ZOMBIE_COLOR = (255, 0, 0)  # For zombies in the other simulation
FARMER_COLOR = (0, 204, 0)  # Green for farmers (associated with agriculture)
MINER_COLOR = (128, 64, 0)  # Brown for miners (associated with earth/ore)
ENGINEER_COLOR = (0, 0, 255)  # Blue for engineers (associated with technology)
LIFEPOD_COLOR = (192, 192, 192)  # Silver/gray for lifepods
GREENHOUSE_COLOR = (0, 255, 0)  # Bright green for greenhouses
DRILL_COLOR = (255, 165, 0)  # Orange for drills


# Image asset paths
BACKGROUND_IMAGE_PATH = "./assets/blackbg.jpg"
HUMAN_IMAGE_PATH = "./assets/human.png"
ZOMBIE_IMAGE_PATH = "./assets/zombie.png"
