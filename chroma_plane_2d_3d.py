# ===== Add this to bidr_demo.py (or run standalone) =====
import numpy as np
import matplotlib.pyplot as plt

def to_log_rgb(I, eps: float = 1e-8):
    return np.log(np.clip(I, eps, None))

def orthonormal_basis_from_vector(v):
    v = v / (np.linalg.norm(v) + 1e-12)
    # pick a helper not parallel to v
    a = np.array([1.0, 0.0, 0.0]) if abs(v[0]) < 0.9 else np.array([0.0, 1.0, 0.0])
    u1 = a - np.dot(a, v) * v
    u1 /= (np.linalg.norm(u1) + 1e-12)
    u2 = np.cross(v, u1); u2 /= (np.linalg.norm(u2) + 1e-12)
    return u1, u2

def project_onto_plane(points, origin, u1, u2):
    # Orthogonal projection: p_proj = origin + ((p-origin)·u1)u1 + ((p-origin)·u2)u2
    dp = points - origin
    a = dp @ u1
    b = dp @ u2
    return origin + np.outer(a, u1) + np.outer(b, u2), a, b  # also return 2D coords (a,b)

def demo_plane_visualization(seed: int = 7):
    rng = np.random.default_rng(seed)

    # Simulate one material across shadow→lit under a fixed (A,D)
    A = np.array([0.25, 0.35, 0.95])   # ambient (bluish)
    D = np.array([1.00, 0.95, 0.80])   # direct  (yellowish)
    R  = np.array([0.55, 0.55, 0.55])  # gray asphalt-like

    n = 2000
    g = rng.uniform(0, 1, n)                                # gamma
    Rj = R + rng.normal(0, 0.02, (n, 3))                    # slight texture
    I  = Rj * (A + g[:, None] * D) + rng.normal(0, 0.002, (n, 3))
    L  = to_log_rgb(I)                                      # log-RGB cloud

    # ISD (Illuminant Spectral Direction) and orthonormal basis of its orthogonal plane
    isd = to_log_rgb(A + D) - to_log_rgb(A)
    isd /= (np.linalg.norm(isd) + 1e-12)

    u1, u2 = orthonormal_basis_from_vector(isd)

    # Choose plane origin near the cloud center
    origin = L.mean(axis=0)

    # Orthogonally project points onto the ISD-orthogonal plane
    L_proj, a2d, b2d = project_onto_plane(L, origin, u1, u2)

    # ----- Build a visible plane patch (mesh) -----
    # Span the plane based on the spread of projected points
    amin, amax = np.percentile(a2d, [2, 98])
    bmin, bmax = np.percentile(b2d, [2, 98])
    # Pad a little for nicer framing
    pad_a = 0.15 * (amax - amin + 1e-12)
    pad_b = 0.15 * (bmax - bmin + 1e-12)
    agrid = np.linspace(amin - pad_a, amax + pad_a, 20)
    bgrid = np.linspace(bmin - pad_b, bmax + pad_b, 20)
    AA, BB = np.meshgrid(agrid, bgrid)
    plane_pts = origin + np.outer(AA.ravel(), u1) + np.outer(BB.ravel(), u2)
    XX = plane_pts[:, 0].reshape(AA.shape)
    YY = plane_pts[:, 1].reshape(AA.shape)
    ZZ = plane_pts[:, 2].reshape(AA.shape)

    # ----- Plot: plane + ISD vector + raw points + projected points -----
    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Plane (semi-transparent)
    ax.plot_surface(XX, YY, ZZ, alpha=0.25, linewidth=0, antialiased=True)

    # ISD arrow at plane origin (scaled for visibility)
    isd_len = 1.0
    p1 = origin
    p2 = origin + isd * isd_len
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], linewidth=3, label='ISD vector')

    # Raw log-RGB point cloud
    ax.scatter(L[:, 0], L[:, 1], L[:, 2], s=6, alpha=0.35, label='Log-RGB points')

    # Projected points (dark) sitting on the plane
    ax.scatter(L_proj[:, 0], L_proj[:, 1], L_proj[:, 2], s=5, alpha=0.8, label='Projected onto plane')

    ax.set_xlabel('log R'); ax.set_ylabel('log G'); ax.set_zlabel('log B')
    ax.set_title('ISD-orthogonal plane (illumination-invariant chromaticity)')
    ax.legend()
    fig.tight_layout()
    fig.savefig('chromaticity_plane_3d.png', dpi=300, bbox_inches='tight')
    plt.close(fig)

    # Optional: also save the 2-D chromaticity scatter (u1 vs u2)
    fig2 = plt.figure(figsize=(7, 6))
    plt.scatter(a2d, b2d, s=8, alpha=0.6)
    plt.xlabel('u1 (ISD-orthogonal axis 1)')
    plt.ylabel('u2 (ISD-orthogonal axis 2)')
    plt.title('Illumination-invariant chromaticity (2-D plane coordinates)')
    fig2.tight_layout()
    fig2.savefig('chromaticity_plane_2d.png', dpi=300, bbox_inches='tight')
    plt.close(fig2)

if __name__ == "__main__":
    demo_plane_visualization()
    print("Saved figures:")
    print(" - chromaticity_plane_3d.png")
    print(" - chromaticity_plane_2d.png")
