import numpy as np
import netCDF4 as nc
import ibcao
from IPython import embed
import sys

# Get helper functions
sys.path.append('/home/imachuca/MEOPAR/analysis-michael/bathymetry')
from bathy_helpers import expandf

# Coordsfile is used to determine IBCAO spatial truncation 
coordsfile = '/home/imachuca/Canyons/runs_mackenzie_canyon/coordinates/NEMO_files/coords_for_agrif.nc'

# Source IBCAO file and destination for truncated IBCAO data in NEMO format
src='/home/imachuca/Canyons/runs_mackenzie_canyon/prepare_real_bathy/IBCAO_V3_500m_RR.grd'
dst='/home/imachuca/Canyons/runs_mackenzie_canyon/prepare_real_bathy/IBCAO_V3_500m_RR_For_Nesting_Tool.nc'

# Get the IBCAO data, make depths positive, and make elevations zero
bathy = ibcao.IBCAO(ibcao_grd_file = src)
ix,iy = bathy.x, bathy.y
z = -bathy.z
z[z<0]=0

# Get a proj object for converting to/from the IBCAO projection
P = bathy.get_proj()

# Load the f-points from the NEMO grid and expand them by one
with nc.Dataset(coordsfile, 'r') as cnc:
    glamf = cnc.variables['glamf'][0,...]
    gphif = cnc.variables['gphif'][0,...]
    glamfe, gphife = expandf(glamf, gphif)

# Convert NEMO's f points to IBCAO's projection
nx,ny= P(glamfe, gphife)
    
# IBCAO has many points, truncate here based on the extrema of the NEMO grid (in IBCAO projection)
idx1 = (ix >= np.min(nx)) & (ix <= np.max(nx))
idx2 = (iy >= np.min(ny)) & (iy <= np.max(ny))
ix,iy = ix[idx1], iy[idx2]
z = z[idx2,:]
z = z[:,idx1]

# Convert the truncated IBCAO x,y grid from IBCAO projection to lon, lat
X,Y = np.meshgrid(ix, iy, sparse=False, indexing='xy')
lon, lat = P(X, Y, inverse=True)

# Now create NetCDF file for use in the nesting tools
with nc.Dataset(dst, 'w') as fout:
    fout.createDimension('x', ix.size)
    fout.createDimension('y', iy.size)
    # Write each variable
    def writevar(fout,name,val):
        fout.createVariable(name, 'f8', ('y','x'), zlib=True, complevel=4)
        fout.variables[name][:] = val
    writevar(fout,'nav_lon', lon);
    writevar(fout,'nav_lat', lat)
    writevar(fout,'Bathymetry', z)

