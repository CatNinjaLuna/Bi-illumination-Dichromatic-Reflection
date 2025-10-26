"""
Log-RGB Contrast Demonstration
------------------------------
Input image: outdoor_shadow.png

This image contains both brightly lit areas and strong shadows — perfect for visualizing
how log-RGB enhances dark-region contrast and compresses bright intensities.

The code:
1. Loads the image as linear RGB (normalized to [0,1]).
2. Applies a logarithmic transformation to simulate log-RGB.
3. Displays side-by-side comparisons of Linear vs Log-RGB.
4. Plots intensity profiles along a horizontal line to show tone compression behavior.
5. Saves all generated figures with descriptive filenames.

Author: Carolina Li
Date: 2025-10-26
"""

import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import os

# ---------- Helper functions ----------
def normalize01(arr):
    arr = arr.astype(np.float32)
    m, M = np.min(arr), np.max(arr)
    return (arr - m) / (M - m + 1e-8)

def to_log_rgb(img, eps=1e-6):
    log_img = np.log(img + eps)
    return normalize01(log_img)

# ---------- Load and prepare image ----------
path = "outdoor_shadow.png"  # image file should be in the same directory as this script
save_dir = "/Users/carolina1650/Bi-illumination-Dichromatic-Reflection/linear_log_outputs"
os.makedirs(save_dir, exist_ok=True)

img = imageio.imread(path).astype(np.float32) / 255.0
linear_rgb = normalize01(img)
log_rgb = to_log_rgb(linear_rgb)

# ---------- Figure 1: Display comparison ----------
plt.figure(figsize=(12,5))
plt.subplot(1,2,1)
plt.imshow(np.clip(linear_rgb, 0, 1))
plt.title("Linear RGB (Radiance Proportional)")
plt.axis('off')

plt.subplot(1,2,2)
plt.imshow(np.clip(log_rgb, 0, 1))
plt.title("Log-RGB (Enhanced Shadows, Compressed Highlights)")
plt.axis('off')
plt.tight_layout()
f1_path = os.path.join(save_dir, "figure1_linear_vs_log.png")
plt.savefig(f1_path, dpi=300)
plt.close()

# ---------- Figure 2: Intensity profile comparison ----------
gray_linear = np.dot(linear_rgb[..., :3], [0.2989, 0.5870, 0.1140])
gray_log = np.dot(log_rgb[..., :3], [0.2989, 0.5870, 0.1140])

row = gray_linear.shape[0] // 2
x = np.arange(gray_linear.shape[1])

plt.figure(figsize=(10,4))
plt.plot(x, gray_linear[row, :], label='Linear RGB Intensity', color='orange')
plt.plot(x, gray_log[row, :], label='Log-RGB Intensity', color='blue')
plt.title("Intensity Profile Across Midline")
plt.xlabel("Pixel Index (horizontal)")
plt.ylabel("Normalized Intensity")
plt.legend()
plt.tight_layout()
f2_path = os.path.join(save_dir, "figure2_intensity_profile.png")
plt.savefig(f2_path, dpi=300)
plt.close()

# ---------- Figure 3: Mapping function comparison ----------
xs = np.linspace(0, 1, 1000)
ys_linear = xs
ys_log = (np.log(xs + 1e-6) - np.log(1e-6)) / (np.log(1 + 1e-6) - np.log(1e-6))

plt.figure(figsize=(6,4))
plt.plot(xs, ys_linear, label="Linear")
plt.plot(xs, ys_log, label="Log (normalized)")
plt.title("Linear vs Log Mapping Curve")
plt.xlabel("Input Intensity")
plt.ylabel("Output (Display Intensity)")
plt.legend()
plt.tight_layout()
f3_path = os.path.join(save_dir, "figure3_linear_vs_log_curve.png")
plt.savefig(f3_path, dpi=300)
plt.close()

# ---------- Figure 4: Histogram comparison ----------
plt.figure(figsize=(7,4))
plt.hist(gray_linear.ravel(), bins=100, alpha=0.6, label='Linear RGB', color='orange')
plt.hist(gray_log.ravel(), bins=100, alpha=0.6, label='Log-RGB', color='blue')
plt.title("Histogram Comparison: Linear vs Log-RGB")
plt.xlabel("Normalized Intensity")
plt.ylabel("Pixel Count")
plt.legend()
plt.tight_layout()
f4_path = os.path.join(save_dir, "figure4_histogram_comparison.png")
plt.savefig(f4_path, dpi=300)
plt.close()

# ---------- Save images ----------
linear_path = os.path.join(save_dir, "linear_rgb_image.png")
log_path = os.path.join(save_dir, "log_rgb_image.png")
imageio.imwrite(linear_path, (linear_rgb * 255).astype(np.uint8))
imageio.imwrite(log_path, (log_rgb * 255).astype(np.uint8))

# ---------- Summary ----------
print("All figures and processed images saved to:")
print(f"📁 {save_dir}\n")
print(f"1️⃣ {f1_path}")
print(f"2️⃣ {f2_path}")
print(f"3️⃣ {f3_path}")
print(f"4️⃣ {f4_path}")
print(f"5️⃣ Linear RGB image: {linear_path}")
print(f"6️⃣ Log RGB image: {log_path}")
