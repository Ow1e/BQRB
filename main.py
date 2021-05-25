import requests
import ansi
import sys, os
import qrcode
from time import sleep

url = "https://basiclyqr.xyz"
find_specific_users = url+"/api/user/query/{}/"
find_group_place_ids = url+"/api/location/query/group/{}/"
find_all_users = url+"/api/user/query/all/"

print(ansi.push(50, "="))
print(ansi.logo)
print(ansi.push(50, "="))
print("(1) to track specific, (2) to track group,\n(3) to track all, (4) Create a QR Code,\n(5) Create batch of qr codes")
print(ansi.push(50, "="))


dec = input(">>> ")
print(ansi.push(50, "="))

def sort_func(value):
    return value["id"]

if int(dec) <= 2:
    print("What identifier are you wanting to use: ")
    identifier = str(input(">>> "))

if int(dec) == 1:
    while True:
        data = requests.get(find_specific_users.format(identifier))
        if data.ok:
            json = data.json()
            title_sub = len(str(len(json)))
            print(str(len(json))+" Scans "+ansi.push(43-title_sub, "="))
            sort = sorted(json, key=sort_func, reverse=True)
            for i in range(10):
                if i<len(sort):
                    temp_data = sort[i]
                    print(f"{temp_data['browser']['name']} version {temp_data['browser']['version']} on {temp_data['browser']['platform']}")
                else:
                    print()
        sleep(1)
elif int(dec) == 2:
    while True:
        data = requests.get(find_group_place_ids.format(identifier))
        json = []
        for i in data.json():
            prod = requests.get(find_specific_users.format(i))
            for i in prod.json():
                json.append(i)
        title_sub = len(str(len(json)))
        print(str(len(json))+" Scans "+ansi.push(43-title_sub, "="))
        print(data.url)
        sort = sorted(json, key=sort_func, reverse=True)
        for i in range(10):
            if i<len(sort):
                temp_data = sort[i]
                print(f"Place {temp_data['place']} | {temp_data['browser']['name']} version {temp_data['browser']['version']} on {temp_data['browser']['platform']}")
            else:
                print()
        sleep(10)
elif int(dec) == 3:
    while True:
        data = requests.get(find_all_users)
        if data.ok:
            json = data.json()
            title_sub = len(str(len(json)))
            print(str(len(json))+" Scans | Sorting by recent "+ansi.push(23-title_sub, "="))
            sort = sorted(json, key=sort_func, reverse=True)
            for i in range(10):
                if i<len(sort):
                    temp_data = sort[i]
                    time_render = temp_data['date']
                    print(f"{time_render} | {temp_data['browser']['name']} version {temp_data['browser']['version']} on {temp_data['browser']['platform']}")
                else:
                    print()
        sleep(10)
elif int(dec) == 4:
    params = {
        "name": "BasiclyQR",
        "location": "",
        "group": input("Group Name: ")
    }
    data = requests.post("https://basiclyqr.xyz/createqr", data=params)
    if data.ok == True:
        print("Created QR Code Link!")
    else:
        sys.exit("This didnt work, aborting!")
elif int(dec) == 5:
    loops = input("How many QR Codes: ")
    group = input("Group: ")
    cache = requests.get(find_group_place_ids.format(group)).json()
    params = {
        "name": "BasiclyQR",
        "location": "",
        "group": group
    }
    for i in range(int(loops)):
        data = requests.post("https://basiclyqr.xyz/createqr", data=params)
        if data.ok:
            print("Created QR Code!")
        else:
            print("There was a error with a QR Code!")
    real = requests.get(find_group_place_ids.format(group)).json()
    for i in cache:
        real.remove(i)
    if not os.path.exists("qrcodes/"):
        os.mkdir("qrcodes")
    for i in real:
        qr = qrcode.QRCode(
            version=1,
            box_size=15,
            border=5
        )
        data = url+"/go/{}/".format(i)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img.save(f'qrcodes/{i}.png')
        print(f"Generated Code {i}")