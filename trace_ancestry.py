from DB import cursor
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import sqlite3

query = "SELECT cube_id FROM ancestry ORDER BY RANDOM() LIMIT 300"
cursor.execute(query)

# Fetch the results
random_creature_ids = cursor.fetchall()

# random_creature_ids will be a list of tuples, where each tuple contains one creature_id
# To get a list of IDs, you can use a list comprehension
random_creature_ids_list = [id[0] for id in random_creature_ids]

def extract_rgb_from_signature(signature):
    # Assuming the first part of the signature contains the RGB information
    # Here we need to extract the RGB values from the genetic signature string
    # The exact implementation may vary depending on how the genetic signature is structured
    rgb_str = signature[:6]  # Assuming the first 6 characters represent the RGB in hexadecimal
    r = int(rgb_str[:2], 16)
    g = int(rgb_str[2:4], 16)
    b = int(rgb_str[4:6], 16)
    return r, g, b


def display_ancestors_colors(ancestry_data):
    colors = [extract_rgb_from_signature(ancestor['genetic_signature']) for ancestor in ancestry_data]

    # Normalize RGB values to [0, 1] for Matplotlib
    colors_normalized = [(r / 255, g / 255, b / 255) for r, g, b in colors]

    num_columns = len(colors_normalized)
    fig_width = max(num_columns / 2, 5)  # Adjust figure width for better spacing

    # Create a figure and a subplot
    fig, ax = plt.subplots(figsize=(fig_width, 3))
    ax.set_xlim([0, num_columns])
    ax.set_ylim([0, 1])

    column_width = 0.8  # Width of each column
    space_width = 0.2  # Width of space between columns

    for idx, color in enumerate(colors_normalized):
        # Calculate the starting x position of each column to include space
        column_position = idx * (column_width + space_width)
        ax.add_patch(mpatches.Rectangle((column_position, 0), column_width, 1, color=color))

    ax.set_xticks([])
    ax.set_yticks([])

    plt.title('Ancestors Colors')
    plt.show()

def trace_ancestry(cube_id):
    ancestry = []
    current_id = cube_id

    while current_id:
        cursor.execute('SELECT parent_id, genetic_signature FROM ancestry WHERE cube_id = ?', (current_id,))
        result = cursor.fetchone()

        if not result:
            break  # End of lineage

        parent_id, genetic_signature = result
        ancestry.append({'cube_id': current_id, 'genetic_signature': genetic_signature})
        current_id = parent_id

    return ancestry[::-1]

#for item in random_creature_ids_list:
display_ancestors_colors(trace_ancestry("c907bd6a-2565-4edf-909c-f0a7fd4adf7d"))
