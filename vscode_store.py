#!/usr/bin/env python3

import json
import re

PRODUCT_CONFIG_FILE_PATH = "/usr/lib/code/product.json"
#PRODUCT_CONFIG_FILE_PATH = "./product.json"

CONFIG_STORE_OPENVSX = dict([
    ('serviceUrl',  "https://open-vsx.org/vscode/gallery"),
    ('itemUrl',     "https://open-vsx.org/vscode/item"),
    ('cacheUrl',    False),
    ('storeName',   'open-vsx.org')
])

CONFIG_STORE_VISUALSTUDIOCOM = dict([
    ('serviceUrl',  "https://marketplace.visualstudio.com/_apis/public/gallery"),
    ('itemUrl',     "https://marketplace.visualstudio.com/items"),
    ('cacheUrl',    "https://vscode.blob.core.windows.net/gallery/index"),
    ('storeName',   'marketplace.visualstudio.com')
])



def readDeserializedProductConfig():
    with open(PRODUCT_CONFIG_FILE_PATH, 'r') as product_config_file_open:
        product_config_deserialized = json.load(product_config_file_open)
        return product_config_deserialized

def writeSerializedProductConfig(json_data_serialized_to_write):
    with open(PRODUCT_CONFIG_FILE_PATH, 'w') as product_config_file_write:
        json.dump(
            json_data_serialized_to_write,
            product_config_file_write,
            indent="\t"
        )

def returnDomaineNameFromURL(urlToRegex):
    match = re.search('https?://([A-Za-z_0-9.-]+).*', urlToRegex)
    if match:
        return match.group(1)
    else:
        return False

def getStoreName(jsonSerializeConfig):
    return returnDomaineNameFromURL(getServiceUrl(jsonSerializeConfig))

def getServiceUrl(jsonSerializeConfig):
    return jsonSerializeConfig["extensionsGallery"]["serviceUrl"]

def setServiceUrl(jsonSerializeConfig, value):
    jsonSerializeConfig["extensionsGallery"]["serviceUrl"] = value
    return jsonSerializeConfig

def getItemUrl(jsonSerializeConfig):
    return jsonSerializeConfig["extensionsGallery"]["itemUrl"]

def setItemUrl(jsonSerializeConfig, value):
    jsonSerializeConfig["extensionsGallery"]["itemUrl"] = value
    return jsonSerializeConfig

def getCacheUrl(jsonSerializeConfig):
    if ("cacheUrl" in jsonSerializeConfig["extensionsGallery"]):
        return jsonSerializeConfig["extensionsGallery"]["cacheUrl"]
    else:
        return False

def setCacheUrl(jsonSerializeConfig, value):
    if (value):
        jsonSerializeConfig["extensionsGallery"]["cacheUrl"] = value
    else:
        del jsonSerializeConfig["extensionsGallery"]["cacheUrl"]
    return jsonSerializeConfig



def getStoreConfig():
    product_config_json_deserialized = readDeserializedProductConfig()

    return_config = dict([
        ("serviceUrl", False),
        ("itemUrl", False),
        ("cacheUrl", False),
        ("storeName", False)
    ])

    return_config['serviceUrl'] = getServiceUrl(product_config_json_deserialized)
    return_config['itemUrl']    = getItemUrl(product_config_json_deserialized)
    return_config['cacheUrl']   = getCacheUrl(product_config_json_deserialized)
    return_config['storeName']  = getStoreName(product_config_json_deserialized)

    return return_config

def setStoreConfig(service_url, item_url, cache_url):
    product_config_json_deserialized = readDeserializedProductConfig()

    setServiceUrl(product_config_json_deserialized, service_url)
    setItemUrl(product_config_json_deserialized, item_url)
    setCacheUrl(product_config_json_deserialized, cache_url)

    with open(PRODUCT_CONFIG_FILE_PATH, 'w') as product_config_file_write:
        json.dump(
            product_config_json_deserialized,
            product_config_file_write,
            indent = "\t"
        )

def printStoreConfig():
    config_to_show = getStoreConfig()

    if (not config_to_show['cacheUrl']):
        config_to_show['cacheUrl'] = "empty"

    print("""Current store is configure for {storeName}
serviceUrl: {serviceUrl}
itemUrl:    {itemUrl}
cacheUrl:   {cacheUrl}""".format(
        serviceUrl = config_to_show['serviceUrl'],
        itemUrl = config_to_show['itemUrl'],
        cacheUrl = config_to_show['cacheUrl'],
        storeName = config_to_show['storeName']
        )
    )

def setStoreVisualStudioCom():
    setStoreConfig(
        CONFIG_STORE_VISUALSTUDIOCOM['serviceUrl'],
        CONFIG_STORE_VISUALSTUDIOCOM['itemUrl'],
        CONFIG_STORE_VISUALSTUDIOCOM['cacheUrl']
    )

def setStoreOpenVSX():
    setStoreConfig(
        CONFIG_STORE_OPENVSX['serviceUrl'],
        CONFIG_STORE_OPENVSX['itemUrl'],
        CONFIG_STORE_OPENVSX['cacheUrl']
    )

setStoreVisualStudioCom()
printStoreConfig()
