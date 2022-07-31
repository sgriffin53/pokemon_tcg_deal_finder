import requests
import win32gui
from main import get_card_info
from main import Value
from main import get_values
from main import get_all_values
global title

def get_value(value):
    exchange_rate = 0.83
    name = value.name.replace("[", "").replace("]", "").replace("#", "")
    name = name.replace("'", "")
    name = name.replace("&39;", "")
    first_dir = "pokemon-base-set"
    if "jungle" in name: first_dir = "pokemon-jungle"
    if "fossil" in name: first_dir = "pokemon-fossil"
    if "team rocket" in name: first_dir = "pokemon-team-rocket"
    if "gym challenge" in name: first_dir = "pokemon-gym-challenge"
    if "gym heroes" in name: first_dir = "pokemon-gym-heroes"
    if "neo genesis" in name: first_dir = "pokemon-neo-genesis"
    if "neo revelation" in name: first_dir = "pokemon-neo-revelation"
    if "neo discovery" in name: first_dir = "pokemon-neo-discovery"
    if "neo destiny" in name: first_dir = "pokemon-neo-destiny"
    threshold = 0
    if "jungle" in name or "fossil" in name or "base" in name:
        threshold = 0
    else:
        threshold = 1
    second_dir = ""
    print("Card: " + name)
    for i, token in enumerate(name.split(" ")):
        if i <= threshold: continue
        second_dir += token
        if i != len(name.split(" ")) - 1:
            second_dir += "-"
    second_dir = second_dir.strip()
    url = "https://www.pricecharting.com/game/" + first_dir + "/" + second_dir
    url = url.lower()
    print(url)
    page = requests.get(url)
    print(page)
    text = ""
    if "<td id=\"used_price\">" in page.text:
        text = page.text.split("<td id=\"used_price\">")[1]
        ungraded_price = text.split("</span")[0].split(">")[1].strip().replace("\n","").replace("$", "")
        ungraded_price = ungraded_price.replace(",","")
        if ungraded_price == "N/A": ungraded_price = 0
        ungraded_price = float(ungraded_price)
        ungraded_price *= exchange_rate
        ungraded_price = round(ungraded_price,2)
        print("Ungraded: £" + str(ungraded_price))
        text = page.text.split("<td id=\"complete_price\">")[1]
        psa7_price = text.split("</span")[0].split(">")[1].strip().replace("\n","").replace("$", "")
        psa7_price = psa7_price.replace(",","")
        if psa7_price == "N/A": psa7_price = "0"
        psa7_price = float(psa7_price)
        psa7_price *= exchange_rate
        psa7_price = round(psa7_price,2)
        print("PSA 7: £" + str(psa7_price))
        text = page.text.split("<td id=\"new_price\">")[1]
        psa8_price = text.split("</span")[0].split(">")[1].strip().replace("\n","").replace("$", "")
        psa8_price = psa8_price.replace(",","")
        if psa8_price == "N/A": psa8_price = "0"
        psa8_price = float(psa8_price)
        psa8_price *= exchange_rate
        psa8_price = round(psa8_price,2)
        print("PSA 8: £" + str(psa8_price))
        text = page.text.split("<td id=\"graded_price\" class=\"tablet-portrait-hidden\">")[1]
        psa9_price = text.split("</span")[0].split(">")[1].strip().replace("\n","").replace("$", "")
        psa9_price = psa9_price.replace(",","")
        if psa9_price == "N/A": psa9_price = "0"
        psa9_price = float(psa9_price)
        psa9_price *= exchange_rate
        psa9_price = round(psa9_price,2)
        print("PSA 9: £" + str(psa9_price))
        text = page.text.split("<td id=\"manual_only_price\" class=\"tablet-portrait-hidden\">")[1]
        psa10_price = text.split("</span")[0].split(">")[1].strip().replace("\n","").replace("$", "")
        if psa10_price == "N/A": psa10_price = "0"
        psa10_price = float(psa10_price.replace(",",""))
        psa10_price *= exchange_rate
        psa10_price = round(psa10_price,2)
        print("PSA 10: £" + str(psa10_price))
    #text = page.text
    #print(text)
    pass

def get_card_value(title):
    set_urls = []
    if "base" in title.lower(): set_urls = ["https://www.pricecharting.com/console/pokemon-base-set?sort=highest-price"]
    if "jungle" in title.lower(): set_urls = ["https://www.pricecharting.com/console/pokemon-jungle?sort=highest-price"]
    if "fossil" in title.lower(): set_urls = ["https://www.pricecharting.com/console/pokemon-fossil?sort=highest-price"]
    if "team rocket" in title.lower(): set_urls = ["https://www.pricecharting.com/console/pokemon-team-rocket?sort=highest-price"]
    if "gym challenge" in title.lower(): set_urls = ["https://www.pricecharting.com/console/pokemon-gym-challenge?sort=highest-price"]
    if "gym heroes" in title.lower(): set_urls = ["https://www.pricecharting.com/console/pokemon-gym-heroes?sort=highest-price"]
    if "neo discovery" in title.lower(): set_urls = ["https://www.pricecharting.com/console/pokemon-neo-discovery?sort=highest-price"]
    if "neo genesis" in title.lower(): set_urls = ["https://www.pricecharting.com/console/pokemon-neo-genesis?sort=highest-price"]
    if "neo revelation" in title.lower(): set_urls = ["https://www.pricecharting.com/console/pokemon-neo-revelation?sort=highest-price"]
    if "neo destiny" in title.lower(): set_urls = ["https://www.pricecharting.com/console/pokemon-neo-destiny?sort=highest-price"]

    all_values = []
    values = []
    for set_url in set_urls:
        values = get_all_values(set_url)
        for value in values:
            all_values.append(value)
    card_info = get_card_info(title,all_values, "", [])
    return card_info
    '''
    best_match = None
    best_count = 0
    for value in values:
        name = value.name.replace("[", "").replace("]", "").replace("#","")
        name = name.replace("'", "")
        name = name.replace("&39;","")
        name_split = name.split(" ")
        num_in_name = False
        for word in name_split:
            if word.isnumeric():
                num_in_name = True
        if not num_in_name:
            name_split.append(value.set)
        #name_split.append(value.set)
        #print("matching:", title, name)
        match = True
        for word in name_split:
            #if "kangaskhan" in name.lower(): print("before", name, word, match)
            if word.lower == "pack": continue
            if word.lower == "shadowless": continue
            if value.set in name_split:
                if word.isnumeric() and word.lower() not in title.lower():
                    found_slash = False
                    if "/" in title: found_slash = True
                    if "#" in title: found_slash = True
                    if not found_slash: continue
            if word.lower() not in title.lower():
                match = False
            if word.isnumeric():
                search_str = word + "/"
                search_str2 = word + " /"
                search_str3 = "#" + word
                search_str4 = "no" + word
                if search_str not in title and search_str2 not in title and search_str3 not in title and search_str4 not in title:
                    match = False
        if "base" not in title.lower() and "jungle" not in title.lower() and "fossil" not in title.lower() and "rocket" not in title.lower() \
                and "heroes" not in title.lower() and "neo" not in title.lower() and "challenge" not in title.lower():
            match = False
            pass
        if match:
            if len(name_split) > best_count:
                best_match = value
                best_count = len(name_split)
    #if best_match == None:
     #   print(title)
    '''
    return best_match

def winEnumHandler( hwnd, ctx ):
    global title
    if win32gui.IsWindowVisible( hwnd ):
        #print (hex(hwnd), win32gui.GetWindowText( hwnd ))
        window_title = win32gui.GetWindowText( hwnd )
        if "eBay" in window_title: title = win32gui.GetWindowText( hwnd )
        pass

def get_title( hwnd, ctx):
    if win32gui.IsWindowVisible( hwnd ):
        title = win32gui.GetWindowText(hwnd)
        if "eBay" in title:
            return title.split("|")[0]
    return "none"

def get_browser_title():
    #title = win32gui.EnumWindows(winEnumHandler, None)
   # return title
    pass
print("Getting value...")
title = ""
win32gui.EnumWindows(winEnumHandler, None)
value = get_card_value(title)
if value == None:
    print("No match.")
else:
    get_value(value)
print("")
esc = input("Press enter to exit")