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
The feature matrix (area, perimeter, compactness, distances, land use code) and target variable (ASS_CLASSI) were prepared. Rows with missing values were removed, the data was split 70/30 into training and testing sets, and a Random Forest classifier was trained on 100 decision trees. The model achieved an accuracy of 96.18% on the test set.

8. **What does accuracy mean spatially?**  
   Accuracy means the model correctly predicted the land use class for about 96 out of every 100 parcels it had never seen before. Spatially, this means the model is correctly identifying what type of land a parcel is based on its shape, size, and surroundings.

9. **Can a model have high accuracy but poor spatial interpretation?**  
   Yes. If most parcels in the dataset belong to one class (like residential), the model can score high accuracy just by predicting that class most of the time, even if it completely misses other land use types. High accuracy does not always mean the model understands the full spatial picture.

10. **What features may improve the model?**  
    Adding features like distance to commercial centers, elevation, population density, or parcel shape regularity could improve predictions. Features that capture more of the social and economic context around a parcel would help the model distinguish between similar-looking land types.

### Milestone 5 – Prediction & Export

**Spatial Misclassification Reflection**

The output shows each parcel with its actual class (ASS_CLASSI), what the model predicted (predicted_label), and whether it was correct (correct_prediction). Most parcels were correctly identified — rows 0, 1, 2, and 4 were all predicted as class A and matched the actual label. Row 3 was a misclassification where the model predicted R (Residential) but the actual class was A (Agricultural). That parcel likely sits near a residential zone and its feature values — size, shape, distance to roads, surrounding land use — looked similar enough to residential that the model got confused. With 96.18% accuracy, only about 4 out of every 100 parcels are misclassified. Errors are most likely parcels sitting on the edge between two land use zones where the features of both classes overlap.

### Milestone 6 – Challenge: Model Improvement
Two additional spatial features were added — count of schools within 500m and count of tourism sites within 1km. Three classifiers were trained and compared using the extended feature set.

| Model | Accuracy |
|---|---|
| Random Forest | 96.32% |
| Decision Tree | 94.89% |
| KNN | 94.75% |

Adding the two new features improved Random Forest from 96.18% to 96.32%. Random Forest remained the best performing model. Decision Tree and KNN both scored around 94.7–94.9%, trailing by about 1.5%. Random Forest handles the spatial complexity of this dataset better because it builds many decision trees and averages their results, making it more resilient to noisy or overlapping feature values near land use boundaries.

## Final Reflection

11. **How is GeoAI different from traditional GIS analysis?**  
    Traditional GIS follows rules that a person writes manually — like drawing a buffer or running an overlay. GeoAI learns the rules from the data itself. Instead of telling the system what matters, you give it examples and it figures out the patterns on its own.

12. **What spatial features most influenced the model?**  
    Based on the model's feature importances, parcel area (19.8%) and perimeter (18.1%) were the top two features, followed by distance to roads (14.5%) and distance to tourism (12.2%). Geometry features ranked highest because parcel size and shape vary significantly across land use classes — large irregular parcels tend to be agricultural while smaller compact ones are more often residential or commercial. Distance to roads and tourism carried the next most weight, confirming that proximity to infrastructure and economic activity also drives classification. Land use context code ranked lowest (4.0%), likely because it partially overlaps with the information already captured by the geometry and distance features.

13. **What are the limitations of this model?**  
    The model only knows what it was trained on. If the data has errors or is outdated, the predictions will reflect those problems. It also struggles with parcels on the boundary between two zones where features overlap. It cannot account for local knowledge, zoning rules, or future development plans.

14. **How can this support spatial decision-making?**  
    Planners can use the predictions to quickly flag parcels that may be misclassified or have changed use over time. It speeds up large-scale land use reviews and helps identify areas where field verification is needed. It can also help prioritize where development or conservation efforts should be focused.

15. **What ethical or planning concerns may arise from predictive parcel classification?**  
    If the model is used to make decisions about land value, taxation, or development approvals, errors could unfairly affect landowners. Predictions based on proximity to roads or tourism could reinforce existing inequalities by favoring already developed areas. Any model used in planning should be validated by humans before decisions are made.
