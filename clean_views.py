import mobie
from copy import deepcopy as dc


ds=mobie.metadata.read_dataset_metadata('./data/tomo')

keep = ['MMRR_07','CD138-BMNC_01']

ds1 = dc(ds)

for view in ds['views'].keys():
    if '_'.join(view.split('_')[:2]) not in keep:
        ds1['views'].pop(view)
