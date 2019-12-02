"""The script was written to find current information on certain items in XML documents by provided URL"""

import requests as req  # Request is used for data collection. XML document link should be used
import xml.etree.ElementTree as ET  # XML document gets loaded and then parsed by ET
import bs4  # To perform HTML parsing BS4 is used
import tempfile as tmp  # To store XML feed, while working on it( string io could be used as well )


def pull_all_url_out():
    """
    Pulls out all url found in feed. Url should have tag {http://www.zbozi.cz/ns/offer/1.0}URL
    Return value : list() with each element - url string
    """
    with tmp.TemporaryFile(mode='w+', encoding='utf-8', suffix='xml', ) as temp_file:
        # First - save feed to file(get feed)
        temp_file.write(req.get(
            'http://www.fit-pro.cz/export/fi......').text)
        # Then prepare place for found url's
        found_urls = []
        # As file was written - pointer is in the end of it., Now take it back
        temp_file.seek(0)
        for event, elem in ET.iterparse(temp_file):
            # Every element with this tag contains url of item, which we are looking for
            if elem.tag == '{http://www.zbozi.cz/ns/offer/1.0}URL':
                found_urls.append(elem.text)
    return found_urls


def get_page_info(url, analysis=0):
    """
    Performs parsing of items web page by its url, looking for category of item(-category) and availability(-stoke)
    Return value : dict() with keys:
        -category
        -stoke
    """
    # Prepare template of return
    item_disc = {'category': '-', 'stoke': 0}
    # Perform standard routine for HTML parsing
    soup = bs4.BeautifulSoup(req.get(url).text, 'html.parser')
    # First - pull out the category
    # Category is represented by tag <li class= "breadcrumb__item"> CAT <a></a></...>
    # However, product page tag <strong> instead of <a>
    tags_with_cat = soup.find_all('li', class_="breadcrumb__item")
    if tags_with_cat:
        # Stores category of item
        category = ''
        for tag in tags_with_cat:
            if tag.a:
                category += tag.a.string + ' > '
            elif tag.strong:
                category += tag.string
            else:
                break
        item_disc['category'] = category
    # Second - lets look at the  availability
    tag_with_stoke = soup.find('div', class_="order-box__ship availability availability--1")
    # Availability is represented by tag <div class= "order-box__ship availability availability--1"> AVL </...>
    # Amount of item is given with format : .... whitespace </> whitespace NUM ks ., the last element is XXXks
    if analysis:
        if tag_with_stoke:
            return tag_with_stoke.string
        else:
            return ''

    if tag_with_stoke:
        # Stores availability
        stoke = ''
        mid_stoke = tag_with_stoke.string
        # Pullout numbers as text ---> make integer
        for i in mid_stoke:
            if i.isdecimal():
                stoke += i
        if stoke:
            item_disc['stoke'] = int(stoke)
    # Finally - return filled dictionary
    return item_disc


def get_all_uniq_masks(source_list):
    """
    Function creates set of unique masks for list/set of lines., ex.: 'qwerty12>45tr' ---> 'LNSNL'
    (for analyse purposes)
    The Letter will be represented with L, Number with N and Symbol with S
    """
    # Set appropriate symbols to use
    letter = 'L'
    number = 'N'
    sign = 'S'
    uniq_masks = set()
    for source_str in source_list:
        mask = ''  # Middle mask
        last = ''  # Type of last symbol found
        for symb in source_str:
            # Control for numbers
            if symb.isnumeric():
                if last != number:
                    mask += number
                    last = number
                else:
                    continue
            # Control for letters
            elif symb.isalpha():
                if last != letter:
                    mask += letter
                    last = letter
                else:
                    continue
            # Else - it is sign
            else:
                if last != sign:
                    mask += sign
                    last = sign
                else:
                    continue
        # As  mask is created - it should be unique - that's why sets are used
        uniq_masks.add(mask)
    return uniq_masks


if __name__ == '__main__':
    # ------ analysis
    # possible_strings = []  # should be list(), not set()., due to compare time
    # try:
    #     for url in pull_all_url_out():
    #         mid_str = get_page_info(url, analysis=1)
    #         if mid_str:
    #             possible_strings.append(mid_str)
    # except req.exceptions.ConnectionError:
    #     print("\n\n\n\n_____CONNECTION ERROR____\n\n\n\n")
    # with open('result_u_mask.txt', 'a') as f:
    #     for m in get_all_uniq_masks(possible_strings):
    #         f.write(m + '\n')

    # # ------ general performance
    # for url in pull_all_url_out():
    #     print(get_page_info(url))

    pass
