import facebook
USER_TOKEN = "EAAGJNkHBQZAEBAGa7qPV2AYSr9YxfwpE7QcinCNpZAZCoSkqA17ZBbZC63G1iTlNmXxjyYNPytbikmT5AQk72PrECpJa0rihEAQG0CN15tHrHRsYl17XB7BBX6j4RnIM1SDaJuyuN9ZAZAoy1m8ocnT7qV3p8e3tpqBvJZCECGbBUokHmchkPDRxllpkCDCmhBnBNlQBPNG8EAZDZD"
graph = facebook.GraphAPI(access_token=USER_TOKEN, version="2.12")


def follower_count(graph):
    followers = graph.get_object(id='me', fields='followers_count')
    print("Cantidad de seguidores: " + str(followers['followers_count'])) 

def main():
    follower_count(graph)
    
main()