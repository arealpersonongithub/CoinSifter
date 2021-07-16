# -*- coding: utf-8 -*-
import requests
import traceback
import time
import json
import sys
import random
import subprocess

i = 0

def main():
	databank="mainbank.txt" # private key / pubkey / pubkey truncated triplets land here
	tempfile="temp.txt" # the home of data processing hell
	siftbank="sifted.txt" # balances go here
	url = "https://blockchain.info/balance?active=" # API
	# filterwords = "'n_tx': 0,", "'total_received': 0}", "'total_received': 0}}", # unnecessary strings to filter out of siftbank
	filterwords = "'final_balance': 0,", "'n_tx': 0,", "'total_received': 0}", "'total_received': 0}}", # unnecessary strings to filter out of siftbank
	pubkey_list = " "

	seed = random.randrange(1, 90462569716653277674664832038037428010029347093027269048910283704) # page for key generator. important to reinitialize this

	process = subprocess.Popen(['keys-generator', 'btc', str(seed)], stdout=subprocess.PIPE)
	data = str(process.communicate()).replace('\\n', '\n').replace('\\t', '\t').replace('(b\'', '').replace('\', None)', '').replace('{', '').replace('}', '') # welcome to edge case hell

	output = open(databank, 'a')
	output.write(data)
	output.close()

	output = open(tempfile, 'w')
	output.write(data)
	output.close()

	data = open(tempfile, "r") # welcome to hell, in general. i cannot tell you why this is necessary.

	for line in data:
		line = line.split(" ")
		pubkey_list = pubkey_list + line[1].strip()+"|"
	data.close()

	pubkey_list = pubkey_list[1:-1]

# print("Keylist: " + str(pubkey_list))

	new_url = url+str(pubkey_list)
#print (new_url)
	
	json_text = requests.get(new_url, headers={'User-Agent': "X11; Ubuntu; Linux x86_64; rv:89.0) CoinSifter/0.1"})
	json_data = json_text.json()
	output = open(tempfile, 'w')
	output.write(str(json_data).replace(', \'', ',\n\''))
	output.close()

	with open(tempfile) as oldfile, open(siftbank, 'a') as newfile:
		for line in oldfile:
			if not any(filterword in line for filterword in filterwords):
				newfile.write(line)

	time.sleep(1) # prevents excessive API abuse

while True:
	main()
	i = i + 1
	print ("Sifted " + str(i) + " time(s).")


