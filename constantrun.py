from __future__ import print_function
from main import get_values
from main import get_listings
from main import myFunc
import os, sys
import time

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint

def send_email(subject, message):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = 'api-key'
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    subject = subject
    html_content = message
    sender = {"name":"name","email":"name"}
    to = [{"email":"name@gmail.com","name":"name"}]
    #cc = [{"email":"example2@example2.com","name":"Janice Doe"}]
    cc = None
    #bcc = [{"name":"John Doe","email":"example@example.com"}]
    bcc = None
    reply_to = {"email":"name","name":"name"}
    #headers = {"Some-Custom-Name":"unique-id-1234"}
    params = None
    headers = None
    #params = {"parameter": None,"subject":"New Subject"}
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, bcc=bcc, cc=cc, reply_to=reply_to, headers=headers, html_content=html_content, sender=sender, subject=subject)

    try:
        # Send a transactional email
        api_response = api_instance.send_transac_email(send_smtp_email)
        pprint(api_response)
    except ApiException as e:
        pass
        #print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)

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

    no_matches = []
    os.system("del out_old.txt")
    os.system("copy out.txt out_old.txt")
    set_urls = ["https://www.pricecharting.com/console/pokemon-base-set?sort=highest-price"]
             #  "https://www.pricecharting.com/console/pokemon-jungle?sort=highest-price",
             #   "https://www.pricecharting.com/console/pokemon-fossil?sort=highest-price",
             #   "https://www.pricecharting.com/console/pokemon-team-rocket?sort=highest-price",
             #   "https://www.pricecharting.com/console/pokemon-gym-heroes?sort=highest-price",
             #   "https://www.pricecharting.com/console/pokemon-neo-genesis?sort=highest-price",
             #   "https://www.pricecharting.com/console/pokemon-gym-challenge?sort=highest-price",
             #   "https://www.pricecharting.com/console/pokemon-neo-discovery?sort=highest-price",
             #   "https://www.pricecharting.com/console/pokemon-neo-revelation?sort=highest-price",
             #   "https://www.pricecharting.com/console/pokemon-neo-destiny?sort=highest-price"]
    # set_urls = ["https://www.pricecharting.com/console/pokemon-neo-genesis?sort=highest-price"]
    all_values = []
    for set_url in set_urls:
        values = get_values(set_url)
        for value in values:
            all_values.append(value)
        #print(set_url, len(values))
    search_terms = []
    pokemon_names = []
    ff = open('pokemon_names.txt','r',encoding='utf-8')
    lines = ff.readlines()
    for pokemon in lines:
        pokemon = pokemon.replace("\n","")
        pokemon_names.append(pokemon)
    ff.close()
    values_pokemon_names = []
    for value in all_values:
        name = value.name.replace("[", "").replace("]", "").replace("#", "")
        name = name.replace("&39;", "'")
        for pokemon in pokemon_names:
            if pokemon.lower() in name.lower() and pokemon.lower() not in values_pokemon_names:
                values_pokemon_names.append(pokemon)
        #print(name)
        #continue
        #print(name)
        search_terms.append("pokemon " + name)
    #for pokemon in values_pokemon_names:
    #    search_terms.append("pokémon " + pokemon + " card")
   # search_terms.append("pokemon trainer card")
   # search_terms.append("pokemon energy card")
   # search_terms.append("pokemon psa 10")
   # search_terms.append("pokemon psa 9")
   # search_terms.append("pokemon rare holo")
   # search_terms.append("pokemon rare holo psa")
   # search_terms.append("pokemon base")
   # search_terms.append("pokemon jungle")
   # search_terms.append("pokemon fossil")
   # search_terms.append("pokemon team rocket")
   # search_terms.append("pokemon gym heroes")
   # search_terms.append("pokemon neo discovery")
   # search_terms.append("pokemon neo genesis")
   # search_terms.append("pokemon neo revelation")
    new_search_terms = []
    for term in search_terms:
        new_term = ""
        for word in term.split(" "):
            if word.isnumeric(): continue
            new_term += word + " "
        new_term = new_term.strip()
        new_search_terms.append(new_term)
   # search_terms = new_search_terms
    print(str(len(search_terms)) + " search terms")
    all_listings = get_listings(search_terms, all_values, buy_it_now, True, no_matches)
    all_listings.sort(key=myFunc)
    listing_urls = []
    for listing in all_listings:
        listing_urls.append(listing.url)
    new_deal_count = 0
    for listing in all_listings:
        listing.url = listing.url.split("?")[0]
        if listing.raw_difference >= -15: continue
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
        bin_str = "Buy it Now"
        if not buy_it_now: bin_str = "Auction"
        ff.write("listing type: " + bin_str + "\n")
        ff.write("-----" + "\n")
        ff.close()
        ff = open('done_deals.txt','a', encoding='utf-8')
        ff.write(listing.url + "\n")
        ff.close()
    #fg = open('no_matches.txt','a',encoding='utf-8')
    #for title in no_matches:
    #    fg.write(title + "\n")
    #print("wrote " + str(len(no_matches)) + " no matches")
    #fg.close()
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
            subject = "⚡ Found " + str(tot_new_deals) + " new deals! ⚡"
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
