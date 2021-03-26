# following this example:
# https://openrouteservice.org/example-apartment-search-with-ors/

import folium
from openrouteservice import client


api_key = '5b3ce3597851110001cf6248316547730c13449498f0ac6c7b88ba62' #Provide your personal API key
clnt = client.Client(key=api_key) 
# Set up folium map
map1 = folium.Map(tiles='Stamen Terrain', location=([50.575587549617886, -121.83890221698378]), zoom_start=7)

# Set up the apartment dictionary with real coordinates
abattoir_dict = {'XH Buffalo Ranch': {'location': [51.39557020423438, -121.20192825105231]},
            'Kam Lake-View Meats Ltd.': {'location': [50.71091611182109, -120.63366067736604]},
            'Meadow Valley Meats': {'location': [49.225067692716316, -122.70716677634903]}
           }

# Request of isochrones with 15 minute footwalk.
params_iso = {'profile': 'driving-car',
              'intervals': [3600],
              'segments': 3600,
             }

for name, ab in abattoir_dict.items():
    params_iso['locations'] = [list(reversed(ab['location']))] # Add abattoir coords to request parameters. Reverse coordinates (folium requires them in the opposite order)
    ab['iso'] = clnt.isochrones(**params_iso) # Perform isochrone request
    folium.features.GeoJson(ab['iso']).add_to(map1) # Add GeoJson to map
    
    folium.map.Marker(ab['location'],
                      icon=folium.Icon(color='lightgray',
                                        icon_color='#cc0000',
                                        icon='check',
                                        prefix='fa',
                                       ),
                      popup=name,
                 ).add_to(map1) # Add apartment locations to map

# add marker for Spray Creek Ranch
folium.map.Marker(
    [50.575587549617886, -121.83890221698378],
    icon=folium.Icon(color='lightgray',
    icon_color='#cc0000',
    icon='home',
    prefix='fa',
    ),
    popup='Spray Creek Ranch',
).add_to(map1)

#map1
map1.save(outfile='index.html')
