Python script for finding good deals on pokemon cards on ebay.

It checks pricecharting.com for the values of the top 50 most expensive base, jungle, and fossil cards, then searches for those cards on eBay. It outputs to a file out.txt
with the listings that matched known cards, with details such as price, grading, price difference (raw and percentage), etc. The output is ordered by the raw difference between
price and value in the listing, so the best deals will be at the top.

~~
It's very miss on how accurately it identifies cards. It might mistake a Lapras booster pack for a Lapras card and give a wrong valuation, or it might mistake a Dark Charizard
for a normal Charizard, etc. Right now it probably has slightly more misses than hits when it comes to card identification.
Despite the inaccuracy in identification, it can still find some good deals, it just requires manually checking the output to find the matching cards with good prices.
~~
EDIT: This is no longer accuarte, the card identifier is a lot more accurate now and rarely makes mistakes.

To run:

run "python main.py"
Three files will be created, out.txt, out_old.txt, fresh.txt.

out.txt is the output with the list of listings.
fresh.txt is the output from out.txt but any entries that existed in the out.txt before the script was run won't be included. So, this file will have the new listings
that have appeared since the script was last run.

Other files:

constantrun.py 
This is an email notification script that runs constantly and emails on new deals. To use this, you need an account with sendinblue and an API key. Add your API key and email details at the top of the file.

get_value.py
This is a script that can get the value of the open ebay page in the browser. If you hook this up to a shortcut with AutoHotKey, you can use the shortcut when browsing ebay to find the value of the card. It takes a few seconds to get the value.

collection_value.py
This is a script to assess the value of your collection. Place your collection in the file collection.txt with each card on a separate line. For example:

base Charizard #4
fossil Ditto #3
jungle Snorlax #11

The important thing is that you have the number with a # preceding it and the set name, so "base #4" will register as a base charizard, but "base charizard" won't.
This shows how complete your base, jungle, and fossil sets are and also outputs a text file which shows which cards are missing from base, jungle, and fossil sets to missing.txt.

get_missing.py

Finds listings for the cards missing from your base, jungle, and fossil collection (based on the list in missing.txt), sends an email with new deals to the email API details configured in constantrun.py.
