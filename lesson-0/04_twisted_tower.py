"""
Example 4: Twisted Tower
Each floor rotated and tapered by a loop, then lofted.
"""

import cadquery as cq
from export_helper import export_gradient

# Parameters
n_floors = 16
floor_h = 8.0
side = 30.0
twist_per_floor = 5.0   # degrees
taper = 0.97             # each floor slightly smaller

# Collect profile wires
wp = cq.Workplane("XY")
current_side = side
for i in range(n_floors + 1):
    z = floor_h * i
    angle = twist_per_floor * i
    wire = (
        cq.Workplane("XY")
        .workplane(offset=z)
        .transformed(rotate=(0, 0, angle))
        .rect(current_side, current_side)
        .val()
    )
    wp = wp.add(wire)
    current_side *= taper

tower = wp.toPending().loft()

print(f"Twisted tower: {n_floors} floors, {twist_per_floor} deg twist each")
export_gradient(tower, "04_twisted_tower", (30, 60, 180), (140, 40, 180))