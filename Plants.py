from ursina import *
import random
"""
class FoodBlob(Entity):
    def __init__(self, position=(0, 0, 0), produce=None, plant_type=None, **kwargs):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            color=color.lime,
            collider='box',
            **kwargs
        )
        self.original_scale = Vec3(1, 1, 1)  # Assuming the original scale is 1 in all dimensions
        self.produce_count = random.randrange(3, 6)
        self.growth_time = random.randrange(1, 5)  # in seconds
        self.last_growth = time.time()
        self.growth_increment = 1.1  # Up to 10% growth
        self.max_scale = self.original_scale * 1.1  # Maximum scale is 110% of the original
        self.plant_type = plant_type if plant_type else random.choice(["grass", "bush", "tree"])
        self.produce = produce
        if not produce and self.plant_type in ["tree", "bush"]:
            self.produce = random.choice(["leaves", "fruits"])

    def update(self):
        if time.time() - self.last_growth >= self.growth_time:
            self.generate_produce()
            self.last_growth = time.time()  # Reset last growth time

    def generate_produce(self):
        if self.plant_type in ["bush", "tree"]:
            if self.produce == "leaves":
                # Increase scale for leaves, but not beyond the maximum allowed scale
                new_scale = Vec3(min(self.scale_x * self.growth_increment, self.max_scale.x),
                                 min(self.scale_y * self.growth_increment, self.max_scale.y),
                                 min(self.scale_z * self.growth_increment, self.max_scale.z))
                self.scale = new_scale
            elif self.produce == "fruits":
                # Generate fruits around the plant within a certain radius
                for _ in range(self.produce_count):
                    offset = Vec3(random.uniform(-1, 1), 0, random.uniform(-1, 1)) * 0.5  # Within a 0.5 unit radius
                    FoodBlob(position=self.position + offset, produce="fruit", plant_type="fruit")
        elif self.plant_type == "grass":
            # Grass behavior, maybe just a simple scale increase like leaves, but not beyond the maximum allowed scale
            new_scale = Vec3(min(self.scale_x * self.growth_increment, self.max_scale.x),
                             min(self.scale_y * self.growth_increment, self.max_scale.y),
                             min(self.scale_z * self.growth_increment, self.max_scale.z))
            self.scale = new_scale

    def consume_produce(self):
        # When produce is consumed, reset the scale to the original size
        self.scale = self.original_scale
"""

class FoodBlob(Entity):
    def __init__(self, position=(0, 0, 0), growth_stage=1, **kwargs):
        self.growth_stage = growth_stage
        scale_factor = growth_stage * 0.2  # Scale factor based on growth stage
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            color=color.lime,
            scale=(scale_factor, scale_factor, scale_factor),
            collider='box',
            **kwargs
        )