
import requests

def print_repo(data, next, type ):
    for entry in data['items']:
        license = ""
        if 'license' in entry and entry['license'] is not None and 'spdx_id' in entry['license']:
            license = entry['license']['spdx_id']

        if entry['description'] == None:
            entry['description'] = ""
        else:
            entry['description'] = entry['description'].replace(",", " ")

        print(entry['owner']['login'] + "," + entry['html_url'] + "," + entry['full_name'] + "," + entry['description'] + "," + license + "," + type)
    if(next != None):
        res = requests.get(next)
        if(res.status_code == 200):
            if 'next' in res.links:
                print_repo(res.json(), res.links['next']['url'], type)
            else:
                print_repo(res.json(), None, type)


if __name__ == "__main__":

    res = requests.get("https://api.github.com/search/repositories?q=language:nextflow&access_token=8936dc997ddbe7074ff087ab42179412fcee0fc9")
    if(res.status_code == 200):
        data = res.json()
        print_repo(data, res.links['next']['url'], "NF")

    res = requests.get("https://api.github.com/search/repositories?q=language:Common+Workflow+Language&access_token=8936dc997ddbe7074ff087ab42179412fcee0fc9")
    if (res.status_code == 200):
        data = res.json()
        print_repo(data, res.links['next']['url'], "CWL")


