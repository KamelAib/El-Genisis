# El-Genisis 

## Introduction

While observing a seemingly mundane interaction between birds over a slice of bread in a park, a profound question arose: How does human alteration of natural landscapes impact the evolutionary trajectories and ecosystems of the animal inhabitants? This curiosity led to the development of el-genisis, a project dedicated to exploring the intricate dynamics between human-modified environments and wildlife through the lens of a controlled simulation.

Human activities have reshaped the Earth's landscapes, introducing new challenges and opportunities for wildlife. The creation of parks and urban green spaces, while beneficial for human recreation and aesthetics, introduces artificial ecosystems where wildlife must adapt or perish. These human-made habitats often become arenas of intense competition among species not typically found together, accelerating changes in behavior and evolutionary paths.

El-genisis simulates this phenomenon, creating a digital microcosm where artificial life forms, termed AiCubes, compete, evolve, and adapt over generations within a user-defined environment. This project aims to shed light on the broader implications of our environmental interventions and foster a deeper understanding of the delicate balance between conservation efforts and the natural adaptability of ecosystems.

## Methodology

El-genisis employs a simulated environment crafted with the Ursina engine, a python-based game engine renowned for its simplicity and effectiveness. This digital ecosystem serves as a controlled space where the dynamics of evolution and competition among species can be observed and analyzed.

### Simulation Environment Setup

- **Terrain**: Dynamically generated using Perlin noise to ensure a unique landscape for each simulation run, emulating the variability of natural environments.
- **Flora and Fauna**: The simulation includes two primary entities: AiCube (animal analogs) and FoodBlob (plant analogs), initiating a basic predator-prey dynamic essential for ecological studies.

### Evolutionary Mechanisms

- **Breeding and Mutation**: AiCubes are programmed to reproduce based on their survival success, with offspring inheriting a mix of parental traits subject to random mutations. These mutations introduce variability and the potential for evolutionary adaptations.
- **Environmental Influences**: The simulation offers a range of controls to mimic human impacts on the environment, such as altering resource availability or introducing invasive species, allowing for a nuanced exploration of human-wildlife interactions.

### Data Collection and Analysis

El-genisis features a comprehensive data collection system, logging a wealth of information from individual traits to population dynamics. This enables in-depth analysis of evolutionary trends and the ecological impact of introduced changes.

### Ancestry Tracing

A unique aspect of the simulation is its ability to trace the lineage of each AiCube, offering insights into the evolutionary pathways and the effects of specific mutations over generations.

## Interpretation of Results

To extract meaningful insights, el-genisis compares the outcomes of various simulation scenarios against a control group representing a stable, untouched ecosystem. By introducing controlled variables and observing their impacts, the project aims to simulate the effect of invasive species and other human-induced changes, providing a theoretical framework to understand real-world ecological challenges.

## Controls

The simulation provides a variety of controls to interact with and manipulate the environment. These controls are activated through keyboard input and allow you to perform actions ranging from spawning AI entities to saving and loading simulation states. Here's a detailed breakdown:

- **`1`**: Spawns Herbivore AiCubes (`spawn_ai_cubes_H`). Herbivores are one of the primary consumers in the simulation, feeding on plant life and avoiding predators.

- **`2`**: Spawns Omnivore AiCubes (`spawn_ai_cubes_O`). Omnivores can consume both plant matter and other AI entities, providing a flexible dietary niche within the ecosystem.

- **`3`**: Spawns Carnivore AiCubes (`spawn_ai_cubes_C`). Carnivores are at the top of the food chain, preying on other AI entities to survive.

- **`0`**: Spawns Randomly generated AiCubes (`spawn_ai_cubes_R`). These AI entities have randomly assigned traits, introducing an element of unpredictability and diversity to the ecosystem.

- **`p`**: Generates additional food sources (`generate_food`). By pressing this key, you add more plant life to the simulation, potentially affecting the balance between consumers and resources.

- **`t`**: Terminates all AiCubes. This command removes all AI entities from the simulation, effectively resetting the animal population.

- **`r`**: Removes the oldest entities from the most successful dietary group (`remove_oldest_from_successful_diet`). This control simulates natural selection by culling older members of the most populous group, potentially promoting genetic diversity.

- **`4`**: Updates the count of each dietary type (`update_diet_counts`). This function recalculates the number of entities in each dietary category, useful for monitoring population dynamics.

- **`5`**: Toggles fullscreen mode. This control allows you to switch between fullscreen and windowed modes, enhancing your viewing experience.

- **`6`**: Pauses or resumes the simulation (`Globals.paused`). This toggle provides a way to halt the simulation's progress, allowing for closer inspection or adjustments.

- **`7`**: Saves the current state and exits (`save_simulation_state`). This command saves all current simulation data and closes the application, ensuring no progress is lost.

- **`8`**: Saves the current simulation state without exiting. Use this control to create a checkpoint without terminating the session.

- **`9`**: Loads a previously saved simulation state (`load_simulation_state`). This control allows you to revert to a past state, useful for exploring different outcomes from a fixed point in time.

- **`q`**: Lists the ID of each AiCube. This command prints a roster of all active AI entities, providing insight into the population structure and individual members.

## Credit where its due GPT wrote the Readme file as im too lazy and its 3:54 AM
