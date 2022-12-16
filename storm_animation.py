import os
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import cartopy.crs as ccrs
import cartopy
import numpy as np
import datetime as dt

def crop_nc(netcdf, min_lon = 245.09, min_lat = 27.98, max_lon = 284.22, max_lat = 50.38):
    return netcdf.sel(lat=slice(min_lat, max_lat), lon=slice(min_lon, max_lon))

def make_storm_animation(varname, datetime, level=None, path=None, min_lon = 250.09, min_lat = 27.98, max_lon = 284.22, max_lat = 55):
    if path is None:
        path = f'D:/data/{datetime.year}'
        
    var_mean_full = xr.open_dataset(f'{path}/means/{varname}.{datetime.year}.nc')
    var_spread_full = xr.open_dataset(f'{path}/spreads/{varname}.{datetime.year}.nc')
    
    var_mean = crop_nc(var_mean_full, min_lon, min_lat, max_lon, max_lat)
    var_spread= crop_nc(var_spread_full, min_lon, min_lat, max_lon, max_lat)
    
    if varname in ['hgt', 'uwnd', 'vwnd']:
        var_mean = var_mean.sel(level=level)
        var_spread = var_spread.sel(level=level)
    
    lon = var_mean['lon']
    lat = var_mean['lat']
    
    fig = plt.figure(figsize=(10,10))
    ax3 = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax3.add_feature(cartopy.feature.COASTLINE)
    ax3.add_feature(cartopy.feature.BORDERS, linestyle=':')
    ax3.add_feature(cartopy.feature.LAKES, alpha=0.5)
    ax3.add_feature(cartopy.feature.RIVERS)
    ax3.set_extent([min_lon, max_lon, min_lat, max_lat], crs=ccrs.PlateCarree())
    
    def plot_storm(steps_plus):
    
        im3 = ax3.pcolor(lon, lat, var_mean[varname].sel(time=datetime + dt.timedelta(hours = 3 * steps_plus)), alpha=0.75)
        cbar = plt.colorbar(im3)
        return [im3, cbar]
    
    anim = FuncAnimation(fig, plot_storm)
    plt.show()
    
    ax3.set_title(f'{varname} on {datetime}')
    
make_storm_animation('apcp', dt.datetime(1844, 5, 12, 3), level=1000)