#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 08:27:24 2021

@author: schorb
"""

import mrcfile as mrc
import random
import time
import sys
import os
import mobie
import glob
from multiprocessing import Pool


target='slurm'



outformat='ome.zarr'
chunks = list((64,128,128))
downscale_factors = list(([2,2,2],[2,2,2],[1,2,2],[1,2,2],[2,2,2],[2,2,2]))

indir = '/g/schwab/Tobias/EMPIAR/volumes/'
suffix = sys.argv[1]

# indir = os.path.join(indir,suffix)

# fileslist = os.path.join('/g/schwab/Tobias/MoBIE/',suffix+'_joinfiles.txt')
joinlist = glob.glob(os.path.join('/g/schwab/Tobias/EMPIAR/volumes',suffix.split('_')[0],suffix+'*'))

outdir = os.path.join('/g/schwab/Tobias/MoBIE2')


idx = 0

def mobieconvert(infile):
    # skip empty lines
    if len(infile)<3: return

    sleeptime = int(random.random()*90)

    base = os.path.basename(infile).split('_join')[0]

    # if os.path.exists(os.path.join(outdir,re.sub('/','_',base)+'.ome.zarr')):
    #     print('Skipping '+base+'. It already exists.')
    #     continue
    #
    # if os.path.exists(outfile):
    #     print('re-doing '+base+'.')
    #     shutil.rmtree(outfile)
    #     #continue
    # idx += 1
    #
    # if idx%blocksize == 0:
    #     time.sleep(break_interval)
    # else:
    #     time.sleep(submit_interval)

    print('converting ' + base + ' into MoBIE format after waiting for '+str(sleeptime)+'seconds.')

    time.sleep(sleeptime)

    # get pixel size

    mfile = mrc.mmap(infile, permissive='True')
    tomopx = mfile.voxel_size.x / 10000  # in um
    del (mfile)
    resolution = [tomopx] * 3

    try:
        mobie.add_image(infile,
                    "data",
                    outdir,
                    "tomo",
                    base,
                    resolution,
                    downscale_factors,
                    chunks,
                    file_format="ome.zarr",
                    target=target,
                    max_jobs=16,
                    menu_name='tomograms',
                    tmp_folder='/scratch/schorb/mobie/'+base
                    )
    except:
        print('re-doing '+base)
        with open('./missingjoins.txt','a+') as f:
            f.write(base+'  -   '+time.ctime())
        os.system('rm -rf /scratch/schorb/mobie/'+base)
        mobieconvert(infile)


with Pool(8) as p:
    p.map(mobieconvert, joinlist)


