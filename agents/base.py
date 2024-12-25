from mesa import Agent
from agents.structures import Lifepod


class BaseHumanAgent(Agent):
    def __init__(self, model, stamina):
        super().__init__(model)
        self.stamina = stamina
        self.inventory = 5

    def move_towards(self, target_pos):
        """Move towards the target position (target_pos is a tuple)."""
        x, y = self.pos
        target_x, target_y = target_pos

        # Move horizontally towards the target
        if x < target_x:
            x += 1  # Move right
        elif x > target_x:
            x -= 1  # Move left

        # Move vertically towards the target
        if y < target_y:
            y += 1  # Move down
        elif y > target_y:
            y -= 1  # Move up

        # Update the position on the grid
        self.model.grid.move_agent(self, (x, y))

    def move(self):
        """Move randomly to a neighboring cell."""
        # Get all possible neighboring positions
        possible_moves = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        # Choose a random move from the available positions
        new_pos = self.random.choice(possible_moves)
        # Update the position on the grid
        self.model.grid.move_agent(self, new_pos)

    def get_lifepod(self):
        """Retrieve the Lifepod in the model."""
        for agent in self.model.agents:
            if isinstance(agent, Lifepod):
                return agent
        return None

    def rest(self):
        """Rest to regain stamina."""
        max_stamina = 100  # Define maximum stamina
        lifepod = self.get_lifepod()

        if lifepod:
            if self.pos != lifepod.pos:  # Move to the lifepod if not already there
                self.move_towards(lifepod.pos)
            else:
                if self.stamina < max_stamina:
                    self.stamina = min(self.stamina + 10, max_stamina)
                    print(
                        f"Agent at {self.pos} is staying at the Lifepod during the night."
                    )

    def step(self):
        """Define agent behavior during each step."""
        if self.stamina <= 0:  # If stamina is depleted, rest until fully restored
            self.rest()
        else:
            pass  # To be implemented by specific agents
