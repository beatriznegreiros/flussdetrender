from detrender import *
"""
 Author: Beatriz Negreiros
 """


# TODO: class of a dem to operate the detrending
#
# def getAngle(pt1, pt2):
#     x_diff = pt2.x - pt1.x
#     y_diff = pt2.y - pt1.y
#     return math.degrees(math.atan2(y_diff, x_diff))

class DEM:
    def __init__(self, rivercourse_shape, crs = 'nan', raster_address=""):
        """A class used to represent a the raster DEM to be detrended.

        Attributes
        ----
        _slope: Float values os the slope of the regression line from
        the  thalwegs' points (Elevation, Distance Downstream)

        Methods:
        ----
        slope: (Setter) Sets the property slope to follow the detrend process
        __mul__: Magic method to transforms the attribute slope in percentage
        __gt__: Magic method to check if the slope of the detrended DEM is lower
        enough to be considered flat (detrended)
        find_thal_new_z: Finds the elevation values of the detrended DEM that
        corresponds to coordinates of the thalwegs' points
        compute_slope: Compute the slope of a regression line of a 2d scatter
        check_detrend: Checks if the DEM respects a limit to be considered detrended

        Parameters:
        ____
        :param shape_address: String of the local address of a shape file
        :param driver: Type of driver to open a shape file. DEFAULT:"ESRI Shapefile"
        """
        # super().__init__(shape_address, driver)
        # self._slope = np.nan
        self.rivercourse_shape = rivercourse_shape
        self.course_df = geopandas.read_file(self.rivercourse_shape)
        if self.course_df.crs:
            self.crs = self.course_df.crs
        else:
            if crs == 'nan':
                print(
                    'Error trying to fetch coordinate reference system. Please enter a shapefile with a crs or insert it as parameter')
            else:
                self.crs = crs

    def breakpoints(self, river_width, threshold = 30, out_shape = 'nan'):
        """ Generates the breakpoints to clip the raster and execute piecewise detrending
        :param threshold: float, minimum accumulated inflection angle between points of the thalweg to establish a breakpoint
        :return: shapefile (.shp) of breakpoints
        """

        # Assigns direct x and y attributed from the derived attributes of the polygon
        self.course_df["x"] = self.course_df["geometry"].x
        self.course_df["y"] = self.course_df["geometry"].y

        # First breakpoint point of the river
        p_break = np.array([self.course_df.loc[0, 'x'], self.course_df.loc[0, 'y']])

        # Dtaaframe through whcih iterate to find the vectors and cumulative angle check
        len_course = len(self.course_df)
        iter_rivercourse = self.course_df.loc[1:len_course - 2, :]  # exclude two last points as there will be no inflection

        # Vector to save the breakpoints of the river
        break_points = np.array([0, 0])

        acc_teta = 0.0
        # Loops through thalweg points
        for i, row in enumerate(iter_rivercourse.itertuples()):
            # Find the next two points necessary to calculate the vectors and later the angle between them
            p_2 = np.array([self.course_df.loc[i + 1, 'x'], self.course_df.loc[i + 1, 'y']])
            p_3 = np.array([self.course_df.loc[i + 2, 'x'], self.course_df.loc[i + 2, 'y']])

            # v_i is the vector defined with a tuple (x,y,z)
            v_1 = p_2 - p_break
            v_2 = p_3 - p_break

            # Claculate the angle between the two vectors
            teta_new = np.degrees(np.arcsin(abs(np.cross(v_1, v_2)) / abs(np.linalg.norm(v_1) * np.linalg.norm(v_2))))
            acc_teta += teta_new

            if acc_teta > threshold:
                p_break = p_2
                break_points = np.vstack((break_points, p_break))

                ab = shapely.geometry.LineString([tuple(p_break), tuple(p_3)])
                left = ab.parallel_offset(river_width / 2, 'left')
                right = ab.parallel_offset(river_width / 2, 'right')
                c = left.boundary[1]
                d = right.boundary[0]  # note the different orientation for right offset
                cd = shapely.geometry.Polygon([c, d])
                acc_teta = 0 #  sets it back for the next loop

        # Exports breakpoints as shape
        columns = ['x', 'y']
        indices = np.arange(0, np.shape(break_points)[0] - 1, 1)
        break_df = pd.DataFrame(columns=columns, data=break_points[1::], index=indices)
        gdf = geopandas.GeoDataFrame(break_df, geometry=geopandas.points_from_xy(break_df.x, break_df.y))
        gdf.crs = self.crs
        if out_shape is not 'nan':
            gdf.to_file(drive='ESRI Shapefile', filename=out_shape)
        return gdf


    def clippingshape(self, riverwidth, out_shape, breakpoints = 'nan'):
        if breakpoints is not 'nan':
            break_pts = geopandas.read_file(breakpoints)
        else:
            break_pts = self.breakpoints()
        for i, row in enumerate(self.course_df.itertuples()):



if __name__ == "__main__":
    # Create two lists with all addresses of: raster files (DEMs); shape files (thalweg points).
    #file_list_raster = find_files(directory=directory_raster_files)
    #file_list_shape = find_files(directory=directory_shape_files)

    # Definiion of threshold to clip the raster
    threshold = 20
    #crs = 'EPSG:25832'
    shape = 'C:/Users/Negreiros/riodetrend_supportingmaterial/smooth_pts_rivercourse.shp'
    riofun = DEM(shape)
    riofun.breakpoints(threshold, out_shape='test_breakpoints_t20_abs.shp')





