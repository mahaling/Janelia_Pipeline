import json
import sys
import os
import argparse
import jsonschema


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate tile pairs for given sections')
    parser.add_argument('--jsonfile', dest='jsonfile', help='input json file with input parameters', type=str, default=None)
    args = parser.parse_args()

    if args.jsonfile is None:
        print "Need an input json file with input parameters"
        sys.exit()

    with open(args.jsonfile) as inputJson:
        inputParams = json.load(inputJson)

    base_cmd = os.path.join(inputParams["renderBinPath"], "run_ws_client.sh") 
    base_cmd = base_cmd + " 6G org.janelia.render.client.TilePairClient"


    filter_opts = " --xyNeighborFactor " + str(inputParams["xyNeighborFactor"]) + " --excludeCornerNeighbors " + inputParams["excludeCornerNeighbors"] + " --excludeSameLayerNeighbors " + inputParams["excludeSameLayerNeighbors"] + " --excludeCompletelyObscuredTiles " + inputParams["excludeCompletelyObscuredTiles"]

    P1 = " --baseDataUrl " + inputParams["baseDataUrl"] + " --owner " + inputParams["owner"] + " --project " + inputParams["project"] 
    P2 = " --baseOwner " + inputParams["owner"] + " --baseProject " + inputParams["project"] + " --baseStack " + inputParams["stack"]
    P3 = " --stack " + inputParams["stack"] + " --minZ " + str(inputParams["minZ"]) + " --maxZ " + str(inputParams["maxZ"])

    withinJson= "tile_pairs_" + inputParams["stack"] + "_z_" + str(inputParams["minZ"]) + "_to_" + str(inputParams["maxZ"]) + "_dist_" + str(inputParams["distance"]) + ".json.gz"
    withinJson = os.path.join(inputParams["outputDir"], withinJson)

    cmd = base_cmd + P1 + P2 + P3 + filter_opts + " --zNeighborDistance " + str(inputParams["distance"]) + " --toJson " + withinJson
    os.system(cmd)


