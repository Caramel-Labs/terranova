from agents.base import BaseHumanAgent
from agents.structures import Lifepod, Greenhouse, Drill


class Miner(BaseHumanAgent):
    def __init__(self, model, stamina=69):
        super().__init__(model, stamina)
        self.iron = 0

    def step(self):
        """Perform the miner's actions for each step."""
        lifepod = self.get_lifepod()
        if self.model.is_night:  # Check if it's nighttime
            if lifepod:
                print(
                    f"Miner at {self.pos} moving towards Lifepod at {lifepod.pos} during the night."
                )
                if self.pos != lifepod.pos:  # If not at the Lifepod, move towards it
                    self.move_towards(lifepod.pos)
                else:
                    print(
                        f"Miner at {self.pos} is staying at the Lifepod during the night."
                    )
        else:  # Daytime actions
            lifepod = self.get_lifepod()  # Ensure lifepod is fetched
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
        """Find the nearest drill on the grid."""
        drills = [
            agent
            for agent in self.model.agents
            if isinstance(agent, Drill) and not agent.is_broken()
        ]
        print(
            f"Available drills: {[drill.pos for drill in drills]}"
        )  # Debug: print available drills
        if not drills:
            return None
        # Find the drill with the minimum Manhattan distance
        nearest_drill = min(
            drills,
            key=lambda drill: abs(drill.pos[0] - self.pos[0])
            + abs(drill.pos[1] - self.pos[1]),
        )
        print(
            f"Nearest drill found at {nearest_drill.pos}"
        )  # Debug: print nearest drill
        return nearest_drill

    def use_drill(self, drill):
        """Use the drill to collect resources."""
        if drill.fuel > 0 and not drill.is_broken():
            print("Drill is functional. Collecting resources.")

            # Collect enough iron to fill the miner's inventory
            iron_to_collect = min(
                self.inventory - self.iron, drill.iron
            )  # Ensure the miner doesn't overfill or take more than available
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

    def get_lifepod(self):
        """Retrieve the Lifepod in the model."""
        # Assuming you have only one Lifepod in your model, find it
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
        lifepod = self.get_lifepod()
        if self.model.is_night:  # Check if it's nighttime

            if lifepod:
                print(
                    f"Farmer at {self.pos} moving towards Lifepod at {lifepod.pos} during the night."
                )
                if self.pos != lifepod.pos:  # If not at the Lifepod, move towards it
                    self.move_towards(lifepod.pos)
                else:
                    print(
                        f"Farmer at {self.pos} is staying at the Lifepod during the night."
                    )
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
            # Calculate how much food to collect based on inventory space and available food
            food_to_collect = min(self.inventory - self.food, greenhouse.food)
            self.food += food_to_collect
            greenhouse.food -= food_to_collect  # Reduce food from the greenhouse
            print(
                f"Farmer collected {food_to_collect} food from greenhouse at {self.pos}. Total Food: {self.food}"
            )

            # Check if the farmer's inventory is full
            if self.food == self.inventory:
                print("Inventory full. Returning to the Lifepod.")
                lifepod = self.get_lifepod()
                if lifepod:
                    # Move towards the Lifepod
                    if self.pos != lifepod.pos:
                        self.move_towards(lifepod.pos)

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
            nearest_greenhouse = min(
                greenhouses,
                key=lambda greenhouse: abs(greenhouse.pos[0] - self.pos[0])
                + abs(greenhouse.pos[1] - self.pos[1]),
            )
            return nearest_greenhouse
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
