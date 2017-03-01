#!/usr/bin/env python

import glob
import json
import os
import re
import sys


# 0: transformId, 1: dataString
lensSpecTemplate = """{{
    "type" : "list",
    "id" : "{0}",
    "specList" : [ {{
        "type" : "leaf",
        "className" : "mpicbg.trakem2.transform.NonLinearCoordinateTransform",
        "dataString" : "{1}"
    }} ]
}}"""

# 0: tileId, 1: section, 2: camera, 3: imageRow, 4: imageCol,
# 5: stageX, 6: stageY, 7: imagePath, 8: lensTransformId
tileSpecTemplate = """{{
    "tileId" : "{0}.{1}.0",
    "layout" : {{
        "sectionId" : "{1}.0",
        "temca" : "0",
        "camera" : "{2}",
        "imageRow" : {3},
        "imageCol" : {4},
        "stageX" : {5},
        "stageY" : {6}
    }},
    "z" : {1}.0,
    "width" : 3840.0,
    "height" : 3840.0,
    "minIntensity" : 0.0,
    "maxIntensity" : 65535.0,
    "mipmapLevels" : {{
        "0" : {{
            "imageUrl" : "file:{7}"
        }}
    }},
    "transforms" : {{
        "type" : "list",
        "specList" : [ {{
            "type" : "ref",
            "refId" : "{8}"
        }}, {{
            "type" : "leaf",
            "className" : "mpicbg.trakem2.transform.AffineModel2D",
            "dataString" : "1 0 0 1 {5} {6}"
        }} ]
    }}
}}"""

sectionJsonfile = sys.argv[1]
inputDirPath = ''# sys.argv[2]
specDirectory = sys.argv[2]

sectionDataPath = os.path.abspath(sectionJsonfile)

with open(sectionDataPath) as sectionDataFile:
    sectionData = json.load(sectionDataFile)

lensSpecs = {}

for section in sectionData:
    rawData = '/EMdata/phase1Data' + sectionData[section]["raw_data"]
    lensCorrectionString = sectionData[section]["lens_correction_string"]
    (dataDirName, camera) = os.path.split(os.path.split(os.path.join(rawData, ''))[0])

    lensTransformId = "lens_%s" % camera

    lensSpecs[lensTransformId] = lensSpecTemplate.format(lensTransformId, lensCorrectionString)

    rawFileDir = rawData # os.path.join(inputDirPath, camera)
    if not os.path.exists(rawFileDir):
        continue
    rawFileNameList = glob.glob(rawFileDir + "/_track*.txt")

    rawFileName = rawFileNameList[0]

    tileSpecList = []

    with open(rawFileName, 'r') as rawFile:
        for line in rawFile:
	    line = line.replace(' ','')
            words = line.split()
            imageFileName = words[0]
            #imageFileName = imageFileName.replace(' ', '')
            imagePath = os.path.join(rawFileDir, imageFileName)
            tileId = os.path.splitext(imageFileName)[0]
            stageX = words[1]
            stageY = words[2]
            imageFileNamePieces = imageFileName.split('_')
	    #print imageFileNamePieces
            column = imageFileNamePieces[len(imageFileNamePieces) - 2]
            row = os.path.splitext(imageFileNamePieces[len(imageFileNamePieces) - 1])[0]

            tileSpecList.append(tileSpecTemplate.format(tileId, section, camera, row, column, stageX, stageY, imagePath, lensTransformId))

    if len(tileSpecList) > 0:
        tileSpecFileName = "%s/%s.json" % (specDirectory, section)
        tileSpecFile = open(tileSpecFileName, 'w')
        tileSpecFile.write('[\n')
        count = 0
        for tileSpec in tileSpecList:
            if count > 0:
                tileSpecFile.write(',\n')
            tileSpecFile.write(tileSpec)
            count = count + 1
        tileSpecFile.write('\n]')

if len(lensSpecs) > 0:
    lensSpecFileName = "%s/lens_specs.json" % specDirectory
    lensSpecFile = open(lensSpecFileName, 'w')
    lensSpecFile.write('[\n')
    count = 0
    for lensSpecId in lensSpecs:
        if count > 0:
            lensSpecFile.write(',\n')
        lensSpecFile.write(lensSpecs[lensSpecId])
        count = count + 1
    lensSpecFile.write('\n]')

print "wrote tile specs for %d sections to %s" % (len(sectionData), specDirectory)
print "wrote shared lens specs to %s" % lensSpecFileName
