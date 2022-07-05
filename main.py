import requests
import os
import time
from os.path import exists

class Listing:
    def __init__(self):
        self.title = ""
        self.name = ""
        self.url = ""
        self.price = 0
        self.difference = 0
        self.grade = None
        self.value = 0
        self.raw_difference = 0

class Value:
    def __init__(self):
        self.name = ""
        self.set = None
        self.ungraded = None
        self.psa9 = None
        self.psa10 = None

def myFunc(listing):
  return listing.raw_difference

def url_in_old_file(url, readlines):
    if not exists('out_old.txt'): return False
    url = url.split("?")[0]
    for line in readlines:
        if "url" in line:
            line = line.replace("\n","")
            line_url = "https://" + line.split("https://")[1].strip().split("?")[0]
            if line_url == url:
                return True
    return False

def listing_exists(listings, in_listing):
    for listing in listings:
        listing_url = listing.url.split("?")[0]
        in_listing_url = in_listing.url.split("?")[0]
        if listing_url == in_listing_url:
            return True
    else: return False

def get_card_info(title, values, set):
    title = title.replace("&39;", "")
    title = title.replace("'", "")
    best_match = None
    best_count = -999
    for value in values:
        name = value.name.replace("[", "").replace("]", "").replace("#","")
        name = name.replace("'", "")
        name = name.replace("&39;","")
        name_split = name.split(" ")
        name_split.append(value.set)
        #print("matching:", title, name)
        match = True
        for word in name_split:
            if word.lower == "pack": continue
            if word.lower() not in title.lower():
                match = False
            if word.isnumeric():
                search_str = word + "/"
                if search_str not in title:
                    match = False
        if "base" not in title.lower() and "jungle" not in title.lower() and "fossil" not in title.lower() and "rocket" not in title.lower() and "heroes" not in title.lower() and "genesis" not in title.lower(): match = False
        if match:
            if len(name_split) > best_count:
                best_match = value
                best_count = len(name_split)
    return best_match

def get_values(url):
    exchange_rate = 0.83
    page = requests.get(url)
    page_text = page.text
    page_text_split = page_text.split("<td class=\"title\" title=")
    values = []
    for item in page_text_split:
        item_split = item.split("</td>")
        if (len(item_split)) < 2: continue
        name = item_split[0].split(">")[2].split("<")[0].replace("\n","").strip()
        ungraded_price = item_split[1].split(">")[2].split("<")[0].replace("\n","").strip()
        psa9_price = item_split[2].split(">")[2].split("<")[0].replace("\n","").strip()
        psa10_price = item_split[3].split(">")[2].split("<")[0].replace("\n","").strip()
        if ungraded_price == "": ungraded_price = None
        if psa9_price == "": psa9_price = None
        if psa10_price == "": psa10_price = None
        if ungraded_price != None: ungraded_price = float(ungraded_price.replace("$", "").replace(",", ""))
        if psa9_price != None: psa9_price = float(psa9_price.replace("$", "").replace(",", ""))
        if psa10_price != None: psa10_price = float(psa10_price.replace("$", "").replace(",", ""))
        value = Value()
        value.set = "base"
        if "jungle" in url: value.set = "jungle"
        if "fossil" in url: value.set = "fossil"
        if "rocket" in url: value.set = "team rocket"
        if "heroes" in url: value.set = "gym heroes"
        if "genesis" in url: value.set = "neo genesis"
        value.name = value.set + " " + name
        value.ungraded = ungraded_price
        value.psa9 = psa9_price
        value.psa10 = psa10_price
        if value.ungraded != None: value.ungraded *= exchange_rate
        if value.psa9 != None: value.psa9 *= exchange_rate
        if value.psa10 != None: value.psa10 *= exchange_rate
        values.append(value)
    return values

def get_listings(search_terms, values, buy_it_now, quiet):
    if buy_it_now:
        bin_on = 1 # buy it now, 0 for off, 1 for on, not true/false
        auc_on = 0 # auction, 0 for off, 1 for on, not true/false
    else: # auction
        bin_on = 0
        auc_on = 1
    main_url = "https://www.ebay.co.uk/sch/i.html?_dcat=183454&_fsrp=1&_from=R40&_nkw=%%%SEARCH%%%&_sacat=0&LH_PrefLoc=1&Language=English&LH_PrefLoc=1&LH_BIN=%%%BIN%%%&LH_Auction=%%%AUC%%%"
    listings = []
    listing_count = 0
    last_listing_count = 0
    last_mins_left = -1
    start_time = time.time()
    for i, search_term in enumerate(search_terms):
        time_elapsed = time.time() - start_time
        if time_elapsed < 1: time_elapsed = 1
        done = i+1
        rate = done / time_elapsed
        items_left = len(search_terms) - i+1
        time_left = items_left / rate
        mins_left = int(time_left / 60)
        secs_left = int(time_left - mins_left * 60)
        if quiet:
            if mins_left != last_mins_left:
                print("time remaining: " + str(mins_left) + " mins " + str(secs_left) + " secs - searching: " + search_term)
            pass
        else:
            print("---", search_term, i+1, "/", len(search_terms))
            print("time remaining: " + str(mins_left) + " mins " + str(secs_left) + " secs")
        last_mins_left = mins_left
        for page_num in range(1,100):
            search_url = main_url.replace("%%%SEARCH%%%", search_term)
            search_url = search_url.replace("%%%BIN%%%", str(bin_on))
            search_url = search_url.replace("%%%AUC%%%", str(auc_on))
            new_url = search_url + "&_pgn=" + str(page_num)
            if "base" in search_term:
                new_url += "&Set=Base%20Set"
            if "fossil" in search_term:
                new_url += "&Set=Fossil%20Set"
            if "jungle" in search_term:
                new_url += "&Set=Jungle%20Set"
            if "rocket" in search_term:
                new_url += "&Set=Team%Rocket%Set"
            if "jungle" in search_term:
                new_url += "&Set=Gym%20Heroes"
            if "genesis" in search_term:
                new_url += "&Set=Neo&Genesis"
            page = requests.get(new_url)
            page_text = page.text.replace("<span class=LIGHT_HIGHLIGHT>New listing</span>", "")
            page_text = page_text.replace("<span class=ITALIC>","")
            page_split = page_text.split("\n")
            for i, line in enumerate(page_split):
                if i > 1000: break
                if "£" in line and "item__title>" in line and "item__price" in line:
                    line_split = line.split("item__link")
                    for item in line_split:
                        if "United States" in item:
                            continue
                        if len(item.split("href=")) < 2: continue
                        url = item.split("href=")[1].split("><h3")[0]
                        if len(item.split("item__title>")) <= 1: continue
                        title = item.split("item__title>")[1].split("</h3")[0]
                        excluded = ["played", "h/p", "l/p", "heavy", "spanish", "german", "french", "not holo", "non foil", "non holo",
                                    "non 1st", "not 1st", "set art", "sticker", "non-holo", "heart gold", "soul silver",
                                    "base set 2", "etc", "sword", "xy", "platinum", "diamond and pearl", "empty",
                                    "custom", "resealed", "ex legend", "sword and shield", "black &amp; white",
                                    "shop on ebay", "korean", "portuguese", "celebrations", "anniversary", "shadowless", "sun and moon",
                                    "opened", "error"]
                        do_continue = False
                        for term in excluded:
                            if term in title.lower(): do_continue = True
                        if do_continue: continue
                        if len(item.split("item__price>")) <= 1: continue
                        price = item.split("item__price>")[1].split("</span>")[0]
                        price = price.split("<span class")[0]
                        listing = Listing()
                        listing.title = title
                        listing.url = url
                        if "$" in price: continue
                        if "€" in price: continue
                        if "EUR" in price: continue
                        if "USD" in price: continue
                        price = float(price.replace("£","").replace(",",""))
                        listing.price = price
                        card_info = get_card_info(title, values, "base set")
                        if card_info == None: continue
                        if "booster box" in card_info.name.lower(): continue
                        grade = "ungraded"
                        if "psa 9" in title.lower(): grade = "psa9"
                        if "psa 10" in title.lower(): grade = "psa10"
                        if "?" in title: grade = "ungraded"
                        if card_info == None: continue
                        value = None
                        if grade == "ungraded":
                            value = card_info.ungraded
                            if value == None: continue
                        if grade == "psa9":
                            value = card_info.psa9
                            if value == None: continue
                        if grade == "psa10":
                            value = card_info.psa10
                            if value == None: continue
                        increase = price - value
                        listing.grade = grade
                        listing.name = card_info.name
                        listing.value = value
                        listing.difference = (increase / value) * 100
                        listing.raw_difference = price - value
                        if not listing_exists(listings, listing):
                            listing_count += 1
                            listings.append(listing)
            if last_listing_count == listing_count: break
            last_listing_count = listing_count
    return listings

if __name__ == "__main__" :

    buy_it_now = False
    start_time = time.time()
    os.system("del out_old.txt")
    os.system("copy out.txt out_old.txt")
    set_urls = ["https://www.pricecharting.com/console/pokemon-base-set?sort=highest-price",
                "https://www.pricecharting.com/console/pokemon-jungle?sort=highest-price",
                "https://www.pricecharting.com/console/pokemon-fossil?sort=highest-price",
                "https://www.pricecharting.com/console/pokemon-team-rocket?sort=highest-price",
                "https://www.pricecharting.com/console/pokemon-gym-heroes?sort=highest-price",
                "https://www.pricecharting.com/console/pokemon-neo-genesis?sort=highest-price"]
    #set_urls = ["https://www.pricecharting.com/console/pokemon-neo-genesis?sort=highest-price"]
    all_values = []
    for set_url in set_urls:
        values = get_values(set_url)
        for value in values:
            all_values.append(value)
        #print(set_url, len(values))
    search_terms = []
    for value in all_values:
        name = value.name.replace("[", "").replace("]", "").replace("#", "")
        name = name.replace("&39;", "'")
        search_terms.append("pokemon " + name)
    search_terms.append("pokemon psa 10")
    search_terms.append("pokemon psa 9")
    search_terms.append("pokemon rare holo")
    search_terms.append("pokemon rare holo psa")
    all_listings = get_listings(search_terms, all_values, buy_it_now, False)
    all_listings.sort(key=myFunc)
    print(str(len(all_listings)) + " total listings")
    '''
    i = -1
    print("Best deals:")
    # print top 10 listings
    for listing in all_listings:
        print("title:", listing.title)
        print("name:", listing.name)
        print("url:", listing.url)
        print("grade:", listing.grade)
        print("price: £", listing.price)
        print("value: £", listing.value)
        print("difference:", round(listing.difference,2))
        print("-----")
        i+=1
        if i >= 10: break
    '''
    ff = open('out.txt','w',encoding='utf-8')
    fg = open('fresh.txt','w',encoding='utf-8')
    fh = None
    old_readlines = None
    if exists('out_old.txt'):
        fh = open('out_old.txt','r',encoding='utf-8')
        old_readlines = fh.readlines()
    fresh_count = 0

    for listing in all_listings:
        ff.write("title: " + listing.title + "\n")
        ff.write("name: " + listing.name + "\n")
        ff.write("url: " + listing.url + "\n")
        ff.write("grade: " + listing.grade + "\n")
        ff.write("price: £" + str(listing.price) + "\n")
        ff.write("value: £" + str(listing.value) + "\n")
        ff.write("difference: " + str(round(listing.difference,2)) + "\n")
        ff.write("raw difference: £" + str(round(listing.raw_difference,2)) + "\n")
        ff.write("-----" + "\n")
        if not url_in_old_file(listing.url, old_readlines):
            fresh_count += 1
            fg.write("title: " + listing.title + "\n")
            fg.write("name: " + listing.name + "\n")
            fg.write("url: " + listing.url + "\n")
            fg.write("grade: " + listing.grade + "\n")
            fg.write("price: £" + str(listing.price) + "\n")
            fg.write("value: £" + str(listing.value) + "\n")
            fg.write("difference: " + str(round(listing.difference, 2)) + "\n")
            fg.write("raw difference: £" + str(round(listing.raw_difference, 2)) + "\n")
            fg.write("-----" + "\n")

    ff.close()
    fg.close()
    if fh != None: fh.close()
    print(str(fresh_count) + " fresh listings")
    print("output written to out.txt and fresh.txt")
    print("")
    time_elapsed = time.time() - start_time
    mins_elapsed = time_elapsed / 60
    secs_elapsed = int(time_elapsed - mins_elapsed * 60)
    print("Finished in " + str(mins_elapsed) + " mins " + str(secs_elapsed) + " secs")