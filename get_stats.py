import os
import json
import user
import user_stats

user_stats_in = '/home/trent/PycharmProjects/CSC 877 Twitter/fake_data_2/user_stats/'
test_in_dir = '/home/trent/PycharmProjects/CSC 877 Twitter/fake_data_2/test_results/'
initial_tuple_list = []
network_tuple = []


def read_stats(file_name):
    try:
        with open(file_name, 'r') as json_data:
            info = json.load(json_data)
            temp_user = user.User(info['user_id'])
            temp_user.average_retweet_count = info['average_retweet_count']
            temp_user.followers_count = info['followers_count']
            temp_user.influence_score = info['influence_score']
            temp_user.average_favorite_count = info['average_favorite_count']
            read_user = user_stats.User_Stats(temp_user,
                                              info['edges'],
                                              info['depth_2_score'],
                                              info['depth_3_score'],
                                              info['followers_at_d2'],
                                              info['followers_at_d3'])
            read_user.average_retweet_count = info['average_retweet_count']
            read_user.followers_count = info['followers_count']
            read_user.influence_score = info['influence_score']
            read_user.average_favorite_count = info['average_favorite_count']
            read_user.network_score = info['average_retweet_count']
            return read_user
    except FileNotFoundError:
        print('Could not find file: ' + file_name)


def search_tuple(user_id):
    for tuple_rank in range(0,len(network_tuple)):
        if network_tuple[tuple_rank][0] == user_id:
            return tuple_rank

file_count = 0
for file_name in os.listdir(user_stats_in):
    if len(file_name) <= 11 or file_name == 'user100.json':
        file_count+=1
        user_object = read_stats(user_stats_in+file_name)
        initial_tuple_list.append((user_object.user_id, user_object.influence_score))

initial_tuple_list.sort(key=lambda tup: float(tup[1]))
initial_tuple_list.reverse()

with open(test_in_dir + 'results.json', 'r') as infile_score:
    network_score = json.load(infile_score)

for key in network_score.keys():
    network_tuple.append((key, network_score[key]))

network_tuple.sort(key=lambda tup: float(tup[1]))
network_tuple.reverse()
print(network_tuple)
rank = 1
for item in initial_tuple_list:
    print('Rank ' + str(rank) + ' -- ' + item[0] + ' -- ' + str(item[1]) + ' -- Influential ranking: ' +
          str(search_tuple(item[0])+1) + ' -- Network Score: ' + str(network_score[str(item[0])]))
    rank += 1
    if rank > 10:
        break
