from mesa import Agent
from agents.base import BaseHumanAgent
from agents.structures import Lifepod, Greenhouse, Drill


class AsteroidStrike(Agent):
    def __init__(self, model, duration, position):
        super().__init__(model)
        self.duration = duration
        self.position = position

    def step(self):
        """Affect agents in the strike's path."""
        if self.position:  # Ensure position is valid
            # Affect agents in the given cell
            cell_contents = self.model.grid.get_cell_list_contents([self.position])
            for agent in cell_contents:
                if isinstance(agent, BaseHumanAgent):
                    agent.stamina -= 10  # Reduce stamina of human agents
                elif isinstance(agent, Drill):
                    agent.health = max(0, agent.health - 10)  # Reduce health of drills

        self.duration -= 1
        if self.duration <= 0:
            try:
                self.model.grid.remove_agent(self)
                Agent.remove(self)
            except Exception as e:
                print(f"Error removing asteroid strike: {e}")
