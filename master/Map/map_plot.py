import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import contextily as ctx

def plot_map_from_csv(file_path):
    # Read data from the CSV file
    data = pd.read_csv(file_path)
    
    # Check if the necessary columns exist
    if 'LONGITUDE' not in data.columns or 'LATITUDE' not in data.columns:
        print("CSV file must contain 'LONGITUDE' and 'LATITUDE' columns.")
        return
    
    # Drop rows with missing values in 'LONGITUDE' or 'LATITUDE' columns
    data = data.dropna(subset=['LONGITUDE', 'LATITUDE'])
    
    # Create a GeoDataFrame using latitude and longitude
    geometry = [Point(xy) for xy in zip(data['LONGITUDE'], data['LATITUDE'])]
    gdf = gpd.GeoDataFrame(data, geometry=geometry)
    gdf = gdf.set_crs(epsg=4326)  # Set coordinate reference system to WGS84
    
    # Convert to Web Mercator for basemap compatibility
    gdf = gdf.to_crs(epsg=3857)

    # Plot map with points
    fig, ax = plt.subplots(figsize=(10, 10))
    gdf.plot(ax=ax, color='red', markersize=50, label="Locations")
    
    # Add basemap using OpenStreetMap with specified zoom level
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, zoom=12)

    # Add labels and title
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("Locations Map with Place Names")
    plt.legend()
    plt.show()

# Example usage:
file_path = r"C:\Users\srijanani.LTPL\Downloads\Merged_ 20.10.24_3.0 kWh vehicle.csv"  # Replace with your file path
plot_map_from_csv(file_path)
