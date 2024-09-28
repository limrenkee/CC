import json
import logging
import heapq

from flask import request

from routes import app

logger = logging.getLogger(__name__)

@app.route('/tourist', methods=['POST'])
def evaluate():
    data = request.get_json()
    print(data)
    return solution(data)
    #logging.info("data sent for evaluation {}".format(data))
    #input_value = data.get("input")
    #result = input_value * input_value
    #logging.info("My result :{}".format(result))
    #return json.dumps(result)

def solution(sample_input):
    subway_stations = {
        "Tokyo Metro Ginza Line": [
            "Asakusa", "Tawaramachi", "Inaricho", "Ueno", "Ueno-hirokoji", "Suehirocho",
            "Kanda", "Mitsukoshimae", "Nihombashi", "Kyobashi", "Ginza", "Shimbashi",
            "Toranomon", "Tameike-sanno", "Akasaka-mitsuke", "Nagatacho", "Aoyama-itchome",
            "Gaiemmae", "Omotesando", "Shibuya"
        ],
        "Tokyo Metro Marunouchi Line": [
            "Ogikubo", "Minami-asagaya", "Shin-koenji", "Higashi-koenji", "Shin-nakano",
            "Nakano-sakaue", "Nishi-shinjuku", "Shinjuku", "Shinjuku-sanchome", "Shin-ochanomizu",
            "Ochanomizu", "Awajicho", "Otemachi", "Tokyo", "Ginza", "Kasumigaseki", "Kokkai-gijidomae",
            "Akasaka-mitsuke", "Yotsuya", "Yotsuya-sanchome", "Shinjuku-gyoemmae", "Nishi-shinjuku-gochome",
            "Nakano-fujimicho", "Nakano-shimbashi", "Nakano-sakaue", "Shinjuku-sanchome", "Kokkai-gijidomae",
            "Kasumigaseki", "Ginza", "Tokyo", "Otemachi", "Awajicho", "Shin-ochanomizu", "Ochanomizu"
        ],
        "Tokyo Metro Hibiya Line": [
            "Naka-meguro", "Ebisu", "Hiroo", "Roppongi", "Kamiyacho", "Kasumigaseki", "Hibiya",
            "Ginza", "Higashi-ginza", "Tsukiji", "Hatchobori", "Kayabacho", "Nihombashi",
            "Kodemmacho", "Akihabara", "Naka-okachimachi", "Ueno", "Iriya", "Minowa",
            "Minami-senju", "Kita-senju"
        ],
        "Tokyo Metro Tozai Line": [
            "Nakano", "Ochiai", "Takadanobaba", "Waseda", "Kagurazaka", "Iidabashi", "Kudanshita",
            "Takebashi", "Otemachi", "Nihombashi", "Kayabacho", "Monzen-nakacho", "Kiba",
            "Toyosu", "Minami-sunamachi", "Nishi-kasai", "Kasai", "Urayasu", "Minami-gyotoku",
            "Gyotoku", "Myoden", "Baraki-nakayama", "Nishi-funabashi"
        ],
        "Tokyo Metro Chiyoda Line": [
            "Yoyogi-uehara", "Yoyogi-koen", "Meiji-jingumae", "Omotesando", "Nogizaka", "Akasaka",
            "Kokkai-gijidomae", "Kasumigaseki", "Hibiya", "Nijubashimae", "Otemachi",
            "Shin-ochanomizu", "Yushima", "Nezu", "Sendagi", "Nishi-nippori", "Machiya",
            "Kita-senju", "Ayase", "Kita-ayase"
        ],
        "Tokyo Metro Yurakucho Line": [
            "Wakoshi", "Chikatetsu-narimasu", "Chikatetsu-akatsuka", "Heiwadai", "Hikawadai",
            "Kotake-mukaihara", "Senkawa", "Kanamecho", "Ikebukuro", "Higashi-ikebukuro",
            "Gokokuji", "Edogawabashi", "Iidabashi", "Ichigaya", "Kojimachi", "Nagatacho",
            "Sakuradamon", "Yurakucho", "Ginza-itchome", "Shintomicho", "Toyocho",
            "Kiba", "Toyosu", "Tsukishima", "Shintomicho", "Tatsumi", "Shinonome", "Ariake"
        ],
        "Tokyo Metro Hanzomon Line": [
            "Shibuya", "Omotesando", "Aoyama-itchome", "Nagatacho", "Hanzomon", "Kudanshita",
            "Jimbocho", "Otemachi", "Mitsukoshimae", "Suitengumae", "Kiyosumi-shirakawa",
            "Sumiyoshi", "Kinshicho", "Oshiage"
        ],
        "Tokyo Metro Namboku Line": [
            "Meguro", "Shirokanedai", "Shirokane-takanawa", "Azabu-juban", "Roppongi-itchome",
            "Tameike-sanno", "Nagatacho", "Yotsuya", "Ichigaya", "Iidabashi", "Korakuen",
            "Todaimae", "Hon-komagome", "Komagome", "Nishigahara", "Oji", "Oji-kamiya",
            "Shimo", "Akabane-iwabuchi"
        ],
        "Tokyo Metro Fukutoshin Line": [
            "Wakoshi", "Chikatetsu-narimasu", "Chikatetsu-akatsuka", "Narimasu", "Shimo-akatsuka",
            "Heiwadai", "Hikawadai", "Kotake-mukaihara", "Senkawa", "Kanamecho", "Ikebukuro",
            "Zoshigaya", "Nishi-waseda", "Higashi-shinjuku", "Shinjuku-sanchome", "Kita-sando",
            "Meiji-jingumae", "Shibuya"
        ],
        "Toei Asakusa Line": [
            "Nishi-magome", "Magome", "Nakanobu", "Togoshi", "Gotanda", "Takanawadai",
            "Sengakuji", "Mita", "Shiba-koen", "Daimon", "Shimbashi", "Higashi-ginza",
            "Takaracho", "Nihombashi", "Ningyocho", "Higashi-nihombashi", "Asakusabashi",
            "Kuramae", "Asakusa", "Honjo-azumabashi", "Oshiage"
        ],
        "Toei Mita Line": [
            "Meguro", "Shirokanedai", "Shirokane-takanawa", "Mita", "Shiba-koen", "Onarimon",
            "Uchisaiwaicho", "Hibiya", "Otemachi", "Jimbocho", "Suidobashi", "Kasuga",
            "Hakusan", "Sengoku", "Sugamo", "Nishi-sugamo", "Shin-itabashi", "Itabashi-kuyakushomae",
            "Itabashi-honcho", "Motohasunuma", "Shin-takashimadaira", "Nishidai", "Hasune",
            "Takashimadaira", "Shimura-sakaue", "Shimura-sanchome", "Nishidai"
        ],
        "Toei Shinjuku Line": [
            "Shinjuku", "Shinjuku-sanchome", "Akebonobashi", "Ichigaya", "Kudanshita",
            "Jimbocho", "Ogawamachi", "Iwamotocho", "Bakuro-yokoyama", "Hamacho",
            "Morishita", "Kikukawa", "Sumiyoshi", "Nishi-ojima", "Ojima", "Higashi-ojima",
            "Funabori", "Ichinoe", "Mizue", "Shinozaki", "Motoyawata"
        ],
        "Toei Oedo Line": [
            "Hikarigaoka", "Nerima-kasugacho", "Toshimaen", "Nerima", "Nerima-sakamachi",
            "Shin-egota", "Ochiai-minami-nagasaki", "Nakai", "Higashi-nakano", "Nakano-sakaue",
            "Nishi-shinjuku-gochome", "Tochomae", "Shinjuku-nishiguchi", "Higashi-shinjuku",
            "Wakamatsu-kawada", "Ushigome-yanagicho", "Ushigome-kagurazaka", "Iidabashi",
            "Kasuga", "Hongosanchome", "Ueno-okachimachi", "Shin-okachimachi", "Kuramae",
            "Ryogoku", "Morishita", "Kiyosumi-shirakawa", "Monzen-nakacho", "Tsukishima",
            "Kachidoki", "Shiodome", "Daimon", "Akasaka-mitsuke", "Roppongi", "Aoyama-itchome",
            "Shinjuku", "Tochomae", "Shinjuku", "Shinjuku-sanchome", "Higashi-shinjuku",
            "Wakamatsu-kawada", "Ushigome-yanagicho", "Ushigome-kagurazaka", "Iidabashi",
            "Kasuga", "Hongosanchome", "Ueno-okachimachi", "Shin-okachimachi", "Kuramae",
            "Ryogoku", "Morishita", "Kiyosumi-shirakawa", "Monzen-nakacho", "Tsukishima",
            "Kachidoki", "Shiodome", "Daimon", "Shiodome", "Tsukishima"
        ]
    }

    travelling_time = {
        "Tokyo Metro Ginza Line": 2,
        "Tokyo Metro Marunouchi Line": 3,
        "Tokyo Metro Hibiya Line": 2.5,
        "Tokyo Metro Tozai Line": 4,
        "Tokyo Metro Chiyoda Line": 1.5,
        "Tokyo Metro Yurakucho Line": 2,
        "Tokyo Metro Hanzomon Line": 2,
        "Tokyo Metro Namboku Line" : 1,
        "Tokyo Metro Fukutoshin Line": 3,
        "Toei Asakusa Line": 3.5,
        "Toei Mita Line": 4,
        "Toei Shinjuku Line": 1.5,
        "Toei Oedo Line": 1
    }

    # Helper function to build graph
    def build_graph(subway_lines, travel_times):
        graph = {}
        for line, stations in subway_lines.items():
            time = travel_times.get(line, 1)
            for i in range(len(stations) - 1):
                station1 = stations[i]
                station2 = stations[i + 1]
                graph.setdefault(station1, []).append((station2, time))
                graph.setdefault(station2, []).append((station1, time))
        return graph

    # Dijkstra's algorithm
    def dijkstra(graph, start, end):
        queue = [(0, start)]
        distances = {station: float('inf') for station in graph}
        distances[start] = 0
        predecessors = {station: None for station in graph}
        
        while queue:
            current_distance, current_station = heapq.heappop(queue)
            
            if current_station == end:
                break
            
            for neighbor, weight in graph[current_station]:
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_station
                    heapq.heappush(queue, (distance, neighbor))
        
        path, station = [], end
        while predecessors[station]:
            path.insert(0, station)
            station = predecessors[station]
        if path:
            path.insert(0, start)
        
        return path, distances[end]

    def find_shortest_paths(locations, graph):
        paths = {}
        loc_keys = list(locations.keys())
        
        for i in range(len(loc_keys)):
            for j in range(i + 1, len(loc_keys)):
                start = loc_keys[i]
                end = loc_keys[j]
                
                # Forward path: start -> end
                path, time_spent = dijkstra(graph, start, end)
                time_spent += locations[end][1]
                paths[(start, end)] = {"time": time_spent, "satisfaction": locations[end][0]}
                
                # Reverse path: end -> start
                reverse_path, reverse_time_spent = dijkstra(graph, end, start)
                reverse_time_spent += locations[start][1]
                paths[(end, start)] = {"time": reverse_time_spent, "satisfaction": locations[start][0]}

        return paths

    def find_max_satisfaction(graph, start_location, time_limit):
        # Variables to keep track of the best path and maximum satisfaction
        best_path = []
        max_satisfaction = 0

        # Helper function for DFS-like traversal
        def dfs(current_location, current_time, current_satisfaction, visited, path):
            nonlocal max_satisfaction, best_path
            
            # Check if we can return to the start within the time limit
            if current_time + graph[(current_location, start_location)]['time'] <= time_limit:
                # If we can, check if the current satisfaction is the highest
                if current_satisfaction > max_satisfaction:
                    max_satisfaction = current_satisfaction
                    best_path = path + [start_location]
            
            # Explore other locations
            for neighbor, data in graph.items():
                loc1, loc2 = neighbor
                travel_time = data['time']
                satisfaction = data['satisfaction']

                # We can only go to an unvisited location
                if loc1 == current_location and loc2 not in visited:
                    new_time = current_time + travel_time
                    if new_time <= time_limit:
                        dfs(loc2, new_time, current_satisfaction + satisfaction, visited | {loc2}, path + [loc2])
        
        # Start DFS from the initial location
        dfs(start_location, 0, 0, {start_location}, [start_location])
        
        return {
            "path": best_path,
            "satisfaction": max_satisfaction
        }

    graph = build_graph(subway_stations, travelling_time)
    shortest_paths = find_shortest_paths(sample_input["locations"], graph)
    start_station = sample_input["startingPoint"]
    time_limit = sample_input["timeLimit"]
    shortest_paths[(start_station, start_station)] = {'time': 0, 'satisfaction': 0} 
    result = find_max_satisfaction(shortest_paths, start_station, time_limit)
    return result

