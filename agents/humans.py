from agents.base import BaseHumanAgent
from agents.structures import Lifepod, Greenhouse, Drill


class Miner(BaseHumanAgent):
    def __init__(self, model, stamina=69):
        super().__init__(model, stamina)
        self.iron = 0

    def step(self):
        """Perform the miner's actions for each step."""
        lifepod = self.get_lifepod()

        if self.model.is_night:  # Nighttime behavior
            if lifepod:
                if self.pos != lifepod.pos:  # Move to the lifepod if not already there
                    self.move_towards(lifepod.pos)
                else:
                    self.rest()
        else:  # Daytime behavior
            if self.iron == self.inventory:  # Inventory is full
                if lifepod:
                    if self.pos != lifepod.pos:  # Move to the lifepod to store resources
                        self.move_towards(lifepod.pos)
                    else:
                        lifepod.store_iron(self.iron)
                        self.iron = 0  # Reset inventory after storing
            elif self.stamina > 0:  # If stamina is available and inventory is not full
                nearest_drill = self.find_nearest_drill()
                if nearest_drill:
                    if self.is_near_drill(nearest_drill):  # Close enough to use the drill
                        self.use_drill(nearest_drill)
                    else:  # Move closer to the drill
                        self.move_towards(nearest_drill.pos)
                else:
                    self.rest()  # Rest if no drills are available
            else:  # Stamina is depleted
                self.rest()

    def is_near_drill(self, drill):
        """Check if the miner is adjacent to the drill (within one step)."""
        return (
            abs(self.pos[0] - drill.pos[0]) <= 1
            and abs(self.pos[1] - drill.pos[1]) <= 1
        )

    def find_nearest_drill(self):
        """Find the nearest functional drill."""
        drills = [
            agent
            for agent in self.model.agents
            if isinstance(agent, Drill) and not agent.is_broken()
        ]
        if not drills:
            return None
        # Find the drill with the minimum Manhattan distance
        return min(drills, key=lambda drill: abs(drill.pos[0] - self.pos[0]) + abs(drill.pos[1] - self.pos[1]))

    def use_drill(self, drill):
        """Use the drill to collect resources."""
        if drill.fuel > 0 and not drill.is_broken():
            iron_to_collect = min(self.inventory - self.iron, drill.iron)
            self.iron += iron_to_collect
            drill.iron -= iron_to_collect
            self.stamina -= 30  # Mining consumes stamina

    def get_lifepod(self):
        """Retrieve the Lifepod in the model."""
        for agent in self.model.agents:
            if isinstance(agent, Lifepod):
                return agent
        return None

class Engineer(BaseHumanAgent):
    def __init__(self, model, stamina=69):
        super().__init__(model, stamina)

    def step(self):
        """Define the engineer's actions for each step."""
        if self.model.is_night:  # Follow the BaseAgent's night behavior
            super().step()
            return

        if self.stamina > 0:
            # Check for a nearby broken drill and move towards it if necessary
            nearest_broken_drill = self.find_nearest_broken_drill()
            if nearest_broken_drill:
                print(
                    f"Engineer at {self.pos} moving towards broken drill at {nearest_broken_drill.pos}."
                )
                if self.is_near_drill(nearest_broken_drill):
                    self.repair(nearest_broken_drill)  # Repair the drill if near
                else:
                    self.move_towards(
                        nearest_broken_drill.pos
                    )  # Move towards the broken drill
            else:
                self.move()  # Move randomly if no broken drill is found
                print(f"Engineer at {self.pos} is moving randomly.")
        else:
            self.rest()  # Rest when stamina is depleted
            print(f"Engineer at {self.pos} is resting to regain stamina.")

    def find_nearest_broken_drill(self):
        """Find the nearest broken drill on the grid."""
        drills = [
            agent
            for agent in self.model.agents
            if isinstance(agent, Drill) and agent.is_broken()
        ]
        if drills:
            nearest_drill = min(
                drills,
                key=lambda drill: abs(self.pos[0] - drill.pos[0])
                + abs(self.pos[1] - drill.pos[1]),
            )
            print(f"Nearest broken drill found at {nearest_drill.pos}.")
            return nearest_drill
        print("No broken drills found.")
        return None

    def is_near_drill(self, drill):
        """Check if the engineer is adjacent to the drill (within one step)."""
        return (
            abs(self.pos[0] - drill.pos[0]) <= 1
            and abs(self.pos[1] - drill.pos[1]) <= 1
        )

    def repair(self, drill):
        """Repair the drill."""
        if drill.is_broken():
            print(f"Engineer at {self.pos} repairing drill at {drill.pos}.")
            drill.repair()
            self.stamina = max(
                0, self.stamina - 10
            )  # Reduce stamina but ensure it doesn't go below 0
        else:
            print(f"Drill at {drill.pos} is not broken.")

    def rest(self):
        """Regain stamina when resting."""
        super().rest()  # Call the base class's rest method
        if self.stamina < 100:
            self.stamina = min(100, self.stamina + 10)  # Increment stamina towards full
            print(
                f"Engineer at {self.pos} is resting. Current stamina: {self.stamina}."
            )


class Farmer(BaseHumanAgent):
    def __init__(self, model, stamina=69):
        super().__init__(model, stamina)
        self.food = 0

    def step(self):
        """Define the farmer's behavior for each step."""
        lifepod = self.get_lifepod()

        if self.model.is_night:  # Nighttime behavior
            if lifepod:
                if self.pos != lifepod.pos:  # Move to the lifepod if not already there
                    self.move_towards(lifepod.pos)
                else:
                    self.rest()
        else:  # Daytime behavior
            if self.food == self.inventory:  # Inventory is full
                if lifepod:
                    if self.pos != lifepod.pos:  # Move to the lifepod to store food
                        self.move_towards(lifepod.pos)
                    else:
                        lifepod.store_food(self.food)
                        self.food = 0  # Reset inventory after storing
            elif self.stamina > 0:  # If stamina is available and inventory is not full
                nearest_greenhouse = self.find_nearest_greenhouse()
                if nearest_greenhouse:
                    if not self.near_greenhouse(nearest_greenhouse):  # Move closer
                        self.move_towards(nearest_greenhouse.pos)
                    else:  # Collect food if near the greenhouse
                        self.collect_food(nearest_greenhouse)
                else:
                    self.rest()  # Rest if no greenhouses are available
            else:  # Stamina is depleted
                self.rest()

    def collect_food(self, greenhouse):
        """Collect food from the greenhouse."""
        if greenhouse.food > 0:
            food_to_collect = min(self.inventory - self.food, greenhouse.food)
            self.food += food_to_collect
            greenhouse.food -= food_to_collect
            self.stamina = max(self.stamina - 10, 0)  # Decrease stamina for collecting food

    def find_nearest_greenhouse(self):
        """Find the nearest greenhouse on the grid."""
        greenhouses = [
            agent for agent in self.model.agents if isinstance(agent, Greenhouse)
        ]
        if greenhouses:
            return min(
                greenhouses,
                key=lambda greenhouse: abs(greenhouse.pos[0] - self.pos[0])
                + abs(greenhouse.pos[1] - self.pos[1]),
            )
        return None

    def near_greenhouse(self, greenhouse):
        """Check if the farmer is near a specific greenhouse."""
        return self.pos == greenhouse.pos

    def get_lifepod(self):
        """Retrieve the Lifepod in the model."""
        for agent in self.model.agents:
            if isinstance(agent, Lifepod):
                return agent
        return None


    # Use the rest method from BaseAgent
    # No need to redefine rest() since it's already handled by BaseAgent
