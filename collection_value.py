import requests
import win32gui
from main import get_card_info
from main import Value
from main import get_all_values
import sys
import os

def sortFunc(valueObj):
    name = valueObj.name
    for word in name.split(" "):
        if word[0] == "#":
            return int(word.replace("#", ""))
    return 0

def card_owned(value, my_card_names):
    name = value.name.replace("[", "").replace("]", "").replace("&#39;", "").replace("#", "")
    name = name.replace("'", "")
    name = name.replace("&39;", "")
    match = False
    for my_card_name in my_card_names:
        my_card_name = my_card_name.replace("'", "")
        my_card_name = my_card_name.replace("[", "").replace("]", "").replace("&#39;", "").replace("#", "")
        currentMatch = True
        for word in name.split(" "):
            if word.lower() not in my_card_name.lower():
                currentMatch = False
        if currentMatch: return True
    return False


if __name__ == "__main__" :
    set_urls = ["https://www.pricecharting.com/console/pokemon-base-set?sort=highest-price",
                "https://www.pricecharting.com/console/pokemon-jungle?sort=highest-price",
                "https://www.pricecharting.com/console/pokemon-fossil?sort=highest-price",
                "https://www.pricecharting.com/console/pokemon-team-rocket?sort=highest-price",
                "https://www.pricecharting.com/console/pokemon-gym-heroes?sort=highest-price"]
              #  "https://www.pricecharting.com/console/pokemon-go?sort=highest-price"]
            #    "https://www.pricecharting.com/console/pokemon-team-rocket?sort=highest-price",
            #    "https://www.pricecharting.com/console/pokemon-gym-heroes?sort=highest-price",
              #  "https://www.pricecharting.com/console/pokemon-neo-genesis?sort=highest-price"]
            #    "https://www.pricecharting.com/console/pokemon-gym-challenge?sort=highest-price",
            #    "https://www.pricecharting.com/console/pokemon-neo-discovery?sort=highest-price",
            #    "https://www.pricecharting.com/console/pokemon-neo-revelation?sort=highest-price",
            #    "https://www.pricecharting.com/console/pokemon-neo-destiny?sort=highest-price"]
    # set_urls = ["https://www.pricecharting.com/console/pokemon-neo-genesis?sort=highest-price"]
    all_values = []
    full_set = {'base': [],
                'jungle': [],
                'fossil': [],
                'neo genesis': [],
                'pokemon go': []}
    for set_url in set_urls:
        values = get_all_values(set_url)
        for value in values:
            all_values.append(value)

    for value in all_values:
        name = value.name
        if "#" not in name: continue
        set_name = "base"
        if "jungle" in name: set_name = "jungle"
        if "fossil" in name: set_name = "fossil"
        if "genesis" in name: set_name = "neo genesis"
        if "heroes" in name: set_name = "gym heroes"
        if "rocket" in name: set_name = "team rocket"
        if "pokemon go" in name: set_name = "pokemon go"
        if "1st edition" in name.lower() and "machamp" not in name.lower(): continue
        if "gold border" in name.lower(): continue
        if "no symbol" in name.lower() or "w stamp" in name.lower() or "prerelease" in name.lower(): continue
        if "cosmos" in name.lower() or "shadowless" in name.lower() or "trainer deck" in name.lower() or "black flame" in name.lower() \
                or "error" in name.lower() or "e3" in name.lower() or "poketour" in name.lower(): continue
        if set_name in full_set: full_set[set_name].append(value)
        pass
    #print(full_set["pokemon go"])
    my_card_names = []
    ff = open('collection.txt')
    lines = ff.readlines()
    ff.close()
    unmatched_count = 0
    total_value = 0
    for line in lines:
        quantity = 1
        for word in line.split(" "):
            if word[0] == "x":
                quantity = int(word.replace("x", ""))
                line = line.replace(word, "")
        card_info = get_card_info(line, all_values, "", [])
        if card_info == None:
            unmatched_count += 1
            print("couldn't find", line)
            continue
        value = card_info.ungraded
        if "psa 9" in line and card_info.psa9 != None: value = card_info.psa9
        if "psa 10" in line and card_info.psa10 != None: value = card_info.psa10
        my_card_names.append(card_info.name)
        value = round(value,2)
        value *= quantity
        total_value += value
    print("Total value: £" + str(total_value))

    ff = open('missing.txt', 'w', encoding='utf-8')
    sets = ['base', 'jungle', 'fossil']
    for set in sets:
        set_value = 0
        owned = 0
        set_cards = full_set[set]
        set_cards.sort(key=sortFunc)
        total = len(set_cards)
        for card in full_set[set]:
            is_owned = card_owned(card, my_card_names)
            if is_owned: owned += 1
            if not is_owned:
                ff.write(card.name + "\n")
            if card.ungraded == None: card.ungraded = 0
            set_value += card.ungraded
        percentage = 0
        if len(set_cards) == 0:
            percentage = 0
        else: percentage = round(owned * 100 / len(set_cards),0)
        print(set, str(owned) + " / " + str(len(set_cards)) + " (" + str(percentage) + "%)")
    ff.close()
    sys.exit()
