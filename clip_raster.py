import geopandas
import scipy.interpolate as scint
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

# Definiion of threshold to clip the raster
threshold = 30
crs = 'EPSG:25832'

# Read Thalweg shapefile
thal_df = geopandas.read_file('C:/Users/beatr/DEMTools/thalweg_rough_trial.shp')

# Assigns direct x and y attributed from the derived attributes of the polygon
thal_df["x"] = thal_df["geometry"].x
thal_df["y"] = thal_df["geometry"].y

# Creates first Pi point
p_1 = np.array([thal_df.loc[0, 'x'], thal_df.loc[0, 'y']])

# Dtaaframe through whcih iterate to find the vectors and cumulative angle check
len = len(thal_df)
iter_thal = thal_df.loc[1:len-2, :]

# Vector to save the breakpoints of the flvuial system
break_points = np.array([0, 0])

acc_teta = 0.0

# Loops through thalweg points
for i, row in enumerate(iter_thal.itertuples()):
    # Find the next two points necessary to calculate the vectors from p_1
    p_2 = np.array([thal_df.loc[i+1, 'x'], thal_df.loc[i+1, 'y']])
    p_3 = np.array([thal_df.loc[i+2, 'x'], thal_df.loc[i+2, 'y']])

    # v_i is the vector defined with a tuple (x,y,z)
    v_1 = p_2 - p_1
    v_2 = p_3 - p_1

    # Claculate the angle between the two vectors
    # print(abs(np.cross(v_1, v_2)))
    # print(abs(np.linalg.norm(v_1)))
    # print(abs(np.linalg.norm(v_2)))
    teta_new = np.degrees(np.arcsin(abs(np.cross(v_1, v_2)) / abs(np.linalg.norm(v_1) * np.linalg.norm(v_2))))
    acc_teta += teta_new

    if acc_teta > threshold:
        p_1 = p_2
        break_points = np.vstack((break_points, p_1))
        acc_teta = 0



#TODO - export breakpoints as shape

columns = ['x', 'y']
indices = np.arange(0, np.shape(break_points)[0]-1, 1)
break_df = pd.DataFrame(columns=columns, data=break_points[1::], index=indices)
gdf = geopandas.GeoDataFrame(break_df, geometry=geopandas.points_from_xy(break_df.x, break_df.y))
gdf.crs = crs
gdf.to_file(drive='ESRI Shapefile', filename='test_breakpoints_t30_abs.shp')