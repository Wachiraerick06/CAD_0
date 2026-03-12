"""
Shared export functions for CadQuery examples.
Exports shapes to STEP, STL, and colored GLB.
"""

import os
import numpy as np
import cadquery as cq
import trimesh

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def _cq_to_trimesh(shape, tolerance=0.1):
    """Convert a CadQuery shape to a trimesh object via temporary STL."""
    tmp_path = os.path.join(OUTPUT_DIR, "_temp.stl")
    cq.exporters.export(shape, tmp_path, tolerance=tolerance)
    mesh = trimesh.load(tmp_path)
    os.remove(tmp_path)
    return mesh

def export_all(shape, name, color, tolerance=0.1):
    """
    Export a single-color, single-part shape to STEP, STL, and GLB.
    color: RGB tuple, 0-255, e.g. (220, 40, 40)
    """
    step_path = os.path.join(OUTPUT_DIR, f"{name}.step")
    stl_path = os.path.join(OUTPUT_DIR, f"{name}.stl")
    glb_path = os.path.join(OUTPUT_DIR, f"{name}.glb")

    cq.exporters.export(shape, step_path)
    cq.exporters.export(shape, stl_path, tolerance=tolerance)

    mesh = trimesh.load(stl_path)
    r, g, b = color
    mesh.visual = trimesh.visual.ColorVisuals(
        mesh=mesh,
        face_colors=np.full((len(mesh.faces), 4), [r, g, b, 255], dtype=np.uint8),
    )
    mesh.export(glb_path)
    _print_summary(name, step_path, stl_path, glb_path)

def export_gradient(shape, name, color_bottom, color_top, tolerance=0.1):
    """
    Export a shape with Z-gradient vertex colors to STEP, STL, and GLB.
    Colors interpolate from color_bottom (min Z) to color_top (max Z).
    """
    step_path = os.path.join(OUTPUT_DIR, f"{name}.step")
    stl_path = os.path.join(OUTPUT_DIR, f"{name}.stl")
    glb_path = os.path.join(OUTPUT_DIR, f"{name}.glb")

    cq.exporters.export(shape, step_path)
    cq.exporters.export(shape, stl_path, tolerance=tolerance)

    mesh = trimesh.load(stl_path)
    vertices = mesh.vertices
    z_min, z_max = vertices[:, 2].min(), vertices[:, 2].max()
    z_range = z_max - z_min if z_max > z_min else 1.0

    t = ((vertices[:, 2] - z_min) / z_range).reshape(-1, 1)
    c_bot = np.array(color_bottom, dtype=np.float64)
    c_top = np.array(color_top, dtype=np.float64)
    rgb = (1 - t) * c_bot + t * c_top
    alpha = np.full((len(vertices), 1), 255, dtype=np.float64)
    vertex_colors = np.hstack([rgb, alpha]).astype(np.uint8)

    mesh.visual = trimesh.visual.ColorVisuals(mesh=mesh, vertex_colors=vertex_colors)
    mesh.export(glb_path)
    _print_summary(name, step_path, stl_path, glb_path)

def export_multipart(parts, name, tolerance=0.1):
    """
    Export a multi-part, multi-color assembly to STEP, STL, and GLB.
    parts: list of (cq_shape, part_name, (r, g, b)) tuples
    """
    step_path = os.path.join(OUTPUT_DIR, f"{name}.step")
    stl_path = os.path.join(OUTPUT_DIR, f"{name}.stl")
    glb_path = os.path.join(OUTPUT_DIR, f"{name}.glb")

    assy = cq.Assembly()
    for shape, part_name, color in parts:
        r, g, b = color
        assy.add(shape, name=part_name,
                 color=cq.Color(r / 255, g / 255, b / 255, 1))
    assy.save(step_path, "STEP")

    scene = trimesh.Scene()
    all_meshes = []
    for shape, part_name, color in parts:
        mesh = _cq_to_trimesh(shape, tolerance)
        r, g, b = color
        mesh.visual = trimesh.visual.ColorVisuals(
            mesh=mesh,
            face_colors=np.full((len(mesh.faces), 4), [r, g, b, 255], dtype=np.uint8),
        )
        scene.add_geometry(mesh, node_name=part_name)
        all_meshes.append(mesh)

    combined = trimesh.util.concatenate(all_meshes)
    combined.export(stl_path)
    scene.export(glb_path)
    _print_summary(name, step_path, stl_path, glb_path)

def _print_summary(name, step_path, stl_path, glb_path):
    def _size(p):
        s = os.path.getsize(p)
        return f"{s / 1_000_000:.1f} MB" if s > 1_000_000 else f"{s / 1_000:.0f} KB"
    print(f"  {name}:")
    print(f"    STEP  {_size(step_path):>8}   {step_path}")
    print(f"    STL   {_size(stl_path):>8}   {stl_path}")
    print(f"    GLB   {_size(glb_path):>8}   {glb_path}")
    print("CadQuery and Export Helper loaded successfully!")