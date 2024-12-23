import mesa
from mesa import Agent
from mesa.space import MultiGrid
from agents import HumanAgent, ZombieAgent
from mesa.datacollection import DataCollector


class ZombieApocalypse(mesa.Model):
    """A model with some zombies and human agents"""

    def __init__(self, width, height, initial_zombies, initial_humans, seed=69):
        super().__init__(seed=seed)
        self.num_humans = initial_humans
        self.num_zombies = initial_zombies
        self.grid = MultiGrid(width, height, True)

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
