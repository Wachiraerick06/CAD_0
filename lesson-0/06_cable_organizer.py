"""
Example 6: Cable Organizer
Parametric slot count and sizes.
"""

import cadquery as cq
from export_helper import export_all

# Parameters
n_slots = 6
slot_w = 8.0        # Slot width
slot_d = 20.0       # Slot depth
wall = 3.0          # Wall between slots
base_h = 8.0        # Base height
slot_h = 25.0       # Slot height above base

total_w = n_slots * slot_w + (n_slots + 1) * wall
depth = slot_d + 2 * wall
total_h = base_h + slot_h

# Main body
body = (
    cq.Workplane("XY")
    .box(total_w, depth, total_h)
    .translate((0, 0, total_h / 2))
)

# Cut slots from the top
slot_start_x = -total_w / 2 + wall + slot_w / 2
slots_shape = cq.Workplane("XY").workplane(offset=base_h)

for i in range(n_slots):
    x = slot_start_x + i * (slot_w + wall)
    slots_shape = (
        slots_shape
        .center(x, 0)
        .rect(slot_w, slot_d)
        .center(-x, 0)
    )

slots_solid = slots_shape.extrude(slot_h + 1)

# Round vertical edges of the body
body = body.edges("|Z").fillet(2.0)

# Cut slots
organizer = body.cut(slots_solid)

# Chamfer slot entry edges
organizer = organizer.faces(">Z").edges().chamfer(0.8)

print(f"Cable organizer: {n_slots} slots, {total_w:.0f}mm wide")
export_all(organizer, "06_cable_organizer", (0, 140, 140))