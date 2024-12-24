from base import BaseHumanAgent
from structures import Lifepod, Greenhouse, Drill


class Miner(BaseHumanAgent):
    def __init__(self, model, stamina=69):
        super().__init__(model, stamina)
        self.iron = 0

    def step(self):
        """Perform the miner's actions for each step."""
        if self.stamina > 0:
            nearest_drill = self.find_nearest_drill()

            if nearest_drill:
                print(
                    f"Miner at {self.pos} moving towards drill at {nearest_drill.pos}"
                )

                # Check if miner is within one step of the drill
                if self.is_near_drill(nearest_drill):
                    print(
                        f"Miner is near the drill at {nearest_drill.pos}. Starting to mine."
                    )
                    self.use_drill(nearest_drill)
                else:
                    # Move towards the drill
                    self.move_towards(nearest_drill.pos)
            else:
                print("No drill found.")
                self.rest()  # If no drill is found, the miner rests
        else:
            self.rest()  # Rest when stamina is depleted

    def move_towards(self, target_pos):  # Target position is the drill
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

        # Update the miner's position
        self.pos = (x, y)
        print(f"Miner moved to {self.pos}")

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
            print("Drill is functional, starting mining.")
            drill.mine()  # The drill mines and updates its fuel, health, and iron state
            self.iron += 3  # Miner collects iron
            print(f"Mining... Total Iron: {self.iron}")

            # After collecting iron, store it in the Lifepod
            lifepod = self.get_lifepod()
            if lifepod:
                lifepod.store_iron(3)  # Store 3 iron in the Lifepod

            self.stamina -= 1  # Miner consumes stamina each time it mines
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
        if self.stamina > 0:
            # Check for a nearby broken drill and move towards it if necessary
            nearest_broken_drill = self.find_nearest_broken_drill()
            if nearest_broken_drill:
                print(
                    f"Engineer at {self.pos} moving towards broken drill at {nearest_broken_drill.pos}."
                )
                if self.is_near_drill(nearest_broken_drill):
                    self.repair(nearest_broken_drill)  # Repair the drill if near
                    print(
                        f"Engineer at {self.pos} repaired the drill at {nearest_broken_drill.pos}."
                    )
                else:
                    self.move_towards(
                        nearest_broken_drill.pos
                    )  # Move towards the broken drill
                    print(f"Engineer at {self.pos} is moving towards the drill.")
            else:
                self.move()  # Move randomly if no broken drill is found
                print(f"Engineer at {self.pos} is moving randomly.")
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
                key=lambda drill: abs(drill.pos[0] - self.pos[0])
                + abs(drill.pos[1] - self.pos[1]),
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
        """Repair the drill."""
        if drill.is_broken():
            print(f"Repairing drill at {drill.pos}.")
            drill.repair()  # Repair the drill
            self.stamina -= 10  # Repairing costs stamina
        else:
            print(f"Drill at {drill.pos} is not broken.")

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
        self.model.grid.move_agent(self, new_position)
        print(f"Engineer moved to {self.pos}.")

    def rest(self):
        """Regain stamina when resting."""
        super().rest()  # Call the base class's rest method
        print(
            f"Engineer at {self.pos} is resting to regain stamina."
        )  # Print when the Engineer is resting


class Farmer(BaseHumanAgent):
    def __init__(self, model, stamina=69):
        super().__init__(model, stamina)

    def step(self):
        if self.stamina > 0:
            nearest_greenhouse = (
                self.find_nearest_greenhouse()
            )  # Find the nearest greenhouse

            if nearest_greenhouse:
                # Move towards the greenhouse until the farmer is near it
                if not self.near_greenhouse(nearest_greenhouse):
                    self.move_towards(nearest_greenhouse.pos)
                    print(
                        f"Farmer at {self.pos} is moving towards greenhouse at {nearest_greenhouse.pos}."
                    )
                else:
                    self.collect_food(
                        nearest_greenhouse
                    )  # Collect food if near the greenhouse
            else:
                print("No greenhouse found.")
        else:
            self.rest()  # Rest when stamina is depleted

    def collect_food(self, greenhouse):
        """Collect food from the greenhouse and store in the Lifepod."""
        if greenhouse.food > 0:
            collected_food = 5  # The farmer collects 5 units of food
            greenhouse.food -= collected_food  # Reduce food from the greenhouse
            print(
                f"Farmer collected {collected_food} food from greenhouse at {self.pos}."
            )

            lifepod = self.get_lifepod()
            if lifepod:
                lifepod.store_food(
                    collected_food
                )  # Store collected food in the Lifepod

            # Decrease stamina only when collecting food
            self.stamina = max(
                self.stamina - 5, 0
            )  # Decrease stamina for collecting food
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

        # Update the farmer's position
        self.pos = (x, y)
        print(f"Farmer moved to {self.pos}")

    def get_lifepod(self):
        """Retrieve the Lifepod in the model."""
        for agent in self.model.agents:
            if isinstance(agent, Lifepod):
                return agent
        return None

    # Use the rest method from BaseAgent
    # No need to redefine rest() since it's already handled by BaseAgent
