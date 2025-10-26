# Bi-illumination Dichromatic Reflection (BIDR) Analysis

This repository explores concepts and implementations from the paper **"A bi-illuminant dichromatic reflection model for understanding images"** by Maxwell et al. (2008). It contains Python implementations for analyzing and visualizing the Bi-illumination Dichromatic Reflection (BIDR) model, a computer vision technique used for understanding how surfaces appear under different lighting conditions.

## Overview

The BIDR model describes how the appearance of surfaces changes when transitioning from direct illumination (lit areas) to ambient illumination (shadows). In the model, observed color **I** is expressed as:

```
I = R_B · (A + γD)
```

Where:

-  **I** is the observed color (RGB triplet)
-  **R_B** is the body reflectance
-  **A** is the ambient illumination
-  **γ** is a scalar for direct illumination intensity
-  **D** is the direct illumination component

## Key Features

### 1. Log-RGB Transformation

In log-RGB space, illumination and reflectance become additive rather than multiplicative, making the analysis more tractable. This transformation reveals the underlying structure of how materials behave under different lighting conditions.

### 2. Illuminant Spectral Direction (ISD)

The ISD represents the direction in log-RGB space along which illumination varies. Materials under the same illumination conditions share the same ISD, making it possible to separate illumination effects from material properties.

### 3. Illumination-Invariant Chromaticity

By projecting onto the plane orthogonal to the ISD, we can obtain illumination-invariant representations of material chromaticity.

## Files Description

### Core Analysis Scripts

-  **`simulate_cylinder.py`** - Basic BIDR cylinder demonstration in log-RGB space
-  **`pca_logchroma_multipleIlluminance.py`** - Comprehensive BIDR analysis including:
   -  PCA analysis of cylinder thickness
   -  Chromaticity plane projections
   -  Multiple illuminant scenarios
-  **`chroma_plane_2d_3d.py`** - 2D and 3D visualization of chromaticity planes
-  **`linear_log_comparison.py`** - Comparative analysis of linear vs log-RGB representations

### Output Directory

-  **`linear_log_outputs/`** - Contains generated figures and processed images from the linear vs log-RGB comparison

## Installation

### Requirements

```bash
pip install numpy matplotlib imageio scikit-learn
```

### Optional Dependencies

-  `scikit-learn` - For PCA analysis (falls back to SVD if unavailable)
-  `imageio` - For image processing in linear_log_comparison.py

## Usage

### Basic BIDR Cylinder Visualization

```bash
python simulate_cylinder.py
```

Generates: `BIDR_cylinder_simulation_log_RGB.png`

### Comprehensive BIDR Analysis

```bash
python pca_logchroma_multipleIlluminance.py
```

Generates:

-  `BIDR_cylinder_simulation_log_RGB.png`
-  `pca_cylinder_thickness.png`
-  `chromaticity_plane_projection.png`
-  `multiple_illuminants_tubes.png`

### Chromaticity Plane Visualization

```bash
python chroma_plane_2d_3d.py
```

Generates:

-  `chromaticity_plane_3d.png`
-  `chromaticity_plane_2d.png`

### Linear vs Log-RGB Comparison

```bash
python linear_log_comparison.py
```

Requires: `outdoor_shadow.png` in the same directory
Generates multiple comparison figures in `linear_log_outputs/` directory

## Generated Visualizations

### 1. BIDR Cylinder

Shows how lit and shadow samples of the same material form a cylindrical structure in log-RGB space, with the cylinder axis aligned with the ISD.

### 2. PCA Thickness Analysis

Demonstrates the thickness of the BIDR cylinder using dense sampling across shadow edges, revealing the principal components of variation.

### 3. Chromaticity Plane Projections

Visualizes illumination-invariant material properties by projecting onto planes orthogonal to the ISD.

### 4. Multiple Illuminant Analysis

Shows how different illumination conditions create separate BIDR tubes with different ISDs.

### 5. Linear vs Log-RGB Comparison

Demonstrates the advantages of log-RGB representation for shadow analysis:

-  Enhanced contrast in dark regions
-  Compressed highlights
-  More uniform distribution of intensity values

## Key Concepts

### Log-RGB Benefits

-  **Additive Model**: Illumination and reflectance become additive
-  **Linear Trajectories**: Material transitions form straight lines
-  **Enhanced Shadows**: Better contrast in dark regions
-  **Compressed Highlights**: Prevents saturation in bright areas

### Applications

-  **Shadow Detection**: Identifying shadowed regions in images
-  **Material Segmentation**: Separating different materials under varying illumination
-  **Illumination Estimation**: Recovering lighting conditions from images
-  **Color Constancy**: Achieving illumination-invariant color representation

## Technical Details

### Mathematical Foundation

The BIDR model assumes that surfaces exhibit dichromatic reflection, where the observed color is a combination of:

1. **Body Reflection**: Light that penetrates the surface and reflects the material's intrinsic color
2. **Interface Reflection**: Direct reflection from the surface interface

### ISD Computation

The Illuminant Spectral Direction is estimated as:

```python
isd = np.mean(lit_log - shadow_log, axis=0)
isd /= np.linalg.norm(isd)
```

### Chromaticity Projection

Illumination-invariant chromaticity is obtained by projecting onto the plane orthogonal to the ISD:

```python
u1, u2 = orthonormal_basis_from_vector(isd)
proj_x = logI @ u1
proj_y = logI @ u2
```

## Author

Carolina Li

## Date

October 26, 2025

## References

This implementation is based on the Bi-illuminant Dichromatic Reflection model:

**Maxwell, B. A., Friedhoff, R. M., & Smith, C. A.** (2008). A bi-illuminant dichromatic reflection model for understanding images. _2008 IEEE Conference on Computer Vision and Pattern Recognition_, Anchorage, AK, USA, 1-8. doi: [10.1109/CVPR.2008.4587491](https://doi.org/10.1109/CVPR.2008.4587491)

Additional references include research in computer vision and color constancy, particularly work on dichromatic reflection models and illumination-invariant image analysis.
