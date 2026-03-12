"""
Example 3: Mathematical Vase
Sine-wave profile lofted and shelled into a vase.
"""

import cadquery as cq
import math
from export_helper import export_gradient

# Parameters
n_sections = 20
height = 120.0
base_r = 30.0
amplitude = 12.0
wall_thickness = 2.5

# Collect profile wires
wp = cq.Workplane("XY")
for i in range(n_sections + 1):
    z = height * i / n_sections
    t = i / n_sections
    # Sine-modulated radius: wide base, narrow waist, flared top
    r = base_r + amplitude * math.sin(t * math.pi * 2 - math.pi / 2)
    wire = cq.Workplane("XY").workplane(offset=z).ellipse(r, r * 0.85).val()
    wp = wp.add(wire)

# Loft through profiles, then hollow
vase = wp.toPending().loft()
vase = vase.faces(">Z").shell(-wall_thickness)

print("Mathematical vase: sine-wave profile, 20 cross-sections")
export_gradient(vase, "03_math_vase", (0, 128, 128), (218, 165, 32))