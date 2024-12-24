import mesa
from mesa import Agent, Model
from mesa.space import MultiGrid
from legacy_agents import HumanAgent, ZombieAgent
from mesa.datacollection import DataCollector
from agents.humans import Engineer, Farmer, Miner
from agents.structures import Lifepod, Greenhouse, Drill


class SpaceColony(Model):
    """The goddamn model"""

    def __init__(self, width, height, seed=69):
        super().__init__(seed=seed)
        self.grid = MultiGrid(width, height, True)

        # Set lifepod location at the center of the grid
        self.lifepod_location = (width // 2, height // 2)

        # Create and place the Lifepod
        self.lifepod = Lifepod(self)
        self.grid.place_agent(self.lifepod, self.lifepod_location)

        # Create and place worker agents at the lifepod location
        self.miner = Miner(self)
        self.engineer = Engineer(self)
        self.farmer = Farmer(self)

        for agent in [self.miner, self.engineer, self.farmer]:
            self.grid.place_agent(agent, self.lifepod_location)

        # Set fixed coordinates for the Drill and Greenhouse for simplicity
        self.drill_location = (
            self.lifepod_location[0] + 4,
            self.lifepod_location[1] + 4,
        )  # Example: place drill 2 units to the right of the lifepod
        self.greenhouse_location = (
            self.lifepod_location[0] - 4,
            self.lifepod_location[1],
        )  # Example: place greenhouse 4 units to the left of the lifepod

        # Create and place resource-generating structures at these specific locations
        self.drill = Drill(self)
        self.greenhouse = Greenhouse(self)

        # Ensure drill and greenhouse are not placed on the lifepod location
        if self.drill_location != self.lifepod_location:
            self.grid.place_agent(self.drill, self.drill_location)

        if self.greenhouse_location != self.lifepod_location:
            self.grid.place_agent(self.greenhouse, self.greenhouse_location)

        # Create DataCollector to track model state
        self.datacollector = DataCollector(
            model_reporters={
                "Total Food": lambda m: m.lifepod.food,
                "Total Iron": lambda m: m.lifepod.iron,  # Track the iron count in the Lifepod
                "Drill Health": lambda m: m.drill.health,
                "Drill Fuel": lambda m: m.drill.fuel,
                "Greenhouse Food": lambda m: m.greenhouse.food,
                "Miner Stamina": lambda m: m.miner.stamina,
                "Engineer Stamina": lambda m: m.engineer.stamina,
                "Farmer Stamina": lambda m: m.farmer.stamina,
                "Cell Contents": self.record_cell_contents,
            }
        )

    def record_cell_contents(self):
        """Record the contents of each cell in the grid."""
        cell_data = {}
        for cell_contents, (x, y) in self.grid.coord_iter():
            cell_data[(x, y)] = [type(agent).__name__ for agent in cell_contents]
        return cell_data

    def step(self):
        """Advance the model by one step."""
        self.datacollector.collect(self)

        self.agents.shuffle_do("step")


class ZombieApocalypse(Model):
    """A model with some zombies and human agents"""

    def __init__(self, width, height, initial_zombies, initial_humans, seed=69):
        super().__init__(seed=seed)
        self.num_humans = initial_humans
        self.num_zombies = initial_zombies
        self.grid = MultiGrid(width, height, False)

        # Create humans
        for i in range(self.num_humans):
            human = HumanAgent(self)
            x = self.rng.integers(0, self.grid.width)
            y = self.rng.integers(0, self.grid.height)
            self.grid.place_agent(human, (x, y))

        # Create zombies
        for i in range(self.num_zombies):
            zombie = ZombieAgent(self)
            x = self.rng.integers(0, self.grid.width)
            y = self.rng.integers(0, self.grid.height)
            self.grid.place_agent(zombie, (x, y))

        # Create DataCollector to track the number of humans and zombies with respective cell content
        self.datacollector = DataCollector(
            model_reporters={
                "Humans": self.count_humans,
                "Zombies": self.count_zombies,
                "coordinates": self.record_cell_contents,
            }
        )

    def count_humans(self):
        """Count the number of humans in the model."""
        return self.num_humans

    def count_zombies(self):
        """Count the number of zombies in the model."""
        return self.num_zombies

    def record_cell_contents(self):
        """Record the contents of each cell in the grid."""
        cell_data = {}
        for cell_contents, (x, y) in self.grid.coord_iter():
            # Store cell coordinates and contents
            cell_data[(x, y)] = [type(agent).__name__ for agent in cell_contents]
        return cell_data

    def step(self):
        """Advance the model by one step."""

        self.datacollector.collect(self)
        self.agents.shuffle_do("step")

        for cell in self.grid.coord_iter():
            cell_contents, (x, y) = cell
            humans = [agent for agent in cell_contents if isinstance(agent, HumanAgent)]
            zombies = [
                agent for agent in cell_contents if isinstance(agent, ZombieAgent)
            ]

            if humans and zombies:
                for human in humans:
                    # Convert human to zombie
                    self.grid.remove_agent(human)
                    Agent.remove(human)
                    new_zombie = ZombieAgent(self)
                    self.grid.place_agent(new_zombie, (x, y))

                    # Update counters
                    self.num_humans -= 1
                    self.num_zombies += 1
