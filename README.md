Python script for finding good deals on pokemon cards on ebay.

It checks pricecharting.com for the values of the top 50 most expensive base, jungle, and fossil cards, then searches for those cards on eBay. It outputs to a file out.txt
with the listings that matched known cards, with details such as price, grading, price difference (raw and percentage), etc. The output is ordered by the raw difference between
price and value in the listing, so the best deals will be at the top.

It's very miss on how accurately it identifies cards. It might mistake a Lapras booster pack for a Lapras card and give a wrong valuation, or it might mistake a Dark Charizard
for a normal Charizard, etc. Right now it probably has slightly more misses than hits when it comes to card identification.

Despite the inaccuracy in identification, it can still find some good deals, it just requires manually checking the output to find the matching cards with good prices.

To run:

run "python main.py"
Three files will be created, out.txt, out_old.txt, fresh.txt.

out.txt is the output with the list of listings.
fresh.txt is the output from out.txt but any entries that existed in the out.txt before the script was run won't be included. So, this file will have the new listings
that have appeared since the script was last run.

