#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 08:27:24 2021

@author: schorb
"""

import numpy as np
import mrcfile as mrc
import re
import sys
import os
import mobie


cluster = True


submit_interval = 2 # time to wait between submitting jobs to not overload the group share IO
blocksize = 8
break_interval = 40


outformat='ome.zarr'
chunks = list((64,128,128))
downscale_factors = list(([2,2,2],[2,2,2],[1,2,2],[1,2,2],[2,4,4],[2,2,2]))

indir = '/g/schwab/Tobias/EMPIAR/volumes/'
suffix = sys.argv[1]

# indir = os.path.join(indir,suffix)

fileslist = os.path.join('/g/schwab/Tobias/MoBIE/',suffix+'_joinfiles.txt')

outdir = os.path.join('./test')#/g/schwab/Tobias/MoBIE2')


with open(fileslist,'r') as f:
    joinlist=f.read().splitlines()

idx = 0

for file in joinlist:

    file = os.path.abspath(os.path.join(indir,file))
    
    base = os.path.basename(file).split('_join')[0]

    # if os.path.exists(os.path.join(outdir,re.sub('/','_',base)+'.ome.zarr')):
    #     print('Skipping '+base+'. It already exists.')
    #     continue
    #
    # if os.path.exists(outfile):
    #     print('re-doing '+base+'.')
    #     shutil.rmtree(outfile)
    #     #continue
    idx += 1
    
    if idx%blocksize == 0:
        time.sleep(break_interval)
    else:
        time.sleep(submit_interval)

    print('converting '+base+' into MoBIE format.')
    
    # get pixel size

    mfile = mrc.mmap(file,permissive = 'True')
    tomopx = mfile.voxel_size.x / 10000 # in um
    del(mfile)
    resolution=[tomopx]*3

    mobie.add_image(file,'',outdir,'tomo',base,resolution,downscale_factors,chunks,file_format=outformat)

    # mat=np.eye(4)*tomopx
    # mat[2,2] = tomopx*zstretch
    # mat[3,3] = 1
    
    # tf_tr = tf.matrix_to_transformation(mat).tolist()

    # setup_id = 0

    # view=dict()
    #
    # view['resolution'] = [tomopx,tomopx,tomopx*zstretch]
    # view['setup_id'] = setup_id
    # view['setup_name'] = os.path.basename(base)
    #
    # view['OriginalFile'] = file
    #
    # view['trafo'] = dict()
    # view['trafo']['Scaling'] = tf_tr
    #
    # view['attributes'] = dict()

    # view['attributes']['displaysettings'] = dict({'id':setup_id,'color':bdv.colors['W'],'isset':'true'})
    # view['attributes']['displaysettings']['Projection_Mode'] = 'Average'

    # data = mfile.data


    # # check if volume is rotated
    # if data.shape[0]/data.shape[1]>5:
    #     data = np.swapaxes(data,0,1)

    # data0 = np.swapaxes(data,0,2)
    # data1 = np.fliplr(data0)
    # data2 = np.swapaxes(data1,0,2)

   # print(outfile)

# bdv.write_bdv(outfile, file, view, outf='.n5', blow_2d=zstretch, downscale_factors=downscale_factors, cluster=cluster,
#               infile=file, chunks=chunks)

del(view)
