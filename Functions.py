import pickle
import Globals
from ursina import *
import random
from noise import pnoise2
from Plants import FoodBlob
import os
import time

def sweep_and_prune():
    valid_cubes = [cube for cube in Globals.ai_cubes if cube.enabled and not cube.is_empty()]
    sorted_cubes = sorted(valid_cubes, key=lambda cube: cube.x - cube.scale_x / 2)
    potential_collisions = []

    for i in range(len(sorted_cubes)):
        for j in range(i + 1, len(sorted_cubes)):
            cube1, cube2 = sorted_cubes[i], sorted_cubes[j]
            if cube2.x - cube2.scale_x / 2 > cube1.x + cube1.scale_x / 2:
                break
            potential_collisions.append((cube1, cube2))

    return potential_collisions

def update_diet_counts():
    herbivore_count, omnivore_count, carnivore_count = Globals.herbivore_count, Globals.omnivore_count, Globals.carnivore_count
    # Count diets
    for cube in Globals.ai_cubes:
        if cube.diet == 'herbivore':
            herbivore_count += 1
        elif cube.diet == 'omnivore':
            omnivore_count += 1
        elif cube.diet == 'carnivore':
            carnivore_count += 1

    print()
    print("#" + "-" * 40 + "#")
    print("Herbivore count-: ", herbivore_count)
    print("#" + "-" * 40 + "#")
    print("Omnivore count-: ", omnivore_count)
    print("#" + "-" * 40 + "#")
    print("Carnivore count-: ", carnivore_count)
    print("#" + "-" * 40 + "#")
    print()

def adjust_rgb(r, g, b, r_adjust=0, g_adjust=0, b_adjust=0, min_brightness=200):
    # Adjust each component and ensure it's within the 0-255 range
    r_final = max(0, min(255, r + r_adjust))
    g_final = max(0, min(255, g + g_adjust))
    b_final = max(0, min(255, b + b_adjust))

    # Check if the brightness is below the minimum threshold
    if (r_final + g_final + b_final) < min_brightness:
        # Calculate the difference needed to reach the minimum brightness
        diff = min_brightness - (r_final + g_final + b_final)
        # Distribute the difference evenly across the RGB components
        increase = diff // 344
        r_final, g_final, b_final = r_final + increase, g_final + increase, b_final + increase
        # Adjust for rounding errors by adding the remaining difference to the red component
        r_final += diff % 3

    return max(0, min(255, r_final)), max(0, min(255, g_final)), max(0, min(255, b_final))


def generate_food():
    x = random.uniform(1, Globals.width - 1) * Globals.size_factor  # Scale x position
    z = random.uniform(1, Globals.width - 1) * Globals.size_factor  # Scale z position
    y = get_terrain_height(x, z)  # Function to get the terrain height at x, z

    # Now place the food blob at (x, y, z)
    food_blob = FoodBlob(position=(x, y, z), growth_stage=random.randint(3, 5))
    Globals.food_blobs.append(food_blob)

def get_terrain_height(x, z):
    return pnoise2(x / (Globals.freq * Globals.size_factor), z / (Globals.freq * Globals.size_factor)) * Globals.amp


def calculate_size_offset(creature_size):
    # Example: simple linear relationship between creature size and height offset
    offset_factor = 0.1  # Adjust this factor based on your game's scaling and needs
    return creature_size * offset_factor


def get_terrain_height_creature(x, z, creature_size):
    base_height = pnoise2(x / (Globals.freq * Globals.size_factor), z / (Globals.freq * Globals.size_factor)) * Globals.amp
    size_adjusted_height = base_height + calculate_size_offset(creature_size)
    return size_adjusted_height

def load_simulation_state():
    from Animals import AICube
    ai_cubes = Globals.ai_cubes # Ensure we're modifying the global list of AICubes

    # Load the saved AICube data from the file
    with open('simulation_state.pkl', 'rb') as file:
        saved_data = pickle.load(file)

    # Clear the current AICube state before loading new ones
    ai_cubes.clear()

    # Restore AICubes from their saved data
    for saved_cube_dict in saved_data['ai_cubes']:
        # Temporarily store the scale value if it exists and remove it from the dictionary
        scale_value = saved_cube_dict.pop('scale', None)  # Default to None if 'scale' is not in the dictionary

        # Unpack the dictionary directly into the AICube constructor
        new_cube = AICube(**saved_cube_dict)

        # If there was a scale value, set it directly on the new instance
        if scale_value is not None:
            new_cube.scale = scale_value  # This assumes 'scale' can be directly assigned like this

        ai_cubes.append(new_cube)

    print("AICubes state successfully loaded!")

def update_environment():
    current_time = time.time()
    if current_time - Globals.last_environment_change > Globals.environment_cycle_duration:
        # Change the environment condition
        if Globals.environment_condition == 'normal':
            Globals.environment_condition = random.choice(['drought', 'plentiful'])
        else:
            Globals.environment_condition = 'normal'
        Globals.last_environment_change = current_time

def save_simulation_state():
    ai_cubes = Globals.ai_cubes

    # Check if a save file already exists
    save_file_name = 'simulation_state.pkl'
    backup_file_name = 'simulation_state-BACKUP.pkl'

    # If a backup file exists, remove it
    if os.path.exists(backup_file_name):
        os.remove(backup_file_name)

    # If a save file exists, rename it to the backup file
    if os.path.exists(save_file_name):
        os.rename(save_file_name, backup_file_name)

    # Now proceed to save the current state
    ai_cubes_data = [cube.to_dict() for cube in ai_cubes if cube.to_dict() is not None]
    with open(save_file_name, 'wb') as file:
        pickle.dump({'ai_cubes': ai_cubes_data}, file)

    Globals.last_save_time = time.time()
    print("AICubes state saved and previous state backed up!")

def spawn_ai_cubes_H():
    from Animals import AICube
    for _ in range(5):
        AICube(position=(random.uniform(1, Globals.width * Globals.size_factor - 1), 0, random.uniform(1, Globals.width - 1)),
               vision_range=random.randrange(10, 30), move_distance=random.randrange(50, 70),
               RGB=(0, 255, 255), size=1, diet='herbivore',
               offspring=1, speed=round(random.uniform(0.1, 0.3) * Globals.speed_factor))


def spawn_ai_cubes_O():
    from Animals import AICube
    for _ in range(5):
        AICube(position=(random.uniform(1, Globals.width * Globals.size_factor - 1), 0, random.uniform(1, Globals.width - 1)),
               vision_range=random.randrange(10, 30), move_distance=random.randrange(50, 70),
               RGB=(155, 20, 255), size=2, diet='omnivore',
               offspring=1, speed=round(random.uniform(0.1, 0.3) * Globals.speed_factor))


def spawn_ai_cubes_C():
    from Animals import AICube
    for _ in range(5):
        AICube(position=(random.uniform(1, Globals.width * Globals.size_factor - 1), 0, random.uniform(1, Globals.width - 1)),
               vision_range=random.randrange(20, 30), move_distance=random.randrange(50, 70), RGB=(194, 255, 10),
               size=random.randrange(3,5), diet='carnivore',
               offspring=1, speed=round(random.uniform(0.1, 0.3) * Globals.speed_factor))


def spawn_ai_cubes_R():
    from Animals import AICube
    for _ in range(random.randrange(2, 20)):
        AICube(position=(random.uniform(1, Globals.width * Globals.size_factor - 1), 0, random.uniform(1, Globals.width - 1)),
               vision_range=random.randrange(20, 30), move_distance=random.randrange(50, 70),
               RGB=(random.randrange(100, 255), random.randrange(100, 255), random.randrange(100, 255)),
               size=round(random.randrange(1, 3)), diet=random.choice(['carnivore', 'omnivore', 'herbivore']),
               offspring=1, speed=round(random.uniform(0.1, 0.3) * Globals.speed_factor))


def remove_oldest_from_successful_diet():
    # Step 1: Identify the most successful diet group
    ai_cubes = Globals.ai_cubes
    diet_counts = {'herbivore': 0, 'omnivore': 0, 'carnivore': 0}
    for cube in ai_cubes:
        if cube.diet in diet_counts:
            diet_counts[cube.diet] += 1

    successful_diet = max(diet_counts, key=diet_counts.get)

    # Step 2: Filter creatures by the successful diet
    successful_creatures = [cube for cube in ai_cubes if cube.diet == successful_diet]

    # Step 3: Sort by age and remove the oldest 5-10 creatures
    successful_creatures.sort(key=lambda x: x.age, reverse=True)
    number_to_remove = min(len(successful_creatures), 10)  # Adjust this number if you want to remove a different amount

    for _ in range(number_to_remove):
        oldest = successful_creatures.pop(0)  # Remove the oldest creature from the list
        if oldest in ai_cubes:
            ai_cubes.remove(oldest)  # Make sure to also remove it from the main ai_cubes list
            destroy(oldest, delay=1 / 60)

def extract_rgb_from_signature(signature):
    # Assuming the first part of the signature contains the RGB information
    # Here we need to extract the RGB values from the genetic signature string
    # The exact implementation may vary depending on how the genetic signature is structured
    rgb_str = signature[:6]  # Assuming the first 6 characters represent the RGB in hexadecimal
    r = int(rgb_str[:2], 16)
    g = int(rgb_str[2:4], 16)
    b = int(rgb_str[4:6], 16)
    return r, g, b