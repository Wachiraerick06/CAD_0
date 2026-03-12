"""
Example 8: Planetary Gear Set
Sun, planets, ring from shared module value.
"""

import cadquery as cq
import math
from export_helper import export_multipart

# Parameters
module = 2.0         # Gear module (mm)
sun_z = 16           # Sun gear tooth count
planet_z = 8         # Planet gear tooth count
n_planets = 3        # Number of planet gears
gear_h = 10.0        # Gear face width
pressure_angle = 20  # degrees

# Derived
ring_z = sun_z + 2 * planet_z  # Ring gear tooth count
sun_r = module * sun_z / 2
planet_r = module * planet_z / 2
ring_r = module * ring_z / 2
orbit_r = sun_r + planet_r      # Planet orbit radius

def make_gear_profile(z, m, pa=20):
    """Create a simplified gear profile using polygon approximation."""
    r_pitch = m * z / 2
    r_outer = r_pitch + m
    r_root = r_pitch - 1.25 * m

    points = []
    for i in range(z):
        angle = 2 * math.pi * i / z

        # Tooth tip
        for j in [-1, 0, 1]:
            a = angle + j * math.pi / (z * 3)
            r = r_outer if j == 0 else r_pitch
            points.append((r * math.cos(a), r * math.sin(a)))

        # Tooth root
        a_root = angle + math.pi / z
        for j in [-1, 0, 1]:
            a = a_root + j * math.pi / (z * 4)
            points.append((r_root * math.cos(a), r_root * math.sin(a)))

    return points

def make_gear(z, m, height, bore_d=0):
    """Create a gear solid from tooth count and module."""
    pts = make_gear_profile(z, m)
    gear = (
        cq.Workplane("XY")
        .polyline(pts).close()
        .extrude(height)
    )
    if bore_d > 0:
        gear = gear.faces(">Z").workplane().hole(bore_d)
    return gear

def make_ring_gear(z_ring, z_planet, m, height):
    """Create an internal ring gear (outer disc with internal teeth)."""
    r_outer = m * z_ring / 2 + 3 * m
    pts = make_gear_profile(z_ring, m)
    inner_profile = (
        cq.Workplane("XY")
        .polyline(pts).close()
        .extrude(height)
    )
    outer_disc = cq.Workplane("XY").cylinder(height, r_outer)
    ring = outer_disc.cut(inner_profile)
    return ring

# Build the assembly
sun = make_gear(sun_z, module, gear_h, bore_d=6)

planets = []
for i in range(n_planets):
    angle = 2 * math.pi * i / n_planets
    px = orbit_r * math.cos(angle)
    py = orbit_r * math.sin(angle)
    planet = make_gear(planet_z, module, gear_h, bore_d=4)
    planet = planet.translate((px, py, 0))
    planets.append(planet)

ring = make_ring_gear(ring_z, planet_z, module, gear_h)

# Carrier plate
carrier = (
    cq.Workplane("XY")
    .workplane(offset=-3)
    .cylinder(3, orbit_r + planet_r - 2)
)
carrier = carrier.faces(">Z").workplane().hole(6)

parts = [
    (sun, "sun_gear", (218, 165, 32)),       # Gold
    (ring, "ring_gear", (0, 140, 140)),       # Teal
    (carrier, "carrier", (160, 160, 165)),    # Gray
]
for i, p in enumerate(planets):
    parts.append((p, f"planet_{i}", (200, 50, 50)))  # Red

print(f"Planetary gear set: sun={sun_z}T, planet={planet_z}T, ring={ring_z}T")
export_multipart(parts, "08_planetary_gears")