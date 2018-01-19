import netCDF4 as nc

dset_t = nc.Dataset('1_temperature_for_agrif_test.nc','r+')
dset_t['votemper'][0, -1, :, :] = dset_t['votemper'][0, -2, :, :]
dset_t.close()

dset_s = nc.Dataset('1_salinity_for_agrif_test.nc','r+')
dset_s['vosaline'][0, -1, :, :] = dset_s['vosaline'][0, -2, :, :]
dset_s.close()
