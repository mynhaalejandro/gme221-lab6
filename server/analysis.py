import geopandas as gpd

# ── Part B: Data Loading ───────────────────────────────────────────────────────

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

# ── Part C: Feature Engineering ───────────────────────────────────────────────

# C.1 Geometry-based features
parcels["area"]        = parcels.geometry.area
parcels["perimeter"]   = parcels.geometry.length
parcels["compactness"] = parcels["area"] / (parcels["perimeter"] ** 2)

# C.2 Parcel centroids
parcels["centroid"] = parcels.geometry.centroid

# C.3 Distance to roads
parcels["dist_to_road"] = parcels["centroid"].apply(
    lambda p: roads.distance(p).min()
)

# C.4 Distance to water
parcels["dist_to_water"] = parcels["centroid"].apply(
    lambda p: water.distance(p).min()
)

# C.5 Distance to schools
parcels["dist_to_school"] = parcels["centroid"].apply(
    lambda p: schools.distance(p).min()
)

# C.6 Distance to tourism
parcels["dist_to_tourism"] = parcels["centroid"].apply(
    lambda p: tourism.distance(p).min()
)

# C.7 Land use context — spatial join and encode
parcels_landuse = gpd.sjoin(
    parcels,
    landuse[["Name", "geometry"]],
    how="left",
    predicate="intersects"
)

parcels_landuse["landuse_code"] = (
    parcels_landuse["Name"]
    .astype("category")
    .cat.codes
)

# C.8 Print land use category codes
print(
    parcels_landuse[["Name", "landuse_code"]]
    .drop_duplicates()
    .sort_values("landuse_code")
)
