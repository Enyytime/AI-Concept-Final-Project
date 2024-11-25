import pandas as pd
import requests
import networkx as nx

# Load dataset
df = pd.read_csv('D:/Code/Coding Stuff/2nd Year/AI Concpet/open_pubs.csv')

# Clean the dataset
df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
df = df.dropna(subset=['latitude', 'longitude'])
df = df.drop_duplicates(subset=['name'], keep='last')

# Choose a city to limit the dataset size
chosen_city = "City of London"
df_chosen_city = df[df['local_authority'] == chosen_city].head(50)  # limit it to 50 pubs

# OSRM function to get the shortest route and distance between two locations
def get_osrm_route(start_coords, end_coords):
    url = f"http://router.project-osrm.org/route/v1/driving/{start_coords[1]},{start_coords[0]};{end_coords[1]},{end_coords[0]}?overview=full&geometries=geojson"
    response = requests.get(url)
    
    if response.status_code == 200:
        route_data = response.json()
        distance_meters = route_data['routes'][0]['distance']  # Distance in meters
        route_coords = route_data['routes'][0]['geometry']['coordinates']
        return route_coords, distance_meters
    else:
        return None, None

# Initialize an empty graph using networkx
G = nx.Graph()

# Add nodes (pubs) to the graph
for i, row in df_chosen_city.iterrows():
    G.add_node(row['name'], pos=[row['latitude'], row['longitude']])  # Use list for position

# Add edges (routes between pubs) and calculate distances
for i in range(len(df_chosen_city) - 1):
    for j in range(i + 1, len(df_chosen_city)):  # Fully connected graph
        start_coords = (df_chosen_city.iloc[i]['latitude'], df_chosen_city.iloc[i]['longitude'])
        end_coords = (df_chosen_city.iloc[j]['latitude'], df_chosen_city.iloc[j]['longitude'])
        
        # Get route coordinates and distance from OSRM
        route, distance_meters = get_osrm_route(start_coords, end_coords)
        
        if route:
            distance_km = distance_meters / 1000  # Convert to kilometers
            G.add_edge(df_chosen_city.iloc[i]['name'], df_chosen_city.iloc[j]['name'], weight=distance_km)

# Save the graph in GraphML format
nx.write_graphml(G, 'pub_graph.graphml')
