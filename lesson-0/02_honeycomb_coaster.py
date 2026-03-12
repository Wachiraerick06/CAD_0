"""
Example 2: Honeycomb Coaster
Nested loop + hex math generates a perfect pattern.
"""

import cadquery as cq
import math
from export_helper import export_all

# Parameters
hex_r = 5.0         # Hex cell outer radius
wall = 1.2          # Wall between hexagons
depth = 3.0         # Pocket depth
base_t = 2.0        # Base thickness
coaster_r = 45.0    # Overall coaster radius

pitch = hex_r * 2 + wall
row_h = pitch * math.sqrt(3) / 2

# Base disc
coaster = cq.Workplane("XY").cylinder(base_t + depth, coaster_r)

# Cut hexagonal pockets
hex_pts = []
for row in range(-8, 9):
    for col in range(-8, 9):
        x = col * pitch + (row % 2) * pitch / 2
        y = row * row_h
        if math.sqrt(x**2 + y**2) + hex_r < coaster_r - 3:
            hex_pts.append((x, y))

wp = coaster.faces(">Z").workplane()
for x, y in hex_pts:
    wp = wp.center(x, y).polygon(6, hex_r * 2).center(-x, -y)

coaster = wp.cutBlind(-depth)

# Round the outer rim
coaster = coaster.edges("|Z").fillet(1.5)

print(f"Honeycomb coaster: {len(hex_pts)} hexagonal pockets")
export_all(coaster, "02_honeycomb_coaster", (218, 165, 32))