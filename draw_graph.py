import networkx as nx
import matplotlib.pyplot as plt
import os
import json
import user
import min_user

d = {}
g = nx.DiGraph()

# fake data

# directory_to_search = '/home/trent/PycharmProjects/CSC 877 Twitter/1k_data_power_law/fake_users/'
# min_obj_in_dir = '/home/trent/PycharmProjects/CSC 877 Twitter/min_object_scores/'
# outgraph_directory = '/home/trent/PycharmProjects/CSC 877 Twitter/graphs/'

# real data
# directory_to_search = '/home/trent/PycharmProjects/CSC 877 Twitter/real_data/user_list/'
# min_obj_in_dir = '/home/trent/PycharmProjects/CSC 877 Twitter/real_data/min_object_scores/'
# outgraph_directory = '/home/trent/PycharmProjects/CSC 877 Twitter/real_data/graphs/'

# fake data 2
directory_to_search = '/home/trent/PycharmProjects/CSC 877 Twitter/fake_data_2/twitter_users/'
min_obj_in_dir = '/home/trent/PycharmProjects/CSC 877 Twitter/fake_data_2/min_object_scores/'
outgraph_directory = '/home/trent/PycharmProjects/CSC 877 Twitter/fake_data_2/graphs/'


def read_user(file_name):
    try:
        with open(file_name, 'r') as json_data:
            info = json.load(json_data)
            # fake data
            # read_user = user.User(info['user_id'])

            # real data
            read_user = user.User(info['user_id'])
            read_user.average_retweet_count = info['average_retweet_count']
            read_user.followers_count = info['followers_count']
            read_user.influence_score = info['influence_score']
            read_user.average_favorite_count = info['average_favorite_count']
            read_user.follower_list = info['follower_list']
            return read_user
    except FileNotFoundError:
        print('Could not find file: ' + file_name)


def read_min_user(file_name):
    try:
        with open(file_name, 'r') as json_data:
            info = json.load(json_data)
            read_user = min_user.Min_user(info['user_id'], info['influence_score'])
            read_user.network_influence = info['network_influence']
            return read_user
    except FileNotFoundError:
        print('Could not find file: ' + file_name)


def run():
    global g
    for file_name in os.listdir(directory_to_search):
        if len(file_name) <= 11 or file_name == 'user100.json':
            user_info = read_user(directory_to_search+file_name)
            min_user_obj = read_min_user(min_obj_in_dir + user_info.user_id + '.json')
            for follower_name in user_info.follower_list:
                # follower = read_min_user(min_obj_in_dir + '/followers/' + follower_name + '.json')
                follower = read_min_user(min_obj_in_dir + follower_name + '.json')
                if float(follower.influence_score) >= 1000:
                    g.add_edge(follower, min_user_obj, weight=.1*float(follower.influence_score))
                    follower_info = read_user(directory_to_search + follower.user_id+'.json')
                    for follower_2_name in follower_info.get_follower_list():
                        min_follower_2_obj = read_min_user(min_obj_in_dir + follower_2_name + '.json')
                        if float(min_follower_2_obj.influence_score) >= 1200:
                            g.add_edge(min_follower_2_obj, follower,
                                       weight=.1**2*float(min_follower_2_obj.influence_score))


run()
# edges = g.edges()
# print(edges)
# values = [d.get(node, node.influence_score) for node in g.nodes()]
# limits = plt.axis('off')
# pos = nx.fruchterman_reingold_layout(g, k = 100)
print('== Finished ==')
# nx.draw_networkx(g, pos, cmap=plt.get_cmap('jet'), node_color=values, with_labels=False)
print('== Writing ==')
nx.write_gexf(g, outgraph_directory+'fake_data_2.gexf')
# plt.show()