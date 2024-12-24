from agents.base import BaseHumanAgent
from agents.structures import Lifepod, Greenhouse, Drill


class Storm(Agent):
    def __init__(self, model, duration):
        super().__init__(model)
        self.duration = duration

    def step(self):
        # Move across the grid
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

        # Affect agents and structures in the storm's path
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        for agent in cell_contents:
            if isinstance(agent, BaseHumanAgent):
                agent.stamina -= 20  # Storm depletes stamina
            elif isinstance(agent, Drill):
                agent.health = max(0, agent.health - 10)  # Damages equipment

        # Reduce duration and remove when it expires
        self.duration -= 1
        if self.duration <= 0:
            self.model.grid.remove_agent(self)
