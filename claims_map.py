# Full code for plotting a UK map showing motor insurance risk by region

import geopandas as gpd
import folium
import pandas as pd
import numpy as np
import os

# Define the Git repo path and the shapefile URL (adjust these as needed)
repo_path = 'your_repo_path'  # Replace with the path to your repo or folder
shapefile_path = os.path.join(repo_path, 'UK_regions.shp')

# Check if the shapefile exists; if not, raise an error (you need to download it beforehand)
if not os.path.exists(shapefile_path):
    raise FileNotFoundError(f"Shapefile not found at {shapefile_path}. Please ensure it's in the correct location.")

# Load the UK shapefile (you need to download the shapefile and place it in your repo folder)
gdf = gpd.read_file(shapefile_path)

# Create some dummy claims data for each region (adjust as necessary for real data)
regions = gdf['region_name']  # Adjust this to match the column name in your shapefile
np.random.seed(42)
claims_data = pd.DataFrame({
    'region': regions,
    'claim_count': np.random.randint(50, 1000, size=len(regions)),
    'risk_score': np.random.uniform(0, 1, size=len(regions))
})

# Merge claims data with GeoDataFrame
gdf = gdf.merge(claims_data, left_on='region_name', right_on='region')

# Create a folium map centered around the UK
uk_map = folium.Map(location=[54.0, -2.0], zoom_start=6)

# Define a color scale based on the risk score
colormap = folium.LinearColormap(['green', 'yellow', 'red'], vmin=0, vmax=1)

# Add regions to the map with colors representing risk score
for _, region in gdf.iterrows():
    folium.GeoJson(
        region['geometry'],
        style_function=lambda feature, risk_score=region['risk_score']: {
            'fillColor': colormap(risk_score),
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.7,
        },
        tooltip=folium.GeoJsonTooltip(fields=['region', 'claim_count', 'risk_score'],
                                      aliases=['Region:', 'Claims:', 'Risk:'],
                                      localize=True)
    ).add_to(uk_map)

# Add a color legend
colormap.add_to(uk_map)

# Save the map to the repo
output_path = os.path.join(repo_path, 'uk_motor_insurance_claims_risk_map.html')
uk_map.save(output_path)

print(f'Map has been saved at {output_path}')
