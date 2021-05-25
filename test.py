import requests

params = {
    "name": "OwieDidSomeTests",
    "location": "",
    "group": ""
}
data = requests.post("https://basiclyqr.xyz/createqr", data=params)