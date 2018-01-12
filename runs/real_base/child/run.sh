#/bin/bash

set -e

TOOLPATH=$HOME/Canyons/nestingtools/NEMOGCM/TOOLS/NESTING
MCPATH=$HOME/Canyons/runs_mackenzie_canyon

# Make symlinks to parent grid files
ln -fs ../mesh_mask.nc
ln -fs $MCPATH/coordinates/NEMO_files/coords_for_agrif.nc
ln -fs $MCPATH/prepare_real_bathy/real_bathy_for_agrif_fix.nc
#ln -fs $MCPATH/bathymetry/NEMO_files/idealized/ideal_bathy_for_agrif.nc

ln -fs $MCPATH/conditions/NEMO_files/salinity/salinity_for_agrif.nc
ln -fs $MCPATH/conditions/NEMO_files/temperature/temperature_for_agrif.nc

echo files read

makefiles ()
{
  # Namelist
  NMLIST=$1

  # Build the coordinates file
  $TOOLPATH/agrif_create_coordinates.exe $NMLIST
  echo coordinates file built
  
  # Write AGRIF_FixdGrids.in
  python make_agfi.py $NMLIST
  echo AGRIF_FixedGrids.in written

  $TOOLPATH/agrif_create_bathy.exe $NMLIST
  echo child bathy created

  # Create the data
  $TOOLPATH/agrif_create_data.exe $NMLIST
  echo forcing created
}


# Make the realistic files
makefiles mackenzie_real
echo made files

mv 1_*nc AGRIF_FixedGrids.in ../
echo moved files

rm real_bathy_for_agrif_fix.nc
rm coords_for_agrif.nc
rm salinity_for_agrif.nc
rm temperature_for_agrif.nc
rm mesh_mask.nc
echo removed symlinks
