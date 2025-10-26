import numpy as np
import matplotlib.pyplot as plt

# Example: lit and shadow RGB samples (linearized)
lit  = np.array([[0.9, 0.7, 0.6],
                 [0.85, 0.65, 0.55],
                 [0.8, 0.6, 0.5]])  # sample points under direct light
shadow = lit * np.array([0.5, 0.6, 0.9])  # example ambient scaling

'''
Mechanics:

lit is a 3×3 NumPy array; each row is an RGB triplet (R,G,B) from the 
same material measured at slightly different places under direct light.

shadow multiplies each lit pixel channel-wise by [0.5, 0.6, 0.9]. 
NumPy broadcasts the 1×3 vector across rows and multiplies component-wise.

Concept:

In the BIDR model: I = R_B ⋅ (A + γD), where:
- 𝐼 is the observed color (RGB triplet)
- 𝑅_𝐵 is the body reflectance
- 𝐴 is the ambient illumination
- 𝛾 is a scalar for direct illumination
- 𝐷 is the direct illumination component

When a surface moves from lit to shadow, the direct term drops, 
leaving mostly the ambient. In RGB, that often appears as a color-biased scaling (e.g., skylight is bluer: a larger factor in B).

Here [0.5,0.6,0.9] is a toy per-channel ratio between shadowed and lit 
appearance (not strictly physics-derived, but illustrative). 
It makes blue drop the least (0.9), mimicking bluish ambient light.
'''


# Compute BIDR cylinder in log space
lit_log = np.log(lit)
shadow_log = np.log(shadow)
'''
Mechanics: Elementwise natural log of each RGB value (must be > 0).

Concept: In log-RGB, illumination and reflectance become additive rather than multiplicative. 
Under BIDR, each material’s lit→shadow trajectory becomes (almost) a straight line; 
different materials under the same A,D share the same direction (the ISD).
'''

# Axis direction (Estimate the Illuminant Spectral Direction)
isd = np.mean(lit_log - shadow_log, axis=0)
isd /= np.linalg.norm(isd)
'''
Mechanics:

lit_log - shadow_log is the vector from shadow to lit for each sample (row-wise).
np.mean(..., axis=0) averages those three vectors column-wise to reduce noise → a single 3-D direction.
np.linalg.norm(isd) computes its Euclidean length; dividing normalizes to unit length.

Concept:

The vector from log(shadow) to log(lit) approximates log(A+γD) change; 
its direction is the ISD for that illuminant pair.

Normalizing gives a pure direction (scale-free). This is the axis along which illumination varies; 
orthogonal directions capture reflectance chromaticity.

'''

# Generate cylinder points
t = np.linspace(0, 1, 50)
cylinder = shadow_log.mean(0) + t[:, None] * (lit_log.mean(0) - shadow_log.mean(0))
'''
Mechanics:

t = np.linspace(0,1,50) creates 50 scalars from 0→1.
shadow_log.mean(0) and lit_log.mean(0) are the mean shadow and mean lit points (3-D).
(lit_log.mean(0) - shadow_log.mean(0)) is the mean direction from shadow to lit.
t[:, None] reshapes t into 50×1 so NumPy can broadcast it when multiplying a 1×3 vector; the result is 50×3 points.

Concept:

This parameterizes the line segment from the average shadow point (t=0) to the average lit point (t=1) in log-RGB. 
In the ideal, all pixels of that material lie on this line; 
in real data they form a thin tube around it (the “cylinder”).
'''

# Plot in log RGB space
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot(cylinder[:,0], cylinder[:,1], cylinder[:,2], '-r', linewidth=2, label='BIDR Cylinder')
ax.scatter(lit_log[:,0], lit_log[:,1], lit_log[:,2], c='orange', s=50, label='Lit Samples')
ax.scatter(shadow_log[:,0], shadow_log[:,1], shadow_log[:,2], c='blue', s=50, label='Shadow Samples')

'''
Mechanics:

Creates a 3-D axes; plots the line (cylinder) in red.
Overlays the individual lit and shadow log-RGB samples as orange and blue points.
Shows a legend; renders the window.

Concept:

You see the lit and shadow clusters and the line joining their means—the BIDR line (center of the cylinder).
With many pixels from one material (not just three), you’d see a slender cloud aligned with that line (the cylinder). 
The major axis of that cloud ≈ ISD.
'''

# Add labels and title
ax.set_xlabel('Log R')
ax.set_ylabel('Log G')
ax.set_zlabel('Log B')
ax.set_title('Bi-illumination Dichromatic Reflection (BIDR) Model\nCylinder in Log RGB Space')
ax.legend()

# Save the figure with a descriptive filename
plt.tight_layout()
plt.savefig('BIDR_cylinder_simulation_log_RGB.png', dpi=300, bbox_inches='tight')
print("Image saved as: BIDR_cylinder_simulation_log_RGB.png")

plt.show()
