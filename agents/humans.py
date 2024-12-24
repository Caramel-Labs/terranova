from agents.base import BaseHumanAgent
from agents.structures import Lifepod, Greenhouse, Drill


class Miner(BaseHumanAgent):
    def __init__(self, model, stamina=69):
        super().__init__(model, stamina)
        self.iron = 0

    def step(self):
        """Perform the miner's actions for each step."""
        if self.model.is_night:  # Check if it's nighttime
            lifepod = self.get_lifepod()
            if lifepod:
                print(f"Miner at {self.pos} moving towards Lifepod at {lifepod.pos} during the night.")
                if self.pos != lifepod.pos:  # If not at the Lifepod, move towards it
                    self.move_towards(lifepod.pos)
                else:
                    print(f"Miner at {self.pos} is staying at the Lifepod during the night.")
        else:  # Daytime actions
            if self.stamina > 0:
                nearest_drill = self.find_nearest_drill()

                if nearest_drill:
                    print(f"Miner at {self.pos} moving towards drill at {nearest_drill.pos}")
                    
                    # Check if miner is within one step of the drill
                    if self.is_near_drill(nearest_drill):
                        print(f"Miner is near the drill at {nearest_drill.pos}. Starting to mine.")
                        self.use_drill(nearest_drill)
                    else:
                        # Move towards the drill
                        self.move_towards(nearest_drill.pos)
                else:
                    print("No drill found.")
                    self.rest()  # If no drill is found, the miner rests
            else:
                self.rest()  # Rest when stamina is depleted

    def is_near_drill(self, drill):
        """Check if the miner is adjacent to the drill (within one step)."""
        return abs(self.pos[0] - drill.pos[0]) <= 1 and abs(self.pos[1] - drill.pos[1]) <= 1

    def find_nearest_drill(self):
        """Find the nearest drill on the grid."""
        drills = [agent for agent in self.model.agents if isinstance(agent, Drill) and not agent.is_broken()]
        print(f"Available drills: {[drill.pos for drill in drills]}")  # Debug: print available drills
        if not drills:
            return None
        # Find the drill with the minimum Manhattan distance
        nearest_drill = min(drills, key=lambda drill: abs(drill.pos[0] - self.pos[0]) + abs(drill.pos[1] - self.pos[1]))
        print(f"Nearest drill found at {nearest_drill.pos}")  # Debug: print nearest drill
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
        print(f"Miner at {self.pos} is resting to regain stamina.")  # Print when the miner is resting

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
                print(f"Engineer at {self.pos} moving towards broken drill at {nearest_broken_drill.pos}.")
                if self.is_near_drill(nearest_broken_drill):
                    self.repair(nearest_broken_drill)  # Repair the drill if near
                else:
                    self.move_towards(nearest_broken_drill.pos)  # Move towards the broken drill
            else:
                self.move()  # Move randomly if no broken drill is found
                print(f"Engineer at {self.pos} is moving randomly.")
        else:
            self.rest()  # Rest when stamina is depleted
            print(f"Engineer at {self.pos} is resting to regain stamina.")

    def find_nearest_broken_drill(self):
        """Find the nearest broken drill on the grid."""
        drills = [
            agent for agent in self.model.agents
            if isinstance(agent, Drill) and agent.is_broken()
        ]
        if drills:
            nearest_drill = min(drills, key=lambda drill: abs(self.pos[0] - drill.pos[0]) + abs(self.pos[1] - drill.pos[1]))
            print(f"Nearest broken drill found at {nearest_drill.pos}.")
            return nearest_drill
        print("No broken drills found.")
        return None

    def is_near_drill(self, drill):
        """Check if the engineer is adjacent to the drill (within one step)."""
        return abs(self.pos[0] - drill.pos[0]) <= 1 and abs(self.pos[1] - drill.pos[1]) <= 1

    def repair(self, drill):
        """Repair the drill."""
        if drill.is_broken():
            print(f"Engineer at {self.pos} repairing drill at {drill.pos}.")
            drill.repair()
            self.stamina = max(0, self.stamina - 10)  # Reduce stamina but ensure it doesn't go below 0
        else:
            print(f"Drill at {drill.pos} is not broken.")

    def rest(self):
        """Regain stamina when resting."""
        super().rest()  # Call the base class's rest method
        if self.stamina < 100:
            self.stamina = min(100, self.stamina + 10)  # Increment stamina towards full
            print(f"Engineer at {self.pos} is resting. Current stamina: {self.stamina}.")


class Farmer(BaseHumanAgent):
    def __init__(self, model, stamina=69):
        super().__init__(model, stamina)

    def step(self):
        if self.model.is_night:  # Check if it's nighttime
            lifepod = self.get_lifepod()
            if lifepod:
                print(f"Farmer at {self.pos} moving towards Lifepod at {lifepod.pos} during the night.")
                if self.pos != lifepod.pos:  # If not at the Lifepod, move towards it
                    self.move_towards(lifepod.pos)
                else:
                    print(f"Farmer at {self.pos} is staying at the Lifepod during the night.")
        else:  # Daytime actions
            if self.stamina > 0:
                nearest_greenhouse = self.find_nearest_greenhouse()  # Find the nearest greenhouse
                
                if nearest_greenhouse:
                    # Move towards the greenhouse until the farmer is near it
                    if not self.near_greenhouse(nearest_greenhouse):
                        self.move_towards(nearest_greenhouse.pos)
                        print(f"Farmer at {self.pos} is moving towards greenhouse at {nearest_greenhouse.pos}.")
                    else:
                        self.collect_food(nearest_greenhouse)  # Collect food if near the greenhouse
                else:
                    print("No greenhouse found.")
            else:
                self.rest()  # Rest when stamina is depleted

    def collect_food(self, greenhouse):
        """Collect food from the greenhouse and store in the Lifepod."""
        if greenhouse.food > 0:
            collected_food = 5  # The farmer collects 5 units of food
            greenhouse.food -= collected_food  # Reduce food from the greenhouse
            print(f"Farmer collected {collected_food} food from greenhouse at {self.pos}.")
            
            lifepod = self.get_lifepod()
            if lifepod:
                lifepod.store_food(collected_food)  # Store collected food in the Lifepod

            # Decrease stamina only when collecting food
            self.stamina = max(self.stamina - 5, 0)  # Decrease stamina for collecting food
        else:
            print(f"Greenhouse at {self.pos} has no food left.")

    def find_nearest_greenhouse(self):
        """Find the nearest greenhouse on the grid."""
        greenhouses = [agent for agent in self.model.agents if isinstance(agent, Greenhouse)]
        if greenhouses:
            nearest_greenhouse = min(greenhouses, key=lambda greenhouse: abs(greenhouse.pos[0] - self.pos[0]) + abs(greenhouse.pos[1] - self.pos[1]))
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
