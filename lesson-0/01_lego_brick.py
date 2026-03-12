"""
Example 1: Parametric Lego Brick
Change rows/cols, entire brick regenerates.
"""

import cadquery as cq
from export_helper import export_all

# Parameters (change these!)
rows = 4
cols = 2
unit = 8.0         # Lego unit spacing (mm)
stud_d = 4.8       # Stud diameter
stud_h = 1.8       # Stud height
wall = 1.2          # Wall thickness
brick_h = 9.6       # Standard brick height

# Body
body = (
    cq.Workplane("XY")
    .box(cols * unit, rows * unit, brick_h)
)

# Hollow underside
body = (
    body.faces("<Z").workplane()
    .rect(cols * unit - 2 * wall, rows * unit - 2 * wall)
    .cutBlind(-(brick_h - wall))
)

# Studs on top
body = (
    body.faces(">Z").workplane()
    .rarray(unit, unit, cols, rows)
    .circle(stud_d / 2)
    .extrude(stud_h)
)

print(f"Lego brick: {rows}x{cols} = {rows * cols} studs")
export_all(body, "01_lego_brick", (220, 40, 40))