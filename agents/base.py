from mesa import Agent


class BaseHumanAgent(Agent):
    def __init__(self, model, stamina):
        super().__init__(model)
        self.stamina = stamina

    def move_towards(self, target_pos):
        """Move towards a target position."""
        x, y = self.pos
        target_x, target_y = target_pos

        # Determine the direction of movement (one step towards the target)
        if x < target_x:
            x += 1
        elif x > target_x:
            x -= 1

        if y < target_y:
            y += 1
        elif y > target_y:
            y -= 1

        # Move the agent to the new position
        new_position = (x, y)
        self.model.grid.place_agent(self, new_position)

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
