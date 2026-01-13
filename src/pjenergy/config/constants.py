
class DefaultParameters():

    DEFAULT_DATASET = 'reanalysis-era5-pressure-levels'
    DEFAULT_PRODUCT_TYPE = ['reanalysis']
    DEFAULT_VARIABLES = ("u_component_of_wind", 
                         "v_component_of_wind", 
                         "relative_humidity", 
                         "temperature", 
                         "geopotential")
    DEFAULT_YEARS = tuple(range(2015, 2026))
    DEFAULT_MONTHS = tuple(range(1, 13))
    DEFAULT_DAYS = tuple(range(1, 32))
    DEFAULT_TIMES = tuple(f"{h:02d}:00" for h in range(24)) 

    DEFAULT_MAXIMUM_LATITUDE = -21.0 # North
    DEFAULT_MINIMUM_LATITUDE = -24.0 # South
    DEFAULT_MAXIMUM_LONGITUDE = -39.0 # East
    DEFAULT_MINIMUM_LONGITUDE = -42.0 # West
    DEFAULT_AREA = (DEFAULT_MAXIMUM_LATITUDE, 
                    DEFAULT_MINIMUM_LONGITUDE, 
                    DEFAULT_MINIMUM_LATITUDE,
                    DEFAULT_MAXIMUM_LONGITUDE)

    DEFAULT_PRESSURE_LEVELS = (900, 925, 950, 975, 1000)
    DEFAULT_DATA_FORMAT = 'netcdf'
    DEFAULT_DOWNLOAD_FORMAT = 'unarchived'

    
