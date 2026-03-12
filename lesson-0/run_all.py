"""Run all 8 examples and generate STEP/STL/GLB output."""

import subprocess, sys, os, time

SCRIPTS = [
    "01_lego_brick.py",
    "02_honeycomb_coaster.py",
    "03_math_vase.py",
    "04_twisted_tower.py",
    "05_perforated_plate.py",
    "06_cable_organizer.py",
    "07_spring.py",
    "08_planetary_gears.py",
]

script_dir = os.path.dirname(os.path.abspath(__file__))

for script in SCRIPTS:
    print(f"\n--- {script} ---")
    result = subprocess.run(
        [sys.executable, os.path.join(script_dir, script)],
        cwd=script_dir, capture_output=True, text=True,
    )
    print(result.stdout, end="")
    if result.returncode != 0:
        print(f"  FAILED: {result.stderr.strip().splitlines()[-1]}")

print("\nDone! Check the output/ directory for STEP, STL, and GLB files.")