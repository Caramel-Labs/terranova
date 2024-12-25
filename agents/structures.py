from mesa import Agent


class Lifepod(Agent):
    def __init__(self, model):
        super().__init__(model)
        self.food = 20  # Starting food in the Lifepod
        self.iron = 0  # Starting iron in the Lifepod

    def store_iron(self, amount):
        """Store the given amount of iron in the Lifepod."""
        self.iron += amount
        print(f"Lifepod now has {self.iron} iron.")

    def get_iron(self):
        """Get the current amount of iron in the Lifepod."""
        return self.iron

    def store_food(self, amount):
        """Store the given amount of food in the Lifepod."""
        self.food += amount
        print(f"Lifepod now has {self.food} food.")

    def get_food(self):
        """Get the current amount of food in the Lifepod."""
        return self.food


class Greenhouse(Agent):
    def __init__(self, model, max_food=100, food_add_rate=2):
        super().__init__(model)
        self.food = 0
        self.max_food = max_food
        self.food_add_rate = (
            food_add_rate  # Rate at which food is added to the greenhouse
        )

    def step(self):
        # The greenhouse adds food at a set rate, up to the max capacity
        self.add_food(self.food_add_rate)

    def add_food(self, amount):
        """Add food to the greenhouse, respecting the max_food limit."""
        if self.food + amount <= self.max_food:
            self.food += amount
            print(f"Greenhouse added {amount} food. Total food: {self.food}")
        else:
            self.food = self.max_food
            print(f"Greenhouse food reached max capacity: {self.food}")


class Drill(Agent):
    def __init__(self, model, max_fuel=69, max_health=69):
        super().__init__(model)
        self.fuel = max_fuel
        self.iron = 0
        self.health = max_health

    def step(self):
        self.mine()

    def is_broken(self):
        """Check if the drill is broken (out of health or fuel)."""
        return (
            self.health <= 0 or self.fuel <= 0
        )  # Drill is considered broken if either fuel or health is zero

    def repair(self):
        """Repair the drill to full health and reset fuel."""
        self.health = 69  # Full health after repair
        self.fuel = 69  # Reset fuel after repair

    def mine(self):
        """Simulate mining using the drill."""
        if not self.is_broken():
            # Perform mining if the drill is functional
            self.fuel -= 1  # Decrease fuel
            self.iron += 2  # Increase iron
            self.health = max(
                0, self.health - 1
            )  # Decrease health, ensure it's non-negative
            print(
                f"Mining... Drill Fuel: {self.fuel}, Drill Health: {self.health}, Iron: {self.iron}"
            )
        else:
            print("Drill is out of fuel or broken!")
