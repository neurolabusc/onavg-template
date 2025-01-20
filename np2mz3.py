import numpy as np
import struct
import os
import sys

# fnm=on1031_trimmed.npy; git annex get $fnm && git annex unlock $fnm
def write_mz3(verts, idxs, scalars, output_file):
    """
    Writes vertices and indices to an mz3 file.

    Parameters:
        verts (np.ndarray): Nx3 array of vertex coordinates.
        idxs (np.ndarray): Mx3 array of vertex indices.
        output_file (str): Path to the output mz3 file.
    """
    # Constants for mz3 format
    MAGIC = 0x5A4D  # Magic number for mz3 files ('MZ')
    FLAG_VERTICES = 1    # Flag to indicate vertices are present
    FLAG_TRIANGLES = 2   # Flag to indicate triangles (indices) are present
    FLAG_SCALARS = 8  # Flag to indicate scalar values are present
    ATTR = 0
    num_faces = 0
    num_verts = 0
    if verts is not None and idxs is not None:
        ATTR += FLAG_VERTICES + FLAG_TRIANGLES  # Combined flags
        num_faces = idxs.shape[0]
        num_verts = verts.shape[0]
        print(f"mesh has {num_faces} triangles with {num_verts} vertices")
    if scalars is not None:
        ATTR += FLAG_SCALARS
        if num_verts == 0:
            num_verts = scalars.shape[0]
        print(f"atlas with {num_verts} vertices range: min={np.min(scalars)}, max={np.max(scalars)}")
    if ATTR == 0:
        print(f"insufficient inputs for write_mz3") 
        return
    n_skip = 0  # No skipped bytes in this case
    # Construct the header
    header = struct.pack(
        "<HHIII",          # Little-endian: uint16, uint16, uint32, uint32, uint32
        MAGIC,             # Magic number
        ATTR,              # Attribute flags
        num_faces,         # Number of faces
        num_verts,         # Number of vertices
        n_skip             # Number of skipped bytes
    )



    # Write the mz3 file
    with open(output_file, "wb") as f:
        f.write(header)    # Write the header
        if idxs is not None:
            idx_data = idxs.astype(np.uint32).tobytes()
            f.write(idx_data)  # Write the face indices
        if verts is not None:
            vert_data = verts.astype(np.float32).tobytes()
            f.write(vert_data) # Write the vertex coordinates
        if scalars is not None:
            scalar_data = scalars.astype(np.float32).tobytes()
            f.write(scalar_data)  # Write the scalar values

# Load vertices and indices from .npy files
order = "32"
root = "onavg-ico" + order + "_"
hemisphere = "rh"
geo = "geometry_"
layers = ["pial_", "midthickness_", "sphere.reg_", "smoothwm_", "white_"]
atlases = ["aparc.DKTatlas", "aparc.a2009s", "aparc"]
hemispheres = ["rh", "lh"]
for hemisphere in hemispheres:
    for layer in layers:
        ext = ""
        if "sphere" not in layer:
            ext = "_on1031_trimmed"
        fnmIdxs = root + geo + "faces_" + hemisphere + ".npy"
        fnmVerts = root + geo + layer + hemisphere + ext + ".npy"
        if os.path.exists(fnmIdxs) and os.path.exists(fnmVerts):
            idxs = np.load(fnmIdxs)  # Indices (Mx3)
            verts = np.load(fnmVerts)  # Vertices (Nx3)
            output_file = f"{layer}{hemisphere}{order}.mz3"
            write_mz3(verts, idxs, None, output_file)
        else:
            print(f"  did not find '{fnmIdxs}'/{fnmVerts}")
    for atlas in atlases:
        fnmAtlas = root + "parcellations_"+atlas+"_"+hemisphere+"_on1031_trimmed_overlap-8div_parc.npy"
        if os.path.exists(fnmAtlas):
            scalars = np.load(fnmAtlas)  # Scalars (e.g., labels)
            print(f"Atlas loaded from {fnmAtlas}")
            output_file = f"{hemisphere}{order}{atlas}.mz3"
            write_mz3(None, None, scalars, output_file)


# Write to mz3 format


print(f"Written mz3 file to {output_file}")
