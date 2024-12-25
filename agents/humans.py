from agents.base import BaseHumanAgent
from agents.structures import Lifepod, Greenhouse, Drill


class Miner(BaseHumanAgent):
    def __init__(self, model, stamina=50):
        super().__init__(model, stamina)
        self.iron = 0

    def step(self):
        """Perform the miner's actions for each step."""

        if self.model.is_night:  # Nighttime behavior
            self.rest()
        else:  # Daytime actions
            lifepod = self.get_lifepod()
            if self.stamina > 0 and self.iron != self.inventory:
                nearest_drill = self.find_nearest_drill()
                if nearest_drill:
                    print(
                        f"Miner at {self.pos} moving towards drill at {nearest_drill.pos}"
                    )
                    # Check if miner is within one step of the drill
                    if self.is_near_drill(nearest_drill):
                        print(
                            f"Miner is near the drill at {nearest_drill.pos}. Starting to collect."
                        )
                        self.use_drill(nearest_drill)
                    else:
                        # Move towards the drill
                        self.move_towards(nearest_drill.pos)
                else:
                    print("No drill found.")
                    self.rest()  # If no drill is found, the miner rests
            elif self.stamina > 0 and self.iron == self.inventory:
                # Move towards the lifepod to store iron
                if lifepod and self.pos != lifepod.pos:
                    print(
                        f"Miner at {self.pos} moving towards Lifepod at {lifepod.pos}"
                    )
                    self.move_towards(lifepod.pos)
                elif lifepod and self.pos == lifepod.pos:
                    # Store iron only when at the Lifepod's position
                    lifepod.store_iron(self.iron)
                    print(f"Stored {self.iron} iron in the Lifepod.")
                    self.iron = 0  # Reset the miner's iron after storing it
            else:
                self.rest()  # Rest when stamina is depleted

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
        return min(
            drills,
            key=lambda drill: abs(drill.pos[0] - self.pos[0])
            + abs(drill.pos[1] - self.pos[1]),
        )

    def use_drill(self, drill):
        """Use the drill to collect resources."""
        if drill.fuel > 0 and not drill.is_broken():
            iron_to_collect = min(self.inventory - self.iron, drill.iron)
            self.iron += iron_to_collect
            drill.iron -= iron_to_collect  # Deduct iron from the drill's reserves
            print(f"Collected {iron_to_collect} iron. Total Iron: {self.iron}")

            # Check if the miner's inventory is full
            if self.iron == self.inventory:
                print("Inventory full. Returning to the Lifepod.")
                lifepod = self.get_lifepod()
                if lifepod:
                    # Move towards the Lifepod
                    if self.pos != lifepod.pos:
                        self.move_towards(lifepod.pos)

            self.stamina -= 10  # Miner consumes stamina each time they collect iron
        else:
            print("Drill cannot be used due to lack of fuel or health.")

    def rest(self):
        """Regain stamina when resting."""
        super().rest()  # Call the base class's rest method
        print(
            f"Miner at {self.pos} is resting to regain stamina."
        )  # Print when the miner is resting


class Engineer(BaseHumanAgent):
    def __init__(self, model, stamina=50):
        super().__init__(model, stamina)
        self.repair_time = 0  # Track the number of steps spent repairing

    def step(self):
        """Define the engineer's actions for each step."""
        if self.model.is_night:  # Follow the BaseAgent's night behavior
            self.rest()

        if self.stamina > 0:
            # Check for a nearby broken drill and move towards it if necessary
            nearest_broken_drill = self.find_nearest_broken_drill()
            if nearest_broken_drill:
                if self.is_near_drill(nearest_broken_drill):
                    if self.repair_time == 0:
                        self.repair(nearest_broken_drill)  # Start repair
                    else:
                        self.repair_time += 1  # Increment repair time during repair
                        if (
                            self.repair_time >= 20
                        ):  # If 20 steps have passed, complete the repair
                            self.complete_repair(nearest_broken_drill)
                else:
                    self.move_towards(
                        nearest_broken_drill.pos
                    )  # Move towards the broken drill
            else:
                self.move()  # Move randomly if no broken drill is found
        else:
            self.rest()  # Rest when stamina is depleted

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
            return nearest_drill
        return None

    def is_near_drill(self, drill):
        """Check if the engineer is adjacent to the drill (within one step)."""
        return (
            abs(self.pos[0] - drill.pos[0]) <= 1
            and abs(self.pos[1] - drill.pos[1]) <= 1
        )

    def repair(self, drill):
        """Start repairing the drill."""
        if drill.is_broken():
            self.repair_time = 1  # Start tracking repair time
            self.stamina = max(self.stamina - 5, 0)  # Deplete stamina progressively
        else:
            pass  # Drill is not broken, no repair needed

    def complete_repair(self, drill):
        """Complete the repair after 20 steps."""
        if self.repair_time >= 20:  # Complete repair only after 20 steps
            drill.repair()  # Complete the repair
            self.repair_time = 0  # Reset repair time counter
            self.stamina = max(
                self.stamina - 10, 0
            )  # Reduce stamina for completing the repair


class Farmer(BaseHumanAgent):
    def __init__(self, model, stamina=50):
        super().__init__(model, stamina)
        self.food = 0

    def step(self):
        """Define the farmer's behavior for each step."""
        if self.model.is_night:  # Nighttime behavior
            self.rest()
        else:  # Daytime actions
            lifepod = self.get_lifepod()  # Ensure lifepod is fetched
            if self.stamina > 0 and self.food != self.inventory:
                nearest_greenhouse = self.find_nearest_greenhouse()
                if nearest_greenhouse:
                    print(
                        f"Farmer at {self.pos} moving towards greenhouse at {nearest_greenhouse.pos}"
                    )
                    # Check if farmer is within one step of the greenhouse
                    if self.near_greenhouse(nearest_greenhouse):
                        print(
                            f"Farmer is near the greenhouse at {nearest_greenhouse.pos}. Starting to collect."
                        )
                        self.collect_food(nearest_greenhouse)
                    else:
                        # Move towards the greenhouse
                        self.move_towards(nearest_greenhouse.pos)
                else:
                    print("No greenhouse found.")
                    self.rest()  # If no greenhouse is found, the farmer rests
            elif self.stamina > 0 and self.food == self.inventory:
                # Move towards the lifepod to store food
                if lifepod and self.pos != lifepod.pos:
                    print(
                        f"Farmer at {self.pos} moving towards Lifepod at {lifepod.pos}"
                    )
                    self.move_towards(lifepod.pos)
                elif lifepod and self.pos == lifepod.pos:
                    # Store food only when at the Lifepod's position
                    lifepod.store_food(self.food)
                    print(f"Stored {self.food} food in the Lifepod.")
                    self.food = 0  # Reset the farmer's food after storing it
            else:
                self.rest()  # Rest when stamina is depleted

    def collect_food(self, greenhouse):
        """Collect food from the greenhouse"""
        if greenhouse.food > 0:
            food_to_collect = min(self.inventory - self.food, greenhouse.food)
            self.food += food_to_collect
            greenhouse.food -= food_to_collect  # Reduce food from the greenhouse
            print(
                f"Farmer collected {food_to_collect} food from greenhouse at {self.pos}. Total Food: {self.food}"
            )

            # Decrease stamina for collecting food
            self.stamina = max(self.stamina - 5, 0)
        else:
            print(f"Greenhouse at {self.pos} has no food left.")

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
