from mesa import Agent
from agents.base import BaseHumanAgent
from agents.structures import Lifepod, Greenhouse, Drill


class AsteroidStrike(Agent):
    def __init__(self, model, duration):
        super().__init__(model)
        self.duration = duration
        self.positions = []  # Store positions where the asteroid strike will happen

    def place_on_grid(self):
        """Place the asteroid strike on 5 random cells of the grid."""
        all_cells = list(self.model.grid.coord_iter())
        random_cells = self.random.sample(all_cells, min(5, len(all_cells)))
        for cell in random_cells:
            cell_pos = cell[1]  # Get position of the cell
            self.model.grid.place_agent(self, cell_pos)
            self.positions.append(cell_pos)

    def step(self):
        """Affect agents in the storm's path."""
        if not self.positions:  # If the agent isn't placed yet, place it
            self.place_on_grid()

        # Affect agents in the selected cells
        for cell_pos in self.positions:
            cell_contents = self.model.grid.get_cell_list_contents([cell_pos])
            for agent in cell_contents:
                if isinstance(agent, BaseHumanAgent):
                    agent.stamina -= 20  # Reduce stamina of human agents
                elif isinstance(agent, Drill):
                    agent.health = max(0, agent.health - 10)  # Reduce health of drills

        # Reduce duration and remove the asteroid strike when it expires
        self.duration -= 1
        if self.duration <= 0:
            self.model.grid.remove_agent(self)
