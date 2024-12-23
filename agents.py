import mesa


class HumanAgent(mesa.Agent):
    """This agent is a bitch ass nigga"""

    def __init__(self, model):
        # Pass the parameters to the parent class.
        super().__init__(model)

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def step(self):
        self.move()


class ZombieAgent(mesa.Agent):
    """A retarded stinking zombie"""

    def __init__(self, model):
        # Pass the parameters to the parent class.
        super().__init__(model)

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def step(self):
        self.move()
