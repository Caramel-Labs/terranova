"""
# Agents

Agents include human settlers and the various structures they interact with inside the colony.

## Human Agents

Human agents can be found in `agents.humans`. These include:

1. `Engineer` - the Engineer travels to structures when their health has depleted and repairs them.
When idle, the Engineer roams around randomly.
2. `Farmer` - the Farmer moves between the Greenhouse and the Lifepod, collecting food from the Greenhouse.
3. `Miner` - the Miner collects iron from the Drill when it has accumulated a significant amount of iron.

Human agents are subclassed from `agents.base.BaseHumanAgent`.

## Structure Agents

Structures are also Mesa agents, which can be found in `agents.structures`. These include:

1. `Lifepod` - the Lifepod is where the humans start exploring the colony.
Humans return to the colony during night-time, and when returning collected resources.
2. `Greenhouse` - the Greenhouse grows food, which provide energy to the humans.
3. `Drill` - the Drill collects iron, which can be used to build new structures.
4. `Scrubber` - the Scrubber produces oxygen for the humans.
"""
