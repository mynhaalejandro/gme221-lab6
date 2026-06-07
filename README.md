# GmE 221 – Laboratory 6: GeoAI Spatial Prediction Using Parcel-Based Feature Engineering

## Overview
This laboratory applies machine learning to spatial parcel data. Spatial features are engineered
from geometry and proximity using GeoPandas, then used to train a classification model with
Scikit-learn. Predictions are exported as GeoJSON and visualized in QGIS.

## How to Run
```bash
# 1. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run analysis
python server/analysis.py
```

## Expected Outputs
- `output/parcel_predictions.geojson` — parcels with predicted land use classification
- `output/feature_importance.png` — bar chart of model feature importances
- `output/confusion_matrix.png` — model evaluation confusion matrix

## Project Structure
```
gme221-lab6
├── .venv/
├── data/
│   ├── landuse.geojson
│   ├── parcel.geojson
│   ├── roads.geojson
│   ├── schools.geojson
│   ├── tourism.geojson
│   └── water_network.geojson
├── output/
├── server/
│   └── analysis.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Commit Milestones and Reflections

### Milestone 1: Project Setup
Project structure created with required directories, dependencies configured, and baseline README established.

### Milestone 2: Data Loading & Inspection
All six map layers (parcels, roads, water, landuse, schools, tourism) were loaded and checked. All layers are using the same coordinate system (EPSG:3123) so they line up correctly on the map. The parcel layer was confirmed to have the classification fields needed for training. Each layer plays a different role — parcels are what we want to predict, roads show how accessible a place is, water shows what's nearby environmentally, schools show access to services, tourism shows economic activity nearby, and land use shows what surrounds each parcel. No machine learning happens yet — this step is just about getting all the data ready.

1. **Why are parcels the prediction unit?**  
   Parcels are individual plots of land with clear boundaries and existing classification labels. Since we want to predict what type of land each plot is, it makes sense to use each parcel as one item the model learns from and predicts on.

2. **What spatial processes might roads influence?**  
   Roads affect how easy it is to get to a place. Land near busy roads is more likely to be used for shops or businesses, while land far from roads tends to stay residential or agricultural. Roads also affect property values and development potential.

3. **Why might tourism affect parcel classification?**  
   Areas near tourist spots tend to develop into commercial or hospitality uses because of the economic activity tourists bring. A parcel close to a tourism feature is more likely to shift toward business or mixed use over time.

4. **Is machine learning occurring at this stage?**  
   No. This step is just loading and organizing the data. No predictions are being made and no model is being trained yet — we are simply making sure all the layers are loaded correctly and ready to use.

### Milestone 3 – Feature Engineering
Geometry features (area, perimeter, compactness) and proximity features (distance to roads, water, schools, tourism) were computed for each parcel. Land use context was added through a spatial join and encoded as numbers. This step converts raw GIS data into a table of numbers that a machine learning model can actually read and learn from.

5. **Why can geometry not be used directly in ML?**  
   Machine learning models only work with numbers. A polygon shape has no numeric meaning on its own — it needs to be broken down into measurable values like area, perimeter, or compactness before a model can use it.

6. **Why are distances meaningful features?**  
   Distance tells the model how close or far a parcel is from things that affect land use — like roads, schools, or water. A parcel right next to a road behaves very differently from one deep in a rural area, and those differences help the model make better predictions.

7. **Which feature do you think is most influential?**  
   Distance to roads is likely the most influential because road access directly drives how land gets developed and used. Parcels near roads tend to shift toward commercial or residential use, while remote parcels tend to stay agricultural.

### Milestone 4 – Model Training
Build ML dataset, train Random Forest classifier, evaluate.

### Milestone 5 – Prediction & Export
Predict all parcels, export to GeoJSON.

### Milestone 6 – Visualization
Generate feature importance and confusion matrix plots.
