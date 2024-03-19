from ursina import *
import time
import random


start_time = time.time()
freq = round(random.uniform(1, 24))
amp = round(random.uniform(1, 8))
width = 100
size_factor = 2
paused = False
food_blobs = []
ai_cubes = []
Species_logger = []
new_creatures_counter = 0
herbivore_count = 0
omnivore_count = 0
carnivore_count = 0
environment_condition = 'normal'
last_environment_change = time.time()
environment_cycle_duration = 60
plant_cooldown = time.time()
speed_factor = 50
creature_introducer = time.time()
last_save_time = time.time()
save_interval = 3600
level_parent = Entity(model=Mesh(vertices=[], uvs=[]), color=color.white, scale=(0.5 * size_factor, 1, 0.5 * size_factor))
