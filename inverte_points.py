
from config import *
from thalweg import *

address = "Thalweg_points/thal_points_k13.shp"
thal_points = Thalweg(address)
thal_df = thal_points.shape2dataframe
thal_df = thal_df[::-1]
thal_df["distance"] =thal_df["distance"].values[::-1]

# Burn shape file
thal_df.to_file("thal_points_kb13", driver='ESRI Shapefile')

print(thal_df["z"])