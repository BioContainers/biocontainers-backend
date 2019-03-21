import csv
import json
import urllib.request
from io import StringIO

import requests

if __name__ == '__main__':
    # post_url = 'https://api.biocontainers.pro/api/ga4gh/v2/workflows'
    post_url = 'http://localhost:8090/api/ga4gh/v2/workflows'
    data = urllib.request.urlopen(
        "https://raw.githubusercontent.com/BioContainers/workflows/master/workflows.csv").read().decode("utf-8")

    f = StringIO(data)
    reader = csv.DictReader(f, delimiter=',')
    headers = {"Content-Type": "application/json"}

    for row in reader:
        data = json.dumps(row)
        print(data)
        response = requests.post(post_url, data=data, headers=headers)
        print(response)

