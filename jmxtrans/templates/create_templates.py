#!/usr/bin/env python

import json
import sys
from collections import OrderedDict

def main(fileNames):
    for filename in fileNames:
        with open(filename) as in_file:
            orig = json.load(in_file, object_pairs_hook=OrderedDict)

        server = orig["servers"][0]
        queries = server["queries"]
        del server["queries"]

        # server is now our serverInfo
        result = OrderedDict()
        result["serverInfo"] = server

        for query in queries:
            settings = query['outputWriters'][0]['settings']
            del query["outputWriters"]
            if 'typeNames' in settings:
                query['typeNames'] = settings['typeNames']

        # keep the other properties in "server"
        result["queryInfos"] = queries

        with open(filename + '.tmpl', 'w') as out:
            json.dump(result, out, separators=(',', ': '), indent=2)

if __name__ == "__main__":
    main(sys.argv[1:])
