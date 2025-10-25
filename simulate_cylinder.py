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
'''







# Compute BIDR cylinder in log space
lit_log = np.log(lit)
shadow_log = np.log(shadow)

# Axis direction (Illuminant Spectral Direction)
isd = np.mean(lit_log - shadow_log, axis=0)
isd /= np.linalg.norm(isd)

# Generate cylinder points
t = np.linspace(0, 1, 50)
cylinder = shadow_log.mean(0) + t[:, None] * (lit_log.mean(0) - shadow_log.mean(0))

# Plot in log RGB space
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot(cylinder[:,0], cylinder[:,1], cylinder[:,2], '-r', linewidth=2, label='BIDR Cylinder')
ax.scatter(lit_log[:,0], lit_log[:,1], lit_log[:,2], c='orange', s=50, label='Lit Samples')
ax.scatter(shadow_log[:,0], shadow_log[:,1], shadow_log[:,2], c='blue', s=50, label='Shadow Samples')

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
