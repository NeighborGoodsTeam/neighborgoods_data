# Python 3 program to calculate Distance Between Two Points on Earth
# https://www.geeksforgeeks.org/program-distance-two-points-earth/
from math import radians, cos, sin, asin, sqrt
def distance(lat1, lon1, lat2, lon2):
    """
    Calculates the distance in miles between two geo coordinates. Adapted from code from https://www.geeksforgeeks.org/program-distance-two-points-earth/
    
    Input: 
        lat1 (double) : latitude of location 1
        lon1 (double) : longitude of location 1
        lat2 (double) : latitude of location 2
        lon2 (double) : longitude of location 2
    
    Output:
        distance (double) : distance between locations in miles
    """
      
    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
       
    # Haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
  
    c = 2 * asin(sqrt(a)) 
     
    # Radius of earth in kilometers. Use 3956 for miles
    r = 3956
       
    # calculate the result
    return(c * r)

from googlemaps import Client
def coordinates_by_address(key, address):
    """
    Uses Google Maps API to generate geo coordinates based on a given address. 
    
    Input:
        key (str) : Google Maps API key (generate one at https://developers.google.com/maps/documentation/javascript/get-api-key)
        address (str) : address or place name
        
    Output:
        coordinates (double, double) : latitude and longitude of location
    """
    api = Client(key)
    search = api.geocode(address)
    coordinates = search[0]['geometry']['location']
    return (coordinates['lat'], coordinates['lng'])

def entry_from_google(google_result, id_num=None):
    """
    Takes a Google Maps API places result and creates a NeighborGoods business entry
    
    Input:
        google_result (dict) : dict/json of business from places API search
        id_num (int, str) : identification value, taken from google result if not specified
        
    Output:
        result (dict) : NeighborGoods business entry
    """
    result = {}
    
    if id_num == None:
        result.update({'id' : google_result['place_id']})
    else:
        result.update({'id' : id_num})
        
    result.update({'name' : google_result['name']})
    result.update({'categories' : [i for i in google_result['types']]})
    
    address_split = google_result['formatted_address'].split(',')
    if len(address_split) == 4:
        result.update({'address1' : str.strip(address_split[0])})
        result.update({'address2' : None})
        result.update({'city' : str.strip(address_split[1])})
        state_zip = address_split[2].split(' ')
        result.update({'state' : state_zip[1]})
        result.update({'zip_code' : state_zip[2]})
    elif len(address_split) > 4:
        result.update({'address1' : str.strip(address_split[0])})
        result.update({'address2' : str.strip(address_split[1])})
        result.update({'city' : str.strip(address_split[2])})
        state_zip = address_split[3].split(' ')
        result.update({'state' : state_zip[1]})
        result.update({'zip_code' : state_zip[2]})
    
    result.update({'latitude' : google_result['geometry']['location']['lat']})
    result.update({'longitude' : google_result['geometry']['location']['lng']})
    
    result.update({'phone' : None})
    result.update({'url' : None})
    result.update({'email' : None})
    result.update({'hours' : None})
    result.update({'description' : None})
    result.update({'owner' : None})
    
    result.update({'products' : []})
    
    return result

def sam_search(key, args):
    """
    Searches SAM API with given arguments.
    
    Input:
        key (str) : SAM API key (generate at https://gsa.github.io/sam_api/sam/key)
        args (dict) : set of argument names and values. Find possible arguments at https://gsa.github.io/sam_api/sam/searchfields.html
    """
    # args is dictionary {parameter : value}
    base = 'https://api.data.gov/sam/v3/registrations?qterms='
    if len(args) == 1:
        url = base + str(list(args.keys())[0]) + ':' + str(list(args.values())[0])
    elif len(args) > 1:
        url = base
        for i in range(len(args)):
            if i > 0:
                url += '+AND+'
            url += '(' + str(list(args.keys())[i]) + ':' + str(list(args.values())[i]) + ')' 
    url += '&api_key=' + key
    
    res = requests.get(url)
    return res.json()

def entry_by_yelp(yelp, id_num=None):
    """
    Takes a Yelp API result and creates a NeighborGoods business entry
    
    Input:
        yelp (dict) : dict/json of business from yelp API search
        id_num (int, str) : identification value, taken from yelp result if not specified
        
    Output:
        result (dict) : NeighborGoods business entry
    """
    result = {}
    
    if id_num == None:
        result.update({'id' : yelp['id']})
    else:
        result.update({'id' : id_num})
        
    result.update({'name' : yelp['name']})
    result.update({'categories' : [i['title'] for i in yelp['categories']]})
    result.update({'address1' : yelp['location']['address1']})
    result.update({'address2' : yelp['location']['address2']})
    result.update({'city' : yelp['location']['city']})
    result.update({'state' : yelp['location']['state']})
    result.update({'zip_code' : yelp['location']['zip_code']})
    result.update({'latitude' : yelp['coordinates']['latitude']})
    result.update({'longitude' : yelp['coordinates']['longitude']})
    
    result.update({'phone' : None})
    result.update({'url' : None})
    result.update({'email' : None})
    result.update({'hours' : None})
    result.update({'description' : None})
    result.update({'owner' : None})
    
    result.update({'products' : []})
    
    return result

def map_image(key, center, size=None, zoom=None):
    """
    Generates url of static google maps image. 
    
    Input:
        key (str) : Google Maps API key (generate one at https://developers.google.com/maps/documentation/javascript/get-api-key)
        center (str, tuple) : location as an address or set of geo coordinates to center the image on
        size (tuple) : width, height of image in pixels, defaults to 600x300
        zoom (int) : level of map zoom, defaults to 13
        
    Output:
        url (str) : url of map image, able to be directly used with <img> html tags, etc. 
        """
    url = 'https://maps.googleapis.com/maps/api/staticmap?center='
    url += center.replace(' ', '+')
    
    if size == None:
        size = (600, 300)
    if zoom == None:
        zoom = 13
    
    url += '&zoom=' + str(zoom) + '&size=' + str(size[0]) + 'x' + str(size[1]) + '&maptype=roadmap&key=' + key
    return url