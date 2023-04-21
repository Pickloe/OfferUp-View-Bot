import cloudscraper
import re

def get_item_info(offerup_url):
    """
    Sends a GET request to the OfferUp URL and extracts the item_id, listing_id, and seller_id from the response using regex.
    Returns a tuple containing the extracted values, or None if any of the values could not be extracted.
    """
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url=offerup_url)
    if response.status_code != 200:
        print(f"{response.status_code} - Failed to access the page")
        return None
    
    item_id = re.search(r'content="ouapp:\/\/\/item\/detail\/(\d+)"', response.text)
    listing_id = re.search(r'"listingId":"(.*?)"', response.text)
    seller_id = re.search(r',"ownerId":"(\d+)"', response.text)
    
    if not item_id or not listing_id or not seller_id:
        print("Failed to extract item information")
        return None
    
    return (item_id.group(1), listing_id.group(1), seller_id.group(1))

def send_viewed_request(item_id, listing_id, seller_id):
    """
    Sends a POST request to the OfferUp API with the item information to register a view.
    Returns True if the request was successful, False otherwise.
    """
    viewed_request_data = {
        "operationName": "TrackItemViewed",
        "variables": {
            "itemId": item_id,
            "listingId": listing_id,
            "sellerId": seller_id,
            "header": {
                "appVersion": "",
                "deviceId": "None",
                "origin": "web_desktop",
                "timestamp": "None",
                "uniqueId": "None"
            },
            "mobileHeader": {
                "localTimestamp": "None"
            },
            "shipping": {
                "available": False
            },
            "posting": {
                "itemTitle": "None",
                "itemPrice": 123,
                "itemCondition": 100,
                "itemLocation": {
                    "latitude": 12.3456789,
                    "longitude": -123.4567890
                },
                "postingTimestamp": "None"
            },
            "vehicle": {
                "make": None,
                "mileage": None,
                "model": None,
                "year": None
            },
            "tileLocation": None,
            "categoryId": "14",
            "sellerType": "PRIVATE_PARTY",
            "moduleRank": None
        },
        "query": "mutation TrackItemViewed($itemId: ID!, $listingId: ID!, $sellerId: ID!, $header: ItemViewedEventHeader!, $mobileHeader: ItemViewedEventMobileHeader!, $origin: String, $source: String, $tileType: String, $userId: String, $moduleId: ID, $shipping: ShippingInput, $vehicle: VehicleInput, $posting: PostingInput, $tileLocation: Int, $categoryId: String, $moduleType: String, $sellerType: SellerType, $moduleRank: Int) {\n  itemViewed(\n    data: {itemId: $itemId, listingId: $listingId, sellerId: $sellerId, origin: $origin, source: $source, tileType: $tileType, userId: $userId, header: $header, mobileHeader: $mobileHeader, moduleId: $moduleId, shipping: $shipping, vehicle: $vehicle, posting: $posting, tileLocation: $tileLocation, categoryId: $categoryId, moduleType: $moduleType, sellerType: $sellerType, moduleRank: $moduleRank}\n  )\n}\n"
    }

    scraper = cloudscraper.create_scraper()
    response = scraper.post(url="https://offerup.com/api/graphql", json=viewed_request_data)
    response_json = response.json()
    
    if response_json and response_json.get('data') and response_json['data'].get('itemViewed'):
        print("Successfully sent a view!")
        return True
    else:
        print("Failed to send a view.")
        print(response_json['errors'])
        return False

if __name__ == '__main__':
    offerup_url = input("OfferUp URL: ")
    item_info = get_item_info(offerup_url)
    if item_info:
        item_id, listing_id, seller_id = item_info
        send_viewed_request(item_id, listing_id, seller_id)