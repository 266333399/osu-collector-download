import threading
import requests
import time
import re
import os

beatconnectstatus = 0
nerinyanstatus = 0
catboystatus = 0
Beatmaps = []

def start():
    threading.Thread(target=check, args=(0,)).start()
    threading.Thread(target=check, args=(1,)).start()
    threading.Thread(target=check, args=(2,)).start()
    threading.Thread(target=prompt).start()

def check(number):
    global beatconnectstatus, nerinyanstatus, catboystatus
    match number:
        case 0:
            if requests.get("https://beatconnect.io/").status_code == 200:
                print("beatconnect | successful")
                beatconnectstatus = 1
            else:
                print("beatconnect | error")
                beatconnectstatus = 0
        case 1:
            if requests.get("https://nerinyan.moe/main").status_code == 200:
                print("nerinyan | successful")
                nerinyanstatus = 1
            else:
                print("nerinyan | error")
                nerinyanstatus = 0
        case 2:
            if requests.get("https://catboy.best/").status_code == 200:
                print("catboy | successful")
                catboystatus = 1
            else:
                print("catboy | error")
                catboystatus = 0

def prompt():
    print("Insert colletion ID: ")
    collectionID = input()
    if re.search("^[0-9]*$", collectionID) is None:
        print("not an ID")
        prompt()
    else:
        print("successful")
        beatmap(collectionID)

def beatmap(ID):
    if requests.get("https://osucollector.com/api/collections/" + ID + "/beatmapsV2?perPage=100"):
        url = "https://osucollector.com/api/collections/" + ID + "/beatmapsV2?perPage=100"
        x = requests.get(url).json()
        while x["hasMore"]:
            amount = len(x["beatmaps"])
            for i in range(amount):
                Beatmaps.append(str(x["beatmaps"][i]["beatmapset"]["id"]))
            x = requests.get(url + "&cursor=" + str(x["nextPageCursor"])).json()
        else:
            amount = len(x["beatmaps"])
            for i in range(amount):
                Beatmaps.append(str(x["beatmaps"][i]["beatmapset"]["id"]))
        duplicate()
    else:
        print("fail")

def duplicate():
    downloaded = [item.replace('.osk', '') for item in os.listdir("beatmaps/")]
    for i in downloaded[:]:
        if i in Beatmaps:
            Beatmaps.remove(i)
            downloaded.remove(i)
        else:
            print("2")
    split()

def split():
    amount = len(Beatmaps)
    split = beatconnectstatus + nerinyanstatus + catboystatus
    size = amount // split
    remainder = amount % split
    split1 = size + (1 if remainder > 0 else 0)
    split2 = size + (1 if remainder > 1 else 0)
    split3 = size
    beatconnectarray = Beatmaps[:split1] if beatconnectstatus == 1 else []
    nerinyanarray = Beatmaps[split1:split1 + split2] if nerinyanstatus == 1 else []
    catboyarray = Beatmaps[split1 + split2:] if catboystatus == 1 else []
    queue(beatconnectarray, nerinyanarray, catboyarray)
    print(beatconnectarray)
    print(nerinyanarray)
    print(catboyarray)

def queue(a1, a2, a3):
    if beatconnectstatus == 1:
        threading.Thread(target=download, args=(0, a1,)).start()
    else:
        pass
    if nerinyanstatus == 1:
        threading.Thread(target=download, args=(1, a2,)).start()
    else:
        pass
    if catboystatus == 1:
        threading.Thread(target=download, args=(2, a3,)).start()
    else:
        pass

def download(number, array):
    match number:
        case 0:
            for i in array[:]:
                try:
                    site = requests.get("https://beatconnect.io/b/" + i)
                    if site.status_code == 200:
                        if site.content:
                            with open("beatmaps/" + i + ".osz", mode="wb") as file:
                                file.write(site.content)
                                print("beatconnect | Downloaded | " + i + " | Downlaods Left: " + str(len(array)))
                                array.remove(i)
                                time.sleep(10)
                        else:
                            print("beatconnect | Failed 1 | " + i + " | Downlaods Left: " + str(len(array)))
                            Beatmaps.remove(i)
                            array.remove(i)
                    else:
                        print("beatconnect | Failed 2 | " + i + " | Downlaods Left: " + str(len(array)))
                        Beatmaps.remove(i)
                        array.remove(i)
                except Exception as e:
                    print("beatconnect | Failed 3 | " + i + " | Downlaods Left: " + str(len(array)))
                    Beatmaps.remove(i)
                    array.remove(i)

        case 1:
            for i in array[:]:
                try:
                    site = requests.get("https://api.nerinyan.moe/d/" + i)
                    if site.status_code == 200:
                        if site.content:
                            with open("beatmaps/" + i + ".osz", mode="wb") as file:
                                file.write(site.content)
                                print("nerinyan | Downloaded | " + i + " | Downlaods Left: " + str(len(array)))
                                array.remove(i)
                                time.sleep(10)
                        else:
                            print("nerinyan | Failed 1 | " + i + " | Downlaods Left: " + str(len(array)))
                            Beatmaps.remove(i)
                            array.remove(i)
                    else:
                        print("nerinyan | Failed 2 | " + i + " | Downlaods Left: " + str(len(array)))
                        Beatmaps.remove(i)
                        array.remove(i)
                except Exception as e:
                    print("nerinyan | Failed 3 | " + i + " | Downlaods Left: " + str(len(array)))
                    Beatmaps.remove(i)
                    array.remove(i)

        case 2:
            for i in array[:]:
                try:
                    site = requests.get("https://catboy.best/d/" + i)
                    if site.status_code == 200:
                        if site.content:
                            with open("beatmaps/" + i + ".osz", mode="wb") as file:
                                file.write(site.content)
                                print("catboy | Downloaded | " + i + " | Downlaods Left: " + str(len(array)))
                                array.remove(i)
                                time.sleep(10)
                        else:
                            print("catboy | Failed 1 | " + i + " | Downlaods Left: " + str(len(array)))
                            Beatmaps.remove(i)
                            array.remove(i)
                    else:
                        print("catboy | Failed 2 | " + i + " | Downlaods Left: " + str(len(array)))
                        Beatmaps.remove(i)
                        array.remove(i)
                except Exception as e:
                    print("catboy | Failed 3 | " + i + " | Downlaods Left: " + str(len(array)))
                    Beatmaps.remove(i)
                    array.remove(i)

start()