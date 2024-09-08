# -*- coding: utf-8 -*- *enhanced by chatgpt*
"""
Created on Sun Aug 18 16:23:35 2024

@author: ss1647
"""

# output director ndvi files
peak_ndvi_dir = r'C:\Local Data\ss1647\Dissertation - Copy - Copy\Peak_NDVI'
os.makedirs(peak_ndvi_dir, exist_ok=True)

# make list of all ndvi files for 2023+2024
ndvi_dir = r'C:\Local Data\ss1647\Dissertation - Copy - Copy\NDVI_Calculations_Vegetation_Land_Cover'
ndvi_2023_files = sorted(glob.glob(os.path.join(ndvi_dir, '*2023*.tif')))
ndvi_2024_files = sorted(glob.glob(os.path.join(ndvi_dir, '*2024*.tif')))

def calculate_peak_ndvi(ndvi_files):
    peak_ndvi = None
    meta = None
    
    for ndvi_file in ndvi_files:
        with rasterio.open(ndvi_file) as src:
            ndvi = src.read(1).astype(float)
            meta = src.meta
            
            if peak_ndvi is None:
                peak_ndvi = ndvi
            else:
                peak_ndvi = np.maximum(peak_ndvi, ndvi)
    
    return peak_ndvi, meta

# find peak ndvi for 2023
peak_ndvi_2023, meta_2023 = calculate_peak_ndvi(ndvi_2023_files)
output_peak_2023 = os.path.join(peak_ndvi_dir, 'Peak_NDVI_2023.tif')
with rasterio.open(output_peak_2023, 'w', **meta_2023) as dst:
    dst.write(peak_ndvi_2023, 1)
print(f"Peak NDVI for 2023 saved to {output_peak_2023}")

# find peak ndvi for 2024
peak_ndvi_2024, meta_2024 = calculate_peak_ndvi(ndvi_2024_files)
output_peak_2024 = os.path.join(peak_ndvi_dir, 'Peak_NDVI_2024.tif')
with rasterio.open(output_peak_2024, 'w', **meta_2024) as dst:
    dst.write(peak_ndvi_2024, 1)
print(f"Peak NDVI for 2024 saved to {output_peak_2024}")
