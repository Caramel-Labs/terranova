from mesa import Agent


class BaseHumanAgent(Agent):
    def __init__(self, model, stamina):
        super().__init__(model)
        self.stamina = stamina

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
        print(f"{type(self).__name__} moved to {self.pos}.")

    def move(self):
        """Move randomly to a neighboring cell."""
        # Get all possible neighboring positions
        possible_moves = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        # Choose a random move from the available positions
        new_pos = self.random.choice(possible_moves)
        # Update the position on the grid
        self.model.grid.move_agent(self, new_pos)
        print(f"{type(self).__name__} moved to {new_pos}.")

    def rest(self):
        """Rest to regain stamina."""
        max_stamina = 100  # Define maximum stamina
        if self.stamina < max_stamina:
            self.stamina = min(self.stamina + 10, max_stamina)
            print(f"{type(self).__name__} resting. Stamina: {self.stamina}/{max_stamina}")

    def step(self):
        """Define agent behavior during each step."""
        if self.model.is_night:
            # Move towards the lifepod if it's night
            lifepod_pos = self.model.lifepod_location
            if self.pos != lifepod_pos:  # If not already at the lifepod
                self.move_towards(lifepod_pos)
            else:
                print(f"{type(self).__name__} resting at lifepod during night at {self.pos}.")
                self.rest()
        else:
            # Define day behavior in derived classes
            print(f"{type(self).__name__} acting during the day.")
