# GmE 221 – Laboratory 6: GeoAI Spatial Prediction Using Parcel-Based Feature Engineering

## Overview
This laboratory applies machine learning to spatial parcel data. Spatial features are engineered
from geometry and proximity using GeoPandas, then used to train a classification model with
Scikit-learn. Predictions are exported as GeoJSON and visualized in QGIS.

## Expected Outputs
- `output/parcel_predictions.geojson` — parcels with predicted land use classification
- `output/feature_importance.png` — bar chart of model feature importances
- `output/confusion_matrix.png` — model evaluation confusion matrix

## Commit Milestones
1. **Milestone 1 – Project Initialization**: folder structure, venv, requirements.txt, README
2. **Milestone 2 – Data Loading & Inspection**: load all GeoJSON layers, print shapes and CRS
3. **Milestone 3 – Feature Engineering**: compute area, perimeter, and proximity features per parcel
4. **Milestone 4 – Model Training**: build ML dataset, train Random Forest classifier, evaluate
5. **Milestone 5 – Prediction & Export**: predict all parcels, export to GeoJSON
6. **Milestone 6 – Visualization**: generate feature importance and confusion matrix plots
