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
        self.buy_it_now = None
        self.how_found = None
        self.html = ""

class Value:
    def __init__(self):
        self.name = ""
        self.set = None
        self.ungraded = None
        self.psa7 = None
        self.psa8 = None
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

def get_card_info(title, values, set, no_matches):
    title = title.replace("&39;", "")
    title = title.replace("'", "")
    best_match = None
    best_count = -999
    if "base" not in title.lower() and "jungle" not in title.lower() and "fossil" not in title.lower() and "rocket" not in title.lower() \
            and "heroes" not in title.lower() and "neo" not in title.lower() and "challenge" not in title.lower() and "pokemon go" not in title.lower()\
            and "evolving skies" not in title.lower() and "shining fates" not in title.lower() and "brilliant stars" not in title.lower()\
            and "fusion strike" not in title.lower() and "chilling reign" not in title.lower() and "vivid voltage" not in title.lower()\
            and "hidden fates" not in title.lower() and "darkness ablaze" not in title.lower() and "rebel clash" not in title.lower()\
            and "astral radiance" not in title.lower() and "celebrations" not in title.lower() and "burning shadows" not in title.lower():
        return None
    for value in values:
        name = value.name.replace("[", "").replace("]", "").replace("#","")
        name = name.replace("'", "")
        name = name.replace("&39;","")
        set_size = 0
        if "base" in value.set: set_size = 102
        if "jungle" in value.set: set_size = 64
        if "fossil" in value.set: set_size = 62
        if "rocket" in value.set: set_size = 83
        if "heroes" in value.set: set_size = 132
        if "challenge" in value.set: set_size = 132
        if "genesis" in value.set: set_size = 111
        if "discovery" in value.set: set_size = 75
        if "revelation" in value.set: set_size = 66
        if "destiny" in value.set: set_size = 113
        if "pokemon go" in value.set: set_size = 79
        sets = ["base", "jungle", "fossil", "rocket", "heroes", "challenge", "genesis", "discovery", "revelation", "destiny", "pokemon go", "evolving skies"\
                "shining fates", "brilliant stars", "fusion strike", "chilling reign", "vivid voltage", "hidden fates", "darkness ablaze", "rebel clash",\
                "astral radiance", "celebrations", "burning shadows"]
        do_continue = False
        for set in sets:
            if set in title.lower() and set not in value.name: do_continue = True
        if do_continue: continue
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
        num_match = False
        for word in name_split:
            if word.isnumeric():
                search_str = word + "/"
                search_str2 = word + " /"
                search_str3 = "#" + word
                search_str4 = "no" + word
                if search_str in title or search_str2 in title or search_str3 in title or search_str4 in title:
                    num_match = True
                    break
        do_continue = False
        for word in name_split:
            if word.lower == "pack": continue
            #if word.lower == "shadowless": continue
            if word.lower == "pokemon": continue
            if value.set in name_split:
                if word.isnumeric() and word.lower() not in title.lower():
                    found_slash = False
                    if "/" in title: found_slash = True
                    if "#" in title: found_slash = True
                    if not found_slash: continue
                if value.set not in title.lower():
                    if word.lower() in value.set and num_match:
                        set_match1 = "/" + str(set_size)
                        set_match2 = "/ " + str(set_size)
                        if set_match1 in title.lower(): continue
                        if set_match2 in title.lower(): continue
            if word.lower() not in title.lower():
                do_continue = True
                break
            if word.isnumeric():
                search_str = word + "/"
                search_str2 = word + " /"
                search_str3 = "#" + word
                search_str4 = "no" + word
                if search_str not in title and search_str2 not in title and search_str3 not in title and search_str4 not in title:
                    do_continue = True
                    break
        #if "pikachu" in value.name.lower(): print(title, do_continue)
        if do_continue: continue
        if match:
            if len(name_split) > best_count:
                best_match = value
                best_count = len(name_split)
    if best_match != None and best_match.set not in title.lower():
        print(title, "::", best_match.name)
    return best_match

def get_all_values(url):
    print(url)
    exchange_rate = 0.83
    values = []
    for page_num in range(1,10):
        cursor_val = str( (page_num - 1) * 50)
        myobj = {'sort': 'highest-price',
                 'cursor': cursor_val
        }
        page = requests.post(url, myobj)
        page_text = page.text
        page_text_split = page_text.split("<td class=\"title\" title=")
        for item in page_text_split:
            item_split = item.split("</td>")
            if (len(item_split)) < 2: continue
            name = item_split[0].split(">")[2].split("<")[0].replace("\n","").strip()
            ungraded_price = None
            psa9_price = None
            psa10_price = None
            if len(item_split) >= 2 and len(item_split[1].split(">")) >= 3: ungraded_price = item_split[1].split(">")[2].split("<")[0].replace("\n","").strip()
            if len(item_split) >= 3 and len(item_split[2].split(">")) >= 3: psa9_price = item_split[2].split(">")[2].split("<")[0].replace("\n","").strip()
            if len(item_split) >= 4 and len(item_split[3].split(">")) >= 3: psa10_price = item_split[3].split(">")[2].split("<")[0].replace("\n","").strip()
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
            if "neo-genesis" in url: value.set = "neo genesis"
            if "gym-challenge" in url: value.set = "gym challenge"
            if "neo-discovery" in url: value.set = "neo discovery"
            if "neo-revelation" in url: value.set = "neo revelation"
            if "neo-destiny" in url: value.set = "neo destiny"
            if "pokemon-go" in url: value.set = "pokemon go"
            if "evolving-skies" in url: value.set = "evolving skies"
            if "shining-fates" in url: value.set = "shining fates"
            if "brilliant-stars" in url: value.set = "brilliant stars"
            if "fusion-strike" in url: value.set = "fusion strike"
            if "chilling-reign" in url: value.set = "chilling reign"
            if "vivid-voltage" in url: value.set = "vivid voltage"
            if "hidden-fates" in url: value.set = "hidden fates"
            if "darkness-ablaze" in url: value.set = "darkness ablaze"
            if "rebel-clash" in url: value.set = "rebel clash"
            if "astral-radiance" in url: value.set = "astral radiance"
            if "celebrations" in url: value.set = "celebrations"
            if "burning-shadows" in url: value.set = "burning shadows"
            value.name = name
            num_in_name = False
            for word in value.name.replace("#", "").split(" "):
                #if "Charizard" in name: print(word)
                if word.isnumeric():
                    num_in_name = True
                 #   if "Charizard" in name: print(word)
            if not num_in_name: value.name = name
            value.ungraded = ungraded_price
            value.psa9 = psa9_price
            value.psa10 = psa10_price
            if value.ungraded != None: value.ungraded *= exchange_rate
            if value.psa9 != None: value.psa9 *= exchange_rate
            if value.psa10 != None: value.psa10 *= exchange_rate
            if value.name == "": continue
            value.name = value.set + " " + value.name
            in_range = True
            if in_range:
                if (len(value.name.split(" "))) >= 2: values.append(value)
    return values

def get_values(url):
    exchange_rate = 0.83
    print(url)
    values = []
    for page_num in range(1,10):
        cursor_val = str( (page_num - 1) * 50)
        myobj = {'sort': 'highest-price',
                 'cursor': cursor_val
        }
        page = requests.post(url, myobj)
        page_text = page.text
        page_text_split = page_text.split("<td class=\"title\" title=")
        for item in page_text_split:
            item_split = item.split("</td>")
            if (len(item_split)) < 2: continue
            name = item_split[0].split(">")[2].split("<")[0].replace("\n","").strip()
            ungraded_price = None
            psa9_price = None
            psa10_price = None
            if len(item_split) >= 2 and len(item_split[1].split(">")) >= 3: ungraded_price = \
            item_split[1].split(">")[2].split("<")[0].replace("\n", "").strip()
            if len(item_split) >= 3 and len(item_split[2].split(">")) >= 3: psa9_price = \
            item_split[2].split(">")[2].split("<")[0].replace("\n", "").strip()
            if len(item_split) >= 4 and len(item_split[3].split(">")) >= 3: psa10_price = \
            item_split[3].split(">")[2].split("<")[0].replace("\n", "").strip()
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
            if "neo-genesis" in url: value.set = "neo genesis"
            if "gym-challenge" in url: value.set = "gym challenge"
            if "neo-discovery" in url: value.set = "neo discovery"
            if "neo-revelation" in url: value.set = "neo revelation"
            if "neo-destiny" in url: value.set = "neo destiny"
            if "pokemon-go" in url: value.set = "pokemon go"
            if "evolving-skies" in url: value.set = "evolving skies"
            if "shining-fates" in url: value.set = "shining fates"
            if "brilliant-stars" in url: value.set = "brilliant stars"
            if "fusion-strike" in url: value.set = "fusion strike"
            if "chilling-reign" in url: value.set = "chilling reign"
            if "vivid-voltage" in url: value.set = "vivid voltage"
            if "hidden-fates" in url: value.set = "hidden fates"
            if "darkness-ablaze" in url: value.set = "darkness ablaze"
            if "rebel-clash" in url: value.set = "rebel clash"
            if "astral-radiance" in url: value.set = "astral radiance"
            if "celebrations" in url: value.set = "celebrations"
            if "burning-shadows" in url: value.set = "burning shadows"
            value.name = name
            num_in_name = False
            for word in value.name.replace("#", "").split(" "):
                #if "Charizard" in name: print(word)
                if word.isnumeric():
                    num_in_name = True
                 #   if "Charizard" in name: print(word)
            if not num_in_name: value.name = name
            value.ungraded = ungraded_price
            value.psa9 = psa9_price
            value.psa10 = psa10_price
            if value.ungraded != None: value.ungraded *= exchange_rate
            if value.psa9 != None: value.psa9 *= exchange_rate
            if value.psa10 != None: value.psa10 *= exchange_rate
            value.name = value.set + " " + value.name
            in_range = True
            if (value.ungraded == None or value.ungraded < 65) \
                and (value.psa9 == None or value.psa9 < 145) \
                and (value.psa10 == None or value.psa10 < 235):
                in_range = False
            if in_range: values.append(value)
    return values

def get_listings(search_terms, values, buy_it_now, quiet, no_matches):
    pokemon_names = []
    ff = open('pokemon_names.txt','r',encoding='utf-8')
    lines = ff.readlines()
    for pokemon in lines:
        pokemon = pokemon.replace("\n","")
        pokemon_names.append(pokemon)
    ff.close()
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
    last_found_page = 0
    last_mins_left = -1
    start_time = time.time()
    done_minutes = []
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
            if mins_left not in done_minutes:
                print("Getting Listings - time remaining: " + str(mins_left) + " mins " + str(secs_left) + " secs - searching: " + search_term + " listings: " + str(len(listings)))
                if i+1 >= 5: done_minutes.append(mins_left)
        else:
            print("---", search_term, i+1, "/", len(search_terms))
            print("time remaining: " + str(mins_left) + " mins " + str(secs_left) + " secs")
        pokemon_name = None
      #  print(pokemon_names)
        for pokemon in pokemon_names:
            if pokemon.lower() in search_term.lower().split(" "):
                pokemon_name = pokemon.lower()
        all_urls = []
        duplicate_url = False
        for page_num in range(1,100):
            search_url = main_url.replace("%%%SEARCH%%%", search_term)
            search_url = search_url.replace("%%%BIN%%%", str(bin_on))
            search_url = search_url.replace("%%%AUC%%%", str(auc_on))
            new_url = search_url + "&_pgn=" + str(page_num)
            '''
            if "base" in search_term:
                new_url += "&Set=Base%20Set"
            if "fossil" in search_term:
                new_url += "&Set=Fossil%20Set"
            if "jungle" in search_term:
                new_url += "&Set=Jungle%20Set"
            if "rocket" in search_term:
                new_url += "&Set=Team%20Rocket%20Set"
            if "jungle" in search_term:
                new_url += "&Set=Gym%20Heroes"
            if "neo genesis" in search_term:
                new_url += "&Set=Neo%20Genesis"
            if "gym challenge" in search_term:
                new_url += "&Set=Gym%20Challenge"
            if "neo discovery" in search_term:
                new_url += "&Set=Neo%20Discovery"
            if "neo revelation" in search_term:
                new_url += "&Set=Neo%20Revelation"
            if "neo destiny" in search_term:
                new_url += "&Set=Neo%20Destiny"
            '''
           # if pokemon_name != None:
           #     new_url += "&Character=" + pokemon_name.capitalize()
            #print("--")
            #print(search_term)
            #print(new_url)
            page = requests.get(new_url)
            page_text = page.text.replace("<span class=LIGHT_HIGHLIGHT>New listing</span>", "")
            page_text = page_text.replace("<span class=ITALIC>","")
            page_split = page_text.split("\n")
            from_in = False
            for i, line in enumerate(page_split):
                if "£" in line and "item__title>" in line and "item__price" in line:
                    line_split = line.split("item__link")
                    for item in line_split:
                        if "united states" in item.lower() or "canada" in item.lower() or "australia" in item.lower():
                            from_in = True
                        if "United States" in item or "Canada" in item or "Australia" in item:
                            continue
                        if len(item.split("href=")) < 2: continue
                        url = item.split("href=")[1].split("><h3")[0]
                        short_url = url.split("?")[0]
                        if len(item.split("item__title>")) <= 1: continue
                        title = item.split("item__title>")[1].split("</h3")[0]
                        if short_url in all_urls:
                            duplicate_url = True
                            break
                        else: all_urls.append(short_url)

                       # print(title, all_titles)
                        excluded = ["played", "h/p", "l/p", "heavy", "spanish", "german", "french", "not holo", "non foil", "non holo",
                                    "non 1st", "not 1st", "set art", "sticker", "non-holo", "heart gold", "soul silver",
                                    "base set 2", "etc", "sword", "xy", "platinum", "diamond and pearl", "empty",
                                    "custom", "resealed", "ex legend", "sword and shield", "black &amp; white",
                                    "shop on ebay", "korean", "portuguese", "celebrations", "anniversary", "shadowless", "sun and moon",
                                    "opened", "error", "sun &amp; moon", "sun & moon", "champions path", "champion&amp;s path", "champion's path",
                                    "fusion strike", "astral radiance", "roaring skies", "japanese"]
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
                        if "bids" in item: listing.buy_it_now = False
                        else: listing.buy_it_now = True
                        card_info = get_card_info(title, values, "base set", no_matches)
                        #print(title, ":", card_info)
                        if card_info == None:
                            no_matches.append(title)
                            continue
                        if "booster box" in card_info.name.lower(): continue
                        grade = "ungraded"
                        if "psa 9" in title.lower() or "psa9" in title.lower(): grade = "psa9"
                        if "psa 10" in title.lower() or "psa10" in title.lower(): grade = "psa10"
                        if "?" in title: grade = "ungraded"
                        if card_info == None: continue
                        value = None
                        if grade == "ungraded":
                            value = card_info.ungraded
                            if value == None: continue
                        if grade == "psa9":
                            value = card_info.psa9
                            if value == None:
                                if card_info.ungraded != None: value = card_info.ungraded
                            if value == None: continue
                        if grade == "psa10":
                            value = card_info.psa10
                            if value == None:
                                if card_info.psa9 != None: value = card_info.psa9
                                elif card_info.ungraded != None: value = card_info.ungraded
                            if value == None: continue
                        increase = price - value
                        listing.grade = grade
                        listing.name = card_info.name
                        listing.value = value
                        listing.difference = (increase / value) * 100
                        listing.raw_difference = price - value
                        listing.how_found = "main listings"
                     #   listing.html += item
                        if not listing_exists(listings, listing):
                            listing_count += 1
                            listings.append(listing)
                            last_found_page = page_num
            #print(title, page_num, listing_count)
            #if "shop on ebay" in title: continue
            if duplicate_url: break
            if from_in: break
            #if last_listing_count == listing_count: break
            #print(title, page_num, listing_count)
            #if page_num - last_found_page >= 3: break
            last_listing_count = listing_count
    return listings

def get_seller_urls(listing_urls):
    seller_urls = []
    done_minutes = []
    start_time = time.time()
    for i, url in enumerate(listing_urls):
        done = i+1
        time_elapsed = time.time() - start_time
        if time_elapsed < 1: time_elapsed = 1
        rate = done / time_elapsed
        items_left = len(listing_urls) - i+1
        time_left = items_left / rate
        mins_left = int(time_left / 60)
        secs_left = int(time_left - mins_left * 60)
        if mins_left not in done_minutes:
            print("Getting Seller URLS - time remaining: " + str(mins_left) + " mins " + str(secs_left) + " secs - searching: " + url.split("?")[0] + " URLS: " + str(len(seller_urls)))
            if i+1 >= 5: done_minutes.append(mins_left)
        page = requests.get(url)
        page_text = page.text
        page_split = page_text.split("\n")
        for line in page_split:
            #print(line)
            match_string = "https://www.ebay.co.uk/usr"
            if match_string in line:
                seller = line.split(match_string)[1].split("\"")[0].split("?")[0].replace("/","")
                seller_url = "https://www.ebay.co.uk/sch/" + seller + "/m.html?_dmd=2&_dkr=1&iconV2Request=true&_ssn=" + seller + "&_oac=1"
                if seller_url not in seller_urls: seller_urls.append(seller_url)
    return seller_urls

def get_seller_listings(seller_urls, values, listings):
    last_title = ""
    first_title = ""
    current_listing = None
    stop_page_search = False
    ignore_current = False
    done_minutes = []
    start_time = time.time()
    title = ""
    for i, seller_url in enumerate(seller_urls):
        done = i+1
        time_elapsed = time.time() - start_time
        if time_elapsed < 1: time_elapsed = 1
        rate = done / time_elapsed
        items_left = len(seller_urls) - i+1
        time_left = items_left / rate
        mins_left = int(time_left / 60)
        secs_left = int(time_left - mins_left * 60)
        if mins_left not in done_minutes:
            print("Getting Seller Listings - time remaining: " + str(mins_left) + " mins " + str(secs_left) + " secs - searching: " + seller_url.split("?")[0] + " listings: " + str(len(listings)))
            if i+1 >= 5: done_minutes.append(mins_left)
        first_title_set = False
        for page_num in range(1, 10):
            current_url = seller_url + "&_pgn=" + str(page_num)
            page = requests.get(current_url)
            page_text = page.text
            #print(page_text)
            page_split = page_text.split("\n")
            for i, line in enumerate(page_split):
                if current_listing != None and "class=\"bin" in line:
                    current_listing.buy_it_now = True
                if " class=\"vip\" title=\"" in line:
                    title = line.split("title=\"")[1].split("\">")[1].split("</a>")[0]
                  #  print(title)
                    excluded = ["played", "h/p", "l/p", "heavy", "spanish", "german", "french", "not holo", "non foil",
                                "non holo",
                                "non 1st", "not 1st", "set art", "sticker", "non-holo", "heart gold", "soul silver",
                                "base set 2", "etc", "sword", "xy", "platinum", "diamond and pearl", "empty",
                                "custom", "resealed", "ex legend", "sword and shield", "black &amp; white",
                                "shop on ebay", "korean", "portuguese", "celebrations", "anniversary", "shadowless",
                                "sun and moon",
                                "opened", "error", "sun &amp; moon", "sun & moon", "champions path",
                                "champion&amp;s path", "champion's path",
                                "fusion strike", "astral radiance", "roaring skies", "japanese"]
                    do_continue = False
                    ignore_current = False
                    for term in excluded:
                        if term in title.lower():
                            ignore_current = True
                    if not first_title_set:
                        if first_title == title: stop_page_search = True
                    url = line.split("<a href=\"")[1].split("\"")[0]
                    current_listing = Listing()
                    current_listing.title = title
                    current_listing.url = url
                    current_listing.html += line
                    if not first_title_set:
                        first_title = title
                        first_title_set = True
                if current_listing != None:
                    current_listing.html += line
                if "£" in line and "</span>" in line:
                    #print("---", line)
                    #print("---", current_listing)

                    if current_listing != None:
                        orig_title = title
                        title = ""
                        if ignore_current:
                            ignore_current = False
                            price = line.split("£")[1].split("</span>")[0]
                            price = price.replace("£", "").replace(",", "")
                 #           print(price)
                 #           print("skipping")
                            continue
                       # print(title)
                        price = line.split("£")[1].split("</span>")[0]
                        price = price.replace("£","").replace(",","")
                        if not price.replace(".","").isnumeric():
                            current_listing = None
                            continue
                        price = float(price.replace("£","").replace(",",""))
                        current_listing.price = price

                        card_info = get_card_info(current_listing.title, values, "base set", [])
                        if card_info == None: continue
                        if "booster box" in card_info.name.lower(): continue
                        grade = "ungraded"
                        if "psa 9" in orig_title.lower() or "psa9" in orig_title.lower(): grade = "psa9"
                        if "psa 10" in orig_title.lower() or "psa10" in orig_title.lower(): grade = "psa10"
                        if "?" in orig_title: grade = "ungraded"
                        if card_info == None: continue
                        value = None
                        if grade == "ungraded":
                            value = card_info.ungraded
                            if value == None: continue
                        if grade == "psa9":
                            value = card_info.psa9
                            if value == None:
                                if card_info.ungraded != None: value = card_info.ungraded
                            if value == None: continue
                        if grade == "psa10":
                            value = card_info.psa10
                            if value == None:
                                if card_info.psa9 != None: value = card_info.psa9
                                elif card_info.ungraded != None: value = card_info.ungraded
                            if value == None: continue
                        increase = price - value
                        current_listing.grade = grade
                        current_listing.name = card_info.name
                        current_listing.value = value
                        current_listing.difference = (increase / value) * 100
                        current_listing.raw_difference = price - value
                        current_listing.buy_it_now = True
                        current_listing.how_found = "seller page"
                        if current_listing not in listings: listings.append(current_listing)
                       # print(current_listing.title, current_listing.price, current_listing.url, current_listing.value, current_listing.name)
                if "bid" in line.lower() and current_listing != None:
                    listings[len(listings) - 1].buy_it_now = False
                    current_listing.buy_it_now = False
                    current_listing = None
            first_title_set = False
            if stop_page_search:
                stop_page_search = False
                break
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
    no_matches = []
    all_listings = get_listings(search_terms, all_values, buy_it_now, False, no_matches)
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