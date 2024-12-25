from mesa import Agent


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

    def rest(self):
        """Rest to regain stamina."""
        max_stamina = 100  # Define maximum stamina
        if self.stamina < max_stamina:
            self.stamina = min(self.stamina + 10, max_stamina)

    def step(self):
        """Define agent behavior during each step."""
        if self.stamina <= 0:  # If stamina is depleted, rest until fully restored
            self.rest()
        elif self.stamina < 100:  # Continue resting if stamina is not full
            self.rest()
        elif self.model.is_night:  # Nighttime behavior
            lifepod_pos = self.model.lifepod_location
            if self.pos != lifepod_pos:  # If not already at the lifepod
                self.move_towards(lifepod_pos)
            else:
                self.rest()  # Rest at the lifepod during the night
        else:
            # Define day behavior in derived classes
            pass  # To be implemented by specific agents
