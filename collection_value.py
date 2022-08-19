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
            new_word = ""
            for letter in word:
                if letter.isnumeric(): new_word += letter
            return int(new_word.replace("#", ""))
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
                "https://www.pricecharting.com/console/pokemon-gym-heroes?sort=highest-price",
                "https://www.pricecharting.com/console/pokemon-go?sort=highest-price",
                "https://www.pricecharting.com/console/pokemon-evolving-skies?sort=highest-price",
                "https://www.pricecharting.com/console/pokemon-brilliant-stars?sort=highest-price",
                "https://www.pricecharting.com/console/pokemon-shining-fates?sort=highest-price",
                "https://www.pricecharting.com/console/pokemon-fusion-strike?sort=highest-price",
                "https://www.pricecharting.com/console/pokemon-chilling-reign?sort=highest-price",
                "https://www.pricecharting.com/console/pokemon-vivid-voltage?sort=highest-price",
                "https://www.pricecharting.com/console/pokemon-hidden-fates?sort=highest-price",
                "https://www.pricecharting.com/console/pokemon-darkness-ablaze?sort=highest-price",
                "https://www.pricecharting.com/console/pokemon-rebel-clash?sort=highest-price",
                "https://www.pricecharting.com/console/pokemon-astral-radiance?sort=highest-price",
                "https://www.pricecharting.com/console/pokemon-celebrations?sort=highest-price",
                "https://www.pricecharting.com/console/pokemon-burning-shadows?sort=highest-price"]
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
        if "evolving skies" in name: set_name = "evolving skies"
        if "shining fates" in name: set_name = "shining fates"
        if "brilliant stars" in name: set_name = "brilliant stars"
        if "1st edition" in name.lower() and "machamp" not in name.lower(): continue
        if "gold border" in name.lower(): continue
        if "no symbol" in name.lower() or "w stamp" in name.lower() or "prerelease" in name.lower(): continue
        if "cosmos" in name.lower() or "shadowless" in name.lower() or "trainer deck" in name.lower() or "black flame" in name.lower() \
                or "error" in name.lower() or "e3" in name.lower() or "poketour" in name.lower(): continue
        if set_name in full_set: full_set[set_name].append(value)
        pass
    #print(full_set["pokemon go"])
    all_files = True
    my_card_names = []
    ff = None
    lines = []
    if not all_files:
        ff = open('collection.txt')
        lines = ff.readlines()
        ff.close()
    if all_files:
        files = ['collections/vintage.txt', 'collections/biggie_hits.txt', 'collections/wiidevil.txt']
        for filename in files:
            ff = open(filename, 'r')
            readlines = ff.readlines()
            for line in readlines:
                lines.append(line)
            ff.close()
    unmatched_count = 0
    total_value = 0
    get_graded = []
    for line in lines:
        quantity = 1
        for word in line.split(" "):
            if word[0] == "x" and word == line.split(" ")[len(line.split(" ")) - 1]:
                quantity = int(word.replace("x", ""))
                line = line.replace(word, "")
        card_info = get_card_info(line, all_values, "", [])
        if card_info == None:
            unmatched_count += 1
            print(" --- couldn't find", line)
            continue
        value = card_info.ungraded
        if "psa 9" in line and card_info.psa9 != None: value = card_info.psa9
        if "psa 10" in line and card_info.psa10 != None: value = card_info.psa10
        if card_info.psa10 != None:
            if card_info.psa10 - card_info.ungraded >= 100:
                get_graded.append((card_info.name, card_info.ungraded, card_info.psa10))
        my_card_names.append(card_info.name)
        value = round(value,2)
        print(card_info.name, "£" + str(value * quantity))
        value *= quantity
        total_value += value
    print("Total value: £" + str(total_value))

    ff = open('missing.txt', 'w', encoding='utf-8')
    sets = ['base', 'jungle', 'fossil']
    do_sets = False
    if do_sets:
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
    grading = False
    if grading:
        print("Get graded:")
        max_return = 0
        for card in get_graded:
            print(card[0], "£" + str(card[1]), "£" + str(card[2]))
            max_return += card[2] - card[1]
        print("Max return: £" + str(max_return))
        print("Return after grading costs: £" + str(max_return - (len(get_graded) * 50)))
    ff.close()
    sys.exit()
