import geopandas
import scipy.interpolate as scint
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

# Definiion of threshold to clip the raster
threshold = 20
crs = 'EPSG:25832'

# Read Thalweg shapefile
thal_df = geopandas.read_file('C:/Users/beatr/flussdetrender/clip_samples/thalweg_rough_trial.shp')

# Assigns direct x and y attributed from the derived attributes of the polygon
thal_df["x"] = thal_df["geometry"].x
thal_df["y"] = thal_df["geometry"].y

# Creates first Pi point
p_1 = np.array([thal_df.loc[0, 'x'], thal_df.loc[0, 'y']])

# Dtaaframe through whcih iterate to find the vectors and cumulative angle check
len = len(thal_df)
iter_thal = thal_df.loc[1:len-2, :]

# Vector to save the breakpoints of the flvuial system
break_points = np.array([])

teta = 0

# Loops through thalweg points
for i, row in enumerate(iter_thal.itertuples()):
    # Find the next two points necessary to calculate the vectors from p_1
    p_2 = np.array([thal_df.loc[i, 'x'], thal_df.loc[i, 'y']])
    p_3 = np.array([thal_df.loc[i+1, 'x'], thal_df.loc[i+1, 'y']])

    # v_i is the vector defined with a tuple (x,y,z)
    v_1 = p_2 - p_1
    v_2 = p_3 - p_1

    # Claculate the angle between the two vectors
    teta = teta + np.degrees(np.arcsin(abs(np.cross(v_1, v_2)) / abs(np.linalg.norm(v_1) * np.linalg.norm(v_2))))
    print(abs(np.cross(v_1, v_2)))
    print(abs(np.linalg.norm(v_1) * np.linalg.norm(v_2)))
    print(teta)
    if teta > threshold:
        p_1 = p_2
        np.append(break_points, p_1)
        # break_points.iloc[i+1, :] = pd.Series({'x': thal_df.loc[i, 'x'], 'y': thal_df.loc[i, 'y']})

print(break_points)


#columns = ['x', 'y']


# gdf = geopandas.GeoDataFrame(self.df, geometry=geopandas.points_from_xy(self.df.x, self.df.y))
#         gdf.crs = self.crs


# pd.DataFrame()
# break_points = break_points.rename(columns = {break_points.columns[0]: 'x', break_points.columns[1]: 'y'})
# break_points.iloc[0, :] = pd.Series({'x': thal_df.loc[0, 'x'], 'y': thal_df.loc[0, 'y']})