import uuid

from Functions import *
from DB import monitor_subspecies_evolution, construct_genetic_signature
import Globals


def random_direction():
    angle = random.uniform(0, 2 * math.pi)
    return Vec3(math.cos(angle), 0, math.sin(angle))


class AICube(Entity):
    def __init__(self, position=(0, 0, 0), vision_range=5, move_distance=60, speed=0.01, RGB=(192, 149, 255),
                 size=0, diet='herbivore', offspring=1, parent=None, **kwargs):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            color=color.rgb(*RGB),
            scale=(size, size, size),
            collider='box',
            offspring=1,
            **kwargs
        )
        self.position = position
        self.hunt_cooldown = 0
        self.vision_range = vision_range
        self.move_distance = move_distance
        self.speed = speed  # self.apply_size_penalty_to_speed(speed, size)
        self.food = 40
        self.target_food = None
        self.target_direction = random_direction()
        self.moved_distance = 0
        self.age = 0
        self.max_age = random.randrange(70, 100)
        self.size = size
        self.RGB = RGB
        self.mutations = ["vision_range", "move_distance", "speed", "size", "offspring_count"]
        self.diet = diet
        self.offspring_count = offspring
        self.breeding_cooldown = 0
        self.cube_id = str(uuid.uuid4())  # Assign a unique ID
        self.parent_id = parent.cube_id if parent else None
        Globals.ai_cubes.append(self)
        Globals.Species_logger.append(self)
        """     
        if transfer_threshold is None:
            self.transfer_threshold = random.randrange(3, 9)
        else:
            self.transfer_threshold = transfer_threshold

        self.instinct = {"positive": [], "negative": []}  # used to transfer information useful throughout generations based on chance, gets the data from long term memory

        self.short_term = {"positive": [], "negative": []} # used to store up to 10 positions that could be good or harmful, gets the data from the terrain
        self.long_term = {"positive": [], "negative": []} # used to store a near unlimited amount of positions that could be good or harmful gets the data from short term memory
        """

        """
    def manage_memory(self, position, category, memory_bank="short_term"):
        # Validate category
        if category not in ["positive", "negative"]:
            raise ValueError("Category must be 'positive' or 'negative'.")

        # Add position to the specified memory bank
        getattr(self, memory_bank)[category].append(position)

        # Promotion from short-term to long-term memory
        if memory_bank == "short_term" and self.short_term[category].count(position) >= self.short_term_threshold:
            self.short_term[category] = [pos for pos in self.short_term[category] if
                                         pos != position]  # Remove from short-term
            self.long_term[category].append(position)  # Add to long-term

        # Promotion from long-term memory to instinct
        if self.long_term[category].count(position) >= self.long_term_threshold:
            self.long_term[category] = [pos for pos in self.long_term[category] if
                                        pos != position]  # Remove from long-term
            if position not in self.instinct[category]:  # Avoid duplicates in instinct
                self.instinct[category].append(position)  # Add to instinct
                """

    def to_dict(self):
        if hasattr(self, 'enabled') and self.enabled:  # Check if the entity is still valid
            return {
                'position': self.position,  # Assuming position is Vec3 and serializable
                'vision_range': self.vision_range,
                'move_distance': self.move_distance,
                'speed': self.speed,
                'RGB': self.RGB,
                'size': self.size,
                'diet': self.diet,
                'offspring_count': self.offspring_count,
                'parent': self.parent_id,
                # Include other relevant attributes
            }
        else:
            return None  # Or some indication that the entity is no longer valid

    def move(self):
        potential_collisions = sweep_and_prune()
        for cube1, cube2 in potential_collisions:
            if cube1 == self or cube2 == self:
                other_cube = cube2 if cube1 == self else cube1
                direction_to_other = (other_cube.position - self.position).normalized()
                distance_to_other = (other_cube.position - self.position).length()
                min_allowed_distance = self.scale_x / 2 + other_cube.scale_x / 2
                if distance_to_other < min_allowed_distance:
                    self.target_direction -= direction_to_other * (
                            min_allowed_distance - distance_to_other) / min_allowed_distance

        self.target_direction = self.target_direction.normalized()
        if self.hunt_cooldown > 0:
            self.target_direction = self.target_direction
            self.hunt_cooldown -= time.dt

        elif self.target_food:
            direction_to_food = (self.target_food.position - self.position).normalized()
            self.target_direction += direction_to_food * 0.8

        if self.x <= 1 or self.x >= Globals.width - 1 or self.z <= 1 or self.z >= Globals.width - 1:
            edge_avoidance = Vec3(-self.target_direction.x, 0, -self.target_direction.z)
            self.target_direction += edge_avoidance * 0.5
        self.target_direction = self.target_direction.normalized()
        self.position += self.target_direction * self.speed
        self.x = clamp(self.x, 1, Globals.width * Globals.size_factor - 1)
        self.z = clamp(self.z, 1, Globals.width * Globals.size_factor - 1)
        self.y = get_terrain_height_creature(self.x, self.z, self.size)

    def find_nearest_food_within_vision(self):
        nearest_blob = None
        nearest_prey = None
        min_blob_distance = float('inf')
        min_prey_distance = float('inf')

        for food in Globals.food_blobs:
            if not food:  # Enhanced check for food blob validity
                continue

            dist = (self.position - food.position).length()
            if dist < min_blob_distance:
                min_blob_distance = dist
                nearest_blob = food

        if self.diet in ['carnivore', 'omnivore']:
            for cube in Globals.ai_cubes:
                if not cube or cube == self or cube.size >= self.size or getattr(cube, 'is_targeted',
                                                                                 False):
                    continue

                dist = (self.position - cube.position).length()
                if dist < min_prey_distance:
                    min_prey_distance = dist
                    nearest_prey = cube

        # Decide on the target food based on the diet
        if self.diet == 'omnivore':
            if random.random() < 0.4:
                self.target_food = nearest_blob if nearest_blob else None
            else:
                self.target_food = nearest_prey if nearest_prey and not hasattr(nearest_prey, 'is_targeted') else None
        elif self.diet == 'herbivore':
            self.target_food = nearest_blob if nearest_blob else None
        elif self.diet == 'carnivore':
            self.target_food = nearest_prey if nearest_prey and not hasattr(nearest_prey, 'is_targeted') else None

        # Mark the target as targeted if a target has been selected
        if self.target_food and not hasattr(self.target_food, 'is_targeted'):
            self.target_food.is_targeted = True

    def update(self):
        ai_cubes, food_blobs, paused, start_time, plant_cooldown, last_save_time = Globals.ai_cubes, \
            Globals.food_blobs, Globals.paused, Globals.start_time, Globals.plant_cooldown, Globals.last_save_time

        current_time = time.time()
        if current_time - Globals.last_save_time > Globals.save_interval:
            save_simulation_state()
            monitor_subspecies_evolution(Globals.Species_logger)

        if paused:
            pass
        else:
            self.move()
            self.find_nearest_food_within_vision()
            self.check_stats()

            # Check if target_food is valid and not destroyed before interacting
            if self.target_food and hasattr(self.target_food,
                                            'enabled') and self.target_food.enabled:
                distance_to_target = (self.position - self.target_food.position).length()
                min_distance_to_interact = self.scale_x / 2 + self.target_food.scale_x / 2
                if distance_to_target < min_distance_to_interact:
                    if self.diet == 'carnivore' and isinstance(self.target_food, AICube):
                        self.attempt_eat_ai_cube()
                    elif self.diet == 'herbivore' and isinstance(self.target_food, FoodBlob):
                        self.attempt_eat_food_blob()
                    elif self.diet == 'omnivore':
                        if isinstance(self.target_food, FoodBlob):
                            self.attempt_eat_food_blob()
                        elif isinstance(self.target_food, AICube):
                            self.attempt_eat_ai_cube()

                    if hasattr(self.target_food, 'is_targeted'):
                        del self.target_food.is_targeted
                    self.target_food = None

        if len(ai_cubes) >= 100:
            sorted_cubes = sorted(ai_cubes, key=lambda cube: cube.age, reverse=True)
            for _ in range(round(random.randrange(10, 20))):
                oldest_cube = sorted_cubes.pop(0)
                if oldest_cube in ai_cubes:
                    ai_cubes.remove(oldest_cube)
                    destroy(oldest_cube, delay=1 / 60)

        if len(food_blobs) < 100:
            if Globals.environment_condition == "drought":
                for _ in range(40):
                    generate_food()
            elif Globals.environment_condition == "plentiful":
                for _ in range(96):
                    generate_food()
            else:
                for _ in range(68):  # standard
                    generate_food()

        if time.time() - Globals.creature_introducer == 600:
            spawn_ai_cubes_R()

    def attempt_eat_ai_cube(self):
        if isinstance(self.target_food, AICube) and random.random() > 0.4:
            self.eat_other_cube(self.target_food)
            self.hunt_cooldown = 5

    def attempt_eat_food_blob(self):
        if isinstance(self.target_food, FoodBlob):
            self.eat_food_blob()

    def eat_food_blob(self):
        if (self.target_food and hasattr(self.target_food, 'enabled') and
                self.target_food.enabled):
            food_value = 2 * self.target_food.growth_stage  # Food value based on growth stage
            self.food += food_value
            Globals.food_blobs.remove(self.target_food)
            destroy(self.target_food, delay=1 / 60)
            self.target_food = None

    def eat_other_cube(self, other_cube):
        if self.size > other_cube.size and not hasattr(other_cube, 'is_targeted') and random.random() > 8:
            # The food value could be a base value plus an additional amount based on the prey's size
            base_food_value = 10  # Base value for eating any cube
            size_bonus = other_cube.size * 2  # Example: bonus food value based on prey's size

            self.food += base_food_value + size_bonus  # Increase the carnivore's food by the total value
            Globals.ai_cubes.remove(other_cube)  # Remove the eaten cube from the list
            destroy(other_cube, delay=1 / 60)  # Remove the eaten cube from the scene
            self.target_food = None  # Clear the target

            if hasattr(other_cube, 'is_targeted'):
                del other_cube.is_targeted

    def removeself(self):
        destroy(self, delay=1 / 60)

    def check_stats(self):
        if self.food <= 0 or self.age >= self.max_age and not hasattr(self, 'is_targeted'):
            destroy(self, delay=1 / 60)
        elif self.food >= 30:
            self.breeding()

        if self.breeding_cooldown > 0:
            self.breeding_cooldown -= time.dt

        self.food -= 0.0003
        self.age += 0.5

    def breeding(self):
        maturity_age = 0.25 * self.max_age
        if self.age < maturity_age or self.breeding_cooldown > 0:
            return

        new_vision_range = self.vision_range
        new_move_distance = self.move_distance
        new_speed = self.speed
        new_size = self.size
        new_diet = self.diet
        new_offspring_count = self.offspring_count
        food_required = 5  # Base food requirement for breeding

        # Adjust food required for breeding based on diet and environmental factors
        if self.diet == "herbivore":
            food_required += len(Globals.ai_cubes) / len(
                Globals.food_blobs) + 1  # More herbivores than food increases breeding cost
        elif self.diet == "omnivore":
            food_required += 0.5 * len(Globals.ai_cubes) / len(
                Globals.food_blobs) + 1  # Omnivores have more food sources
        else:  # Carnivore
            prey_available = sum(1 for cube in Globals.ai_cubes if cube.size < self.size and cube.diet != 'carnivore')
            food_required += len([cube for cube in Globals.ai_cubes if cube.diet == 'carnivore']) / max(1,
                                                                                                        prey_available)

        # Check if there's enough food to breed
        if self.food < food_required:
            return  # Not enough food to breed

        self.food -= food_required  # Deduct the food cost of breeding

        # Mutation chance and effects
        mutation_chance = random.randrange(1, 10)
        epsilon = 0.1  # A very small positive value to ensure properties are greater than 0

        if mutation_chance >= 6:
            new_vision_range += random.randint(-2, 2)
            new_vision_range = max(epsilon, new_vision_range)  # Ensures vision_range is greater than 0

        mutation_chance = random.randrange(1, 10)

        if mutation_chance >= 6:
            new_move_distance += random.randint(-2, 2)
            new_move_distance = max(epsilon, new_move_distance)  # Ensures move_distance is greater than 0

        mutation_chance = random.randrange(1, 10)

        if mutation_chance >= 6:
            new_speed += random.uniform(-1, 1)
            new_speed = max(epsilon, new_speed)  # Ensures speed is greater than 0

        mutation_chance = random.randrange(1, 10)

        if mutation_chance >= 6 and new_size < 3:
            new_size += random.uniform(-1, 1)
            new_size = max(epsilon, new_size)  # Ensures size is greater than 0

        mutation_chance = random.randrange(1, 10)

        if mutation_chance >= 6:
            new_diet = random.choice(["carnivore", "herbivore", "omnivore"])  # Corrected syntax error

        # Use the genetic signature to determine the unique RGB for the offspring
        offspring_genetic_signature = construct_genetic_signature(self)
        offspring_RGB = extract_rgb_from_signature(offspring_genetic_signature)

        # Breeding new offspring
        for _ in range(new_offspring_count):
            new_cube = AICube(
                position=self.position + Vec3(random.uniform(-1, 1), 0, random.uniform(-1, 1)),
                vision_range=new_vision_range,
                move_distance=new_move_distance,
                speed=new_speed,
                RGB=offspring_RGB,  # Use the RGB extracted from the genetic signature
                size=new_size,
                diet=new_diet,
                offspring=new_offspring_count,
                parent=self
            )

        self.breeding_cooldown = 0.2 * self.max_age