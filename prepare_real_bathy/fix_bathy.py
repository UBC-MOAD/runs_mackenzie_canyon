import netCDF4 as nc
import numpy as np
import sys

def fix_bathy(infile,outfile):
    """
    Simple script to make depths shallower than 1.5m into land points
    """
    with nc.Dataset(infile) as f:
        bm = f.variables['Bathymetry'][:]

    minval = 1.5
    idx = (bm < minval)
    if np.any(idx):
        bm[idx] = 0
    
    # Now create output NetCDF file
    with nc.Dataset(outfile, 'w') as fout:
        fout.createDimension('x', bm.shape[1])
        fout.createDimension('y', bm.shape[0])
        fout.createVariable('Bathymetry', 'f8', ('y','x'), zlib=True, complevel=4)
        fout.variables['Bathymetry'][:] = bm

if __name__ == "__main__":
    fix_bathy(sys.argv[1],sys.argv[2])

