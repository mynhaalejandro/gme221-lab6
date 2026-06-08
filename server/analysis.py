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

# ── Part D: GeoAI Model Construction ──────────────────────────────────────────
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# D.1 Encode target variable
parcels_landuse["target_code"] = (
    parcels_landuse["ASS_CLASSI"]
    .astype("category")
    .cat.codes
)

# D.2 Define feature matrix
features = [
    "area",
    "perimeter",
    "compactness",
    "dist_to_road",
    "dist_to_water",
    "dist_to_school",
    "dist_to_tourism",
    "landuse_code"
]

# D.3 Prepare dataset
data = parcels_landuse.dropna(subset=features + ["target_code"])

X = data[features]
y = data["target_code"]

# D.4 Split training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, random_state=42
)

# D.5 Train GeoAI model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# D.6 Generate predictions
y_pred = model.predict(X_test)

# D.7 Evaluate model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# ── Part E: Apply Predictions to Spatial Data ─────────────────────────────────

# E.1 Predict all parcels
data["predicted_class"] = model.predict(X)

# E.2 Convert codes back to labels
categories = (
    data["ASS_CLASSI"]
    .astype("category")
    .cat.categories
)

data["predicted_label"] = data["predicted_class"].apply(
    lambda code: categories[code]
)

# E.3 Compare actual vs predicted
data["correct_prediction"] = (
    data["ASS_CLASSI"] == data["predicted_label"]
)

print(
    data[["ASS_CLASSI", "predicted_label", "correct_prediction"]].head()
)

# ── Part F: Export GeoAI Results ──────────────────────────────────────────────

# F.1 Remove temporary columns
data = data.drop(columns=["centroid"], errors="ignore")

# F.2 Export to GeoJSON
data.to_file(
    "output/parcel_geoai_prediction.geojson",
    driver="GeoJSON"
)

print("GeoAI output exported.")

# ── Part G: Challenge – Improved Model ────────────────────────────────────────
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

# G.1 Additional spatial features
# Count of schools within 500m
data = data.copy()
data["schools_within_500m"] = data["centroid"].apply(
    lambda p: (schools.distance(p) <= 500).sum()
) if "centroid" in data.columns else data["geometry"].centroid.apply(
    lambda p: (schools.distance(p) <= 500).sum()
)

# Tourism density within 1km
data["tourism_within_1km"] = data["geometry"].centroid.apply(
    lambda p: (tourism.distance(p) <= 1000).sum()
)

# G.2 Extended feature set
features_g = features + ["schools_within_500m", "tourism_within_1km"]
data_g = data.dropna(subset=features_g + ["target_code"])

X_g = data_g[features_g]
y_g = data_g["target_code"]

X_train_g, X_test_g, y_train_g, y_test_g = train_test_split(
    X_g, y_g, test_size=0.30, random_state=42
)

# G.3 Compare classifiers
classifiers = {
    "Random Forest":  RandomForestClassifier(n_estimators=100, random_state=42),
    "Decision Tree":  DecisionTreeClassifier(random_state=42),
    "KNN":            KNeighborsClassifier(n_neighbors=5)
}

print("\nModel Comparison (with additional features):")
for name, clf in classifiers.items():
    clf.fit(X_train_g, y_train_g)
    acc = accuracy_score(y_test_g, clf.predict(X_test_g))
    print(f"  {name}: {acc:.4f}")
