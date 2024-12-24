from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from agents.humans import Engineer, Farmer, Miner
from agents.environment import AsteroidStrike
from agents.structures import Lifepod, Greenhouse, Drill


class SpaceColony(Model):
    """The goddamn model"""

    def __init__(self, width, height, seed=69):
        super().__init__(seed=seed)
        self.grid = MultiGrid(width, height, False)
        self.strike_probability = 0.1  # Chance of a storm each step

        # Randomly generate storms
        if self.random.random() < self.strike_probability:
            strike = AsteroidStrike("AsteroidStrike", self, duration=8)

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
            self.lifepod_location[1] + 4,
        )  # Example: place greenhouse 4 units to the left of the lifepod

        # Create and place resource-generating structures at these specific locations
        self.drill = Drill(self)
        self.greenhouse = Greenhouse(self)

        # Ensure drill and greenhouse are not placed on the lifepod location
        if self.drill_location != self.lifepod_location:
            self.grid.place_agent(self.drill, self.drill_location)

        if self.greenhouse_location != self.lifepod_location:
            self.grid.place_agent(self.greenhouse, self.greenhouse_location)

        # Day-night cycle variables
        self.time_step = 0
        self.is_night = False

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
                "Is Night": lambda m: m.is_night,
                "Cell Contents": self.record_cell_contents,
            }
        )

    def record_cell_contents(self):
        """Record the contents of each cell in the grid."""
        cell_data = {}
        for cell_contents, (x, y) in self.grid.coord_iter():
            cell_data[(x, y)] = [type(agent).__name__ for agent in cell_contents]
        return cell_data

    def toggle_day_night(self):
        """Toggle the day-night cycle based on the time step."""
        # Day lasts for 30 iterations, night lasts for 15 iterations
        if self.time_step % 45 < 30:
            self.is_night = False
        else:
            self.is_night = True
        print(f"Time Step: {self.time_step}, Night: {self.is_night}")

    def step(self):
        """Advance the model by one step."""
        # Update the day-night cycle
        self.toggle_day_night()

        # Collect data and advance agents
        self.datacollector.collect(self)
        self.agents.shuffle_do("step")

        # Increment the time step
        self.time_step += 1
