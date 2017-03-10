#!/usr/bin/env python
'''

Used to make json for file transport to Janelia October 2016
'''
import os
import sys
import json
from time import strftime
import requests

LIMSaddress = 'http://lims2/wij_rois/get_specimen_rois/517649378.json'

LIMSjson = requests.get(LIMSaddress).json()
LIMSrois = LIMSjson['wij_rois']


def inrange(i, minmaxtup):
    try:
        int(i)
    except:
        return False
    return (int(i) >= minmaxtup[0] and int(i) <= minmaxtup[1])


def readlc(td):
    with open(os.path.join(td, 'lensCorrection.txt'), 'r') as f:
        t = f.read()
    return t


if __name__ == "__main__":
    firstz = int(sys.argv[1])
    lastz = int(sys.argv[2])
    outfn = sys.argv[3]

    print outfn

    zdict = {r['z_index']:
        {'raw_data': r['tile_directory'],
         'lens_correction_string': readlc(r['lens_correction']['tile_directory'])}
        for r in LIMSrois if inrange(r['z_index'], (firstz, lastz))
        and not r['superseded_by_roi']}

    jsonfn = os.path.join(
        os.path.dirname(outfn), '{}_z{}-z{}.json'.format(
            strftime('%Y%m%d'), firstz, lastz))

    with open(jsonfn, 'w') as f:
        json.dump(zdict, f)

#    with open(outfn, 'w') as f:
#        for ln in set([z['raw_data'] for z in zdict.values()]):
#            f.write('{}\n'.format(ln))
