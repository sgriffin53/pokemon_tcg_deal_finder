from main import get_card_info
from main import Value
from main import myFunc
from main import get_all_values
from main import get_listings
from main import get_seller_urls, get_seller_listings
from constantrun import send_email
from collection_value import card_owned
import time
import os

ff = open('missing.txt','r',encoding='utf-8')
lines = ff.readlines()
ff.close()

missing_cards = []
search_terms = []

for line in lines:
    line = line.replace("\n","").strip()
    missing_cards.append(line)
    search_terms.append("pokemon " + line)

buy_it_now = True
i = 0
while True:
    start_time = time.time()
    i += 1
    if i % 2 == 0:
        print("Buy it now")
        buy_it_now = True
    else:
        print("Auction")
        buy_it_now = False
    set_urls = ["https://www.pricecharting.com/console/pokemon-base-set?sort=highest-price",
               "https://www.pricecharting.com/console/pokemon-jungle?sort=highest-price",
                "https://www.pricecharting.com/console/pokemon-fossil?sort=highest-price"]
    # set_urls = ["https://www.pricecharting.com/console/pokemon-neo-genesis?sort=highest-price"]
    wanted_values = []
    all_values = []
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
        if "1st edition" in name.lower() and "machamp" not in name.lower(): continue
        if "gold border" in name.lower(): continue
        if "no symbol" in name.lower() or "w stamp" in name.lower() or "prerelease" in name.lower(): continue
        if "cosmos" in name.lower() or "shadowless" in name.lower() or "trainer deck" in name.lower() or "black flame" in name.lower() \
                or "error" in name.lower() or "e3" in name.lower() or "poketour" in name.lower(): continue
        if card_owned(value, missing_cards): wanted_values.append(value)
        pass
    all_values = wanted_values
    no_matches = []
    all_listings = get_listings(search_terms, all_values, buy_it_now, True, no_matches)
    all_listings.sort(key=myFunc)
    listing_urls = []
    for listing in all_listings:
        listing_urls.append(listing.url)
    seller_urls = get_seller_urls(listing_urls)
    seller_listings = get_seller_listings(seller_urls, all_values, list(all_listings))
    all_listings = []
    for listing in seller_listings:
        all_listings.append(listing)
    all_listings.sort(key=myFunc)
    listing_urls = []
    for listing in all_listings:
        listing_urls.append(listing.url)
    new_deal_count = 0
    for listing in all_listings:
        listing.url = listing.url.split("?")[0]
        if listing.raw_difference >= 15: continue
        ff = open('done_deals.txt','r',encoding='utf-8')
        readlines = ff.readlines()
        already_exists = False
        for line in readlines:
            line = line.replace("\n","").strip()
            if listing.url == line:
                already_exists = True
        ff.close()
        if already_exists: continue
        new_deal_count += 1
        ff = open('new_deals.txt','a',encoding='utf-8')
        ff.write("title: " + listing.title + "\n")
        ff.write("name: " + listing.name + "\n")
        ff.write("url: " + listing.url + "\n")
        ff.write("grade: " + listing.grade + "\n")
        ff.write("price: £" + str(listing.price) + "\n")
        ff.write("value: £" + str(listing.value) + "\n")
        ff.write("difference: " + str(round(listing.difference,2)) + "\n")
        ff.write("raw difference: £" + str(round(listing.raw_difference,2)) + "\n")
        if listing.buy_it_now == None:
            bin_str = "Buy it Now"
            if buy_it_now == True: bin_str = "Buy it now"
            elif buy_it_now == False: bin_str = "Auction"
        else:
            bin_str = "Buy it Now"
            if not listing.buy_it_now: bin_str = "Auction"
        bin_str += " (" + str(listing.how_found) + ")"
        ff.write("listing type: " + bin_str + "\n")
        ff.write("-----" + "\n")
        ff.close()
        ff = open('done_deals.txt','a', encoding='utf-8')
        ff.write(listing.url + "\n")
        ff.close()
        fff = open('out_html.html','a',encoding='utf-8')
        fff.write(listing.html + "\n")
        fff.close()

    print(str(len(all_listings)) + " total listings")
    print(str(new_deal_count) + " new deals")
    ff = open('new_deals.txt', 'r', encoding='utf-8')
    readlines = ff.readlines()
    ff.close()
    tot_new_deals = int(len(readlines) / 10)
    print(str(tot_new_deals) + " unseen deals")
    if (new_deal_count >= 1):
        if tot_new_deals >= 3:
            message = "New deals\n<br><br>"
            for line in readlines:
                message += line + "<br>"
            print("\a")
            time.sleep(0.6)
            os.system("Powershell -Command \"Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('found " + str(tot_new_deals) + " new deals');\"")
            subject = "⚡ Found " + str(tot_new_deals) + " new deals (missing from sets)! ⚡"
            send_email(subject,message)
            print("Sent email")
            os.system("del new_deals.txt")
            ff = open('new_deals.txt','w',encoding='utf-8')
            ff.write(" ")
            ff.close()
    time_elapsed = time.time() - start_time
    time_elapsed_mins = round(time_elapsed / 60,2)
    print("finished in " + str(time_elapsed_mins))
    if i % 2 == 0:
        print("sleeping")
        time.sleep(60*10)