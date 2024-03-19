from noise import pnoise2
from ursina import *
from Functions import generate_food, spawn_ai_cubes_H, spawn_ai_cubes_C, spawn_ai_cubes_O, spawn_ai_cubes_R, \
    update_diet_counts, remove_oldest_from_successful_diet, load_simulation_state, save_simulation_state
import Globals
import DB
from DB import monitor_subspecies_evolution

app = Ursina()

def generate_terrain():
    for x in range(1, Globals.width):
        for z in range(1, Globals.width):
            scaled_x = x * Globals.size_factor
            scaled_z = z * Globals.size_factor
            scaled_x_minus_one = (x - 1) * Globals.size_factor
            scaled_z_minus_one = (z - 1) * Globals.size_factor

            # Calculate the y values at these scaled positions
            y00 = pnoise2(scaled_x / Globals.freq, scaled_z / Globals.freq) * Globals.amp
            y10 = pnoise2(scaled_x_minus_one / Globals.freq, scaled_z / Globals.freq) * Globals.amp
            y11 = pnoise2(scaled_x_minus_one / Globals.freq, scaled_z_minus_one / Globals.freq) * Globals.amp
            y01 = pnoise2(scaled_x / Globals.freq, scaled_z_minus_one / Globals.freq) * Globals.amp

            # Use the scaled x and z values for the vertices
            Globals.level_parent.model.vertices.extend([
                (scaled_x, y00, scaled_z), (scaled_x_minus_one, y10, scaled_z),
                (scaled_x_minus_one, y11, scaled_z_minus_one),
                (scaled_x, y00, scaled_z), (scaled_x_minus_one, y11, scaled_z_minus_one),
                (scaled_x, y01, scaled_z_minus_one)
            ])
    Globals.level_parent.model.generate()
    Globals.level_parent.model.project_uvs()
    Globals.level_parent.model.generate_normals()

    for _ in range(1000):
        generate_food()


def input(key):
    if key == '1':
        spawn_ai_cubes_H()

    elif key == "2":
        spawn_ai_cubes_O()

    elif key == "3":
        spawn_ai_cubes_C()

    elif key == "p":
        for _ in range(5):
            generate_food()

    elif key == "t":
        for _ in Globals.ai_cubes:
            Globals.ai_cubes.remove(_)
            destroy(_, delay=1 / 60)
            _.removeself()
    elif key == "r":
        remove_oldest_from_successful_diet()

    elif key == "4":
        update_diet_counts()

    elif key == "5":
        if window.fullscreen is True:
            window.fullscreen = False
        else:
            window.fullscreen = True

    elif key == "6":
        if Globals.paused:
            Globals.paused = False
        else:
            Globals.paused = True

    elif key == "7":
        monitor_subspecies_evolution(Globals.Species_logger)
        save_simulation_state()
        application.quit()

    elif key == "8":
        save_simulation_state()

    elif key == "9":
        load_simulation_state()

    elif key == "0":
        spawn_ai_cubes_R()

    elif key == "q":
        i = 1
        print()
        print("-" * 40)

        for cube in Globals.ai_cubes:
            print(f"cube {i}-:", cube.id)

        print("-" * 40)
        print()



#load_simulation_state()
generate_terrain()
EditorCamera()
app.run()

DB.conn.close()

