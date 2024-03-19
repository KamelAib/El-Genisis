import sqlite3
import time
from Globals import start_time  # Ensure Globals module has a start_time variable

# Function to convert a cube's diet into a numeric code
def diet_to_number(diet):
    diets = {'herbivore': 1, 'omnivore': 2, 'carnivore': 3}
    return diets.get(diet, 0)  # Default to 0 if diet is not recognized

# Function to convert RGB values to a single number
def rgb_to_number(rgb):
    return rgb[0] * 256**2 + rgb[1] * 256 + rgb[2]

# Function to construct a genetic signature for a cube
def construct_genetic_signature(cube):
    rgb_number = rgb_to_number(cube.RGB)
    size_str = str(int(cube.size)).zfill(2)  # Ensures size is a 2-digit string
    diet_number = diet_to_number(cube.diet)
    return f"{rgb_number}{size_str}{diet_number}"

# Establish a connection to the SQLite3 database
conn = sqlite3.connect('subspecies.db')
cursor = conn.cursor()

# Create tables for subspecies, diets, and ancestry tracking
cursor.execute('''
CREATE TABLE IF NOT EXISTS subspecies (
    genetic_signature TEXT PRIMARY KEY,
    population INTEGER,
    average_speed REAL,
    average_vision_range REAL,
    average_size REAL,
    diet TEXT,
    logged_at REAL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS diets (
    diet TEXT PRIMARY KEY,
    population INTEGER,
    logged_at REAL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS ancestry (
    cube_id TEXT PRIMARY KEY,
    parent_id TEXT,
    genetic_signature TEXT,
    FOREIGN KEY (parent_id) REFERENCES ancestry(cube_id)
)
''')

conn.commit()

def monitor_subspecies_evolution(cubes):
    subspecies_info = {}
    diet_info = {'herbivore': 0, 'omnivore': 0, 'carnivore': 0}

    for cube in cubes:
        genetic_signature = construct_genetic_signature(cube)

        if genetic_signature not in subspecies_info:
            subspecies_info[genetic_signature] = {'population': 0, 'total_speed': 0, 'total_vision_range': 0, 'total_size': 0, 'diet': cube.diet}

        subspecies = subspecies_info[genetic_signature]
        subspecies['population'] += 1
        subspecies['total_speed'] += cube.speed
        subspecies['total_vision_range'] += cube.vision_range
        subspecies['total_size'] += cube.size

        # Count the diet for each cube
        diet_info[cube.diet] += 1

        # Update ancestry information for each cube
        cursor.execute('''
            INSERT INTO ancestry (cube_id, parent_id, genetic_signature)
            VALUES (?, ?, ?)
            ON CONFLICT(cube_id) DO UPDATE SET
                parent_id = excluded.parent_id,
                genetic_signature = excluded.genetic_signature
        ''', (cube.cube_id, cube.parent_id, genetic_signature))

    # Process subspecies information
    for genetic_signature, info in subspecies_info.items():
        cursor.execute('''
            INSERT INTO subspecies (genetic_signature, population, average_speed, average_vision_range, average_size, diet, logged_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(genetic_signature) DO UPDATE SET
                population = excluded.population,
                average_speed = excluded.average_speed,
                average_vision_range = excluded.average_vision_range,
                average_size = excluded.average_size,
                diet = excluded.diet,
                logged_at = excluded.logged_at
        ''', (genetic_signature, info['population'], info['total_speed'] / info['population'],
              info['total_vision_range'] / info['population'], info['total_size'] / info['population'],
              info['diet'], time.time() - start_time))

    # Process diet information
    for diet, population in diet_info.items():
        cursor.execute('''
            INSERT INTO diets (diet, population, logged_at)
            VALUES (?, ?, ?)
            ON CONFLICT(diet) DO UPDATE SET
                population = excluded.population,
                logged_at = excluded.logged_at
        ''', (diet, population, time.time() - start_time))

    conn.commit()


