"""
Example 7: Helical Spring
Wire diameter, coil diameter, pitch all parametric.
"""

import cadquery as cq
from export_helper import export_all

# Parameters
wire_d = 3.0         # Wire diameter
coil_d = 25.0        # Mean coil diameter
pitch = 8.0          # Pitch (distance per turn)
n_turns = 5          # Number of active turns

coil_r = coil_d / 2
height = pitch * n_turns

# Generate a true helix wire
helix_wire = cq.Wire.makeHelix(pitch, height, coil_r)

# Create circular cross-section at helix start
cross_section = (
    cq.Workplane("YZ")
    .transformed(offset=(coil_r, 0, 0))
    .circle(wire_d / 2)
)

# Sweep cross-section along helix
spring = cross_section.sweep(cq.Workplane().add(helix_wire))

print(f"Helical spring: {n_turns} turns, {wire_d}mm wire, {coil_d}mm coil")
export_all(spring, "07_spring", (140, 150, 170), tolerance=0.5)