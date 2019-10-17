#! /usr/bin/env python3
#! c:/Python/ python

"""
AUTHOR:  KBeDeveloper (https://github.com/KBeDeveloper), (https://gitlab.com/KBeDeveloper)
DATE:    October 7, 2019
LICENSE: MIT
"""

import sys
import re
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

req_url = str((sys.argv)[1])

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
# req_url = "https://www.amazon.com/CeraVe-Moisturizing-Cream-Daily-Moisturizer/dp/B00TTD9BRC?pf_rd_p=db3cdb4c-2bd3-40c9-9dc4-3184fe00fa20&pf_rd_r=4Y8JEMQZY6RVTMS5VM95"
# req_url = "https://www.amazon.com/dp/B01MSZSL4I/ref=twister_B07FBDGKDT?_encoding=UTF8&psc=1"
req_url = 'https://www.amazon.com/dp/B07K58ZHTR/ref=dp_cerb_1'
req = Request(url=req_url, headers=headers)
html = urlopen(req)
soup = BeautifulSoup(html.read(), 'html5lib')

# GET DESC
desc = soup.find(id='productTitle')
desc = desc.text
desc = (re.sub('\n','',desc)).strip()

# GET PRICE
try:
    price = soup.find(id='priceblock_ourprice')
    price = (price.text).strip().replace("\n","").replace("$","")
    error = False
except:
    error = True

# GET DIMS
try:
    try:
        dim_type = 0
        dims = soup.find_all('td', class_="bucket")[0].find(class_="content").find_all('ul')[0].find_all('li')[0]
        dims = (dims.text).strip()
        dims = re.sub('Product Dimensions:', '', dims)
        dims_pre = dims
        dims = re.sub('inches','@inches#', dims)
        if dims == dims_pre:
            dims = re.sub('centimeters','@centimeters', dims)
        slice_index_1 = dims.index('@')
        slice_index_2 = dims.index('#')
        dim_aux = dims
        dims = dims[:slice_index_1].strip()
        slice_index_1 = slice_index_1 + 1
        dim_unit = dim_aux[slice_index_1:slice_index_2].strip().upper()
        error = False
    except:
        dim_type = 1
        dims = soup.find_all('table', id="productDetails_detailBullets_sections1")[0].find('tbody').find_all('tr')[0].find('td', class_="a-size-base")
        dims = dims.text
        dims = dims.strip()
        dims_pre = dims
        dims = re.sub('inches','@inches',dims)
        if dims == dims_pre:
            dims = re.sub('centimeters','@centimeters', dims)
        slice_index = dims.index('@')
        dim_aux = dims
        dims = dims[:slice_index].strip()
        dim_unit = (dim_aux[slice_index:].upper()).replace("@","")
        error = False
except:
    dim_type = -1
    error = True

# GET WEIGHT
if dim_type is 0:

    weight = dim_aux
    slice_index_1 = (weight.index(';'))+1
    weight = weight[slice_index_1:].strip()
    weight_pre = weight
    weight = weight.replace("pounds","@pounds").strip()
    if weight == weight_pre:
        weight = weight.replace("ounces","@ounces").strip()
    slice_index_2 = weight.index('@')
    weight_aux = weight
    weight = weight[:slice_index_2].strip()
    slice_index_2 = slice_index_2 + 1
    weight_unit = weight_aux[slice_index_2:].strip().upper()
    error = False

elif dim_type is 1:
    
    weight = soup.find_all('table', id="productDetails_detailBullets_sections1")[0].find('tbody').find_all('tr')[2].find('td', class_="a-size-base")
    weight = (weight.text).strip()
    slice_index_1 = weight.index("(")
    weight_pre = weight = weight[:slice_index_1].strip()
    weight = weight.replace("pounds","@pounds").strip()
    if weight == weight_pre:
        weight = weight.replace("ounces","@ounces").strip()
    slice_index_2 = weight.index('@')
    weight_aux = weight
    weight = weight[:slice_index_2].strip()
    slice_index_2 = slice_index_2 + 1
    weight_unit = weight_aux[slice_index_2:].strip().upper()
    error = False

else:
    error = True

# HANDLING RESULT
if error is not None:
    if error is True:
        product = {
            "hasErrors" : True,
            "Error" : "Could not retrieve product data."
        }
    else:
        product = {
            "DESC" : desc,
            "PRICE" : price,
            "DIMS" : dims,
            "DIMS_UNIT" : dim_unit,
            "WEIGHT" : weight,
            "WEIGHT_UNIT" : weight_unit
        }
else:
    product = {
        "hasErrors" : True,
        "Error" : "Internal error"
    }

print(product)
