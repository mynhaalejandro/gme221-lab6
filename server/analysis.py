import geopandas as gpd

# B.1 Load parcel layer
parcels = gpd.read_file("data/parcel.geojson")
print(parcels.head())
print(parcels.crs)

# B.2 Load supporting layers
roads   = gpd.read_file("data/roads.geojson")
water   = gpd.read_file("data/water_network.geojson")
landuse = gpd.read_file("data/landuse.geojson")
schools = gpd.read_file("data/schools.geojson")
tourism = gpd.read_file("data/tourism.geojson")

# B.3 Align CRS to parcel
roads   = roads.to_crs(parcels.crs)
water   = water.to_crs(parcels.crs)
landuse = landuse.to_crs(parcels.crs)
schools = schools.to_crs(parcels.crs)
tourism = tourism.to_crs(parcels.crs)

for name, gdf in [("parcels", parcels), ("roads", roads), ("water", water),
                  ("landuse", landuse), ("schools", schools), ("tourism", tourism)]:
    print(f"{name}: {gdf.shape}, CRS={gdf.crs}")
