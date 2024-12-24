from mesa import Agent


class BaseHumanAgent(Agent):
    def __init__(self, model, stamina):
        super().__init__(model)
        self.stamina = stamina

    def move(self):
        """Move to a random adjacent cell."""
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def rest(self):
        """Rest to regain stamina."""
        if self.stamina == 0:
            self.stamina += 10  # Add stamina when resting
