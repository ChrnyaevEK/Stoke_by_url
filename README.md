# Stoke_by_URL

 The script was written to find current information on certain items in XML documents by provided URL

* Author : __Cherniaev Egor__, 	  for Brani s.r.o.

## Usage
* To perform dictionary creation on single link - provide function `get_page_info` this link.

* If you want to pull out those links firsft - provide `pull_all_url_out` source link(task XML  link). Then you may just uncomment check code down below - result will be printed.

* Perform analysis - uncomment code for this. `get_all_uniq_masks` is responsible for mask creation. Pass a list/set of strings to it, to get a set of masks. In output MASKS ARE UNIQUE
