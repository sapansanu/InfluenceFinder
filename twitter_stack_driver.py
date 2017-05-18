# Trent Liu
# tliu3@mail.sfsu.edu
# 4/29/2017
#
# main driver for data analysis

import networkx as nx
import read
import json
import os
import time
import stats_driver
import user_stats


# file names
network_stats_file_name = 'network_results.json'


# directory list [0]: real data, [1]: fake data
cwd = os.getcwd()
directory_to_search = [cwd + '/real_data/twitter_users/',
                       cwd + '/fake_data_2/twitter_users/',
                       cwd + '/fake_data_3/twitter_users/']
gpickle_out_directory = [cwd + '/real_data/gpickle/',
                         cwd + '/fake_data_2/gpickle/',
                         cwd + '/fake_data_3/gpickle/']
out_graph_directory = [cwd + '/real_data/graphs/',
                       cwd + '/fake_data_2/graphs/',
                       cwd + '/fake_data_3/graphs/']
min_obj_out_directory = [cwd + '/real_data/min_object_scores/',
                         cwd + '/fake_data_2/min_object_scores/',
                         cwd + '/fake_data_3/min_object_scores/']
test_out_directory = [cwd + '/real_data/test_results/',
                      cwd + '/fake_data_2/test_results/',
                      cwd + '/fake_data_3/test_results/']
user_stats_out_directory = [cwd + '/real_data/user_stats/',
                            cwd + '/fake_data_2/user_stats/',
                            cwd + '/fake_data_3/user_stats/']

# tuple for network and it's score


def iterate(directory, user_obj, d, g, real):
    depth_to_iterate = int(d)
    # stack to keep track of users per depth
    stack = []
    # list of the positions of each follower at each depth
    follower_index = [0] * depth_to_iterate
    # current depth
    count = 0

    # stats
    follower_count_stats = [0] * depth_to_iterate
    follower_influence_stats = [0] * depth_to_iterate
    # total_stats = [follower_count_stats, follower_influence_stats]
    stack.append(user_obj)

    while len(stack) != 0:
        if count < depth_to_iterate - 1:
            # if we haven't finished iterating through all the users at a particular depth
            if follower_index[count] < len(stack[count].get_follower_list()):
                stack.append(read.read(directory+'followers/'*(depth_to_iterate-1)*real + user_obj.get_follower_list()[follower_index[count]] + '.json'))
                follower_index[count] += 1
                count += 1
            else:
                pop_stack(directory+'followers/'*(depth_to_iterate-1)*real, stack.pop(), count, follower_influence_stats, follower_count_stats, g)
                count -= 1
        else:
            pop_stack(directory+'followers/'*depth_to_iterate*real, stack.pop(), count, follower_influence_stats, follower_count_stats, g)
            count -= 1
    # returns a user stats object
    graph_sum = 0
    for edge in g.edges(data=True):
        graph_sum += float(edge[2]['weight'])
    graph_sum += float(user_obj.influence_score)

    return user_stats.User_Stats(user_obj, follower_influence_stats, follower_count_stats, graph_sum)


# pop last user and create edges between this user and it's followers
def pop_stack(directory, temp_var, count, follower_influence_stats, follower_count_stats, g):
    for follower in temp_var.get_follower_list():
        follower_obj = read.read(directory + follower + '.json')
        if follower_obj != None:
            # adds edge with dampening coefficient
            weight = 0.1 ** (count + 1) * float(follower_obj.get_influence_score())
            g.add_edge(follower_obj.user_id, temp_var.user_id, weight=weight)
            # stats
            follower_count_stats[count] += 1
            follower_influence_stats[count] += weight


# driver to create generate fake data stats and graphs
def fake_data_driver(depth_to_iterate, index):
    network_tuple_list = []
    stats_object_dict = {}
    time_start = time.clock()
    file_length = 0
    stop_name = ''
    if index == 1:
        file_length = 11
        stop_name = 'user100.json'
    elif index == 2:
        file_length = 12
        stop_name = 'user1000.json'
    # f = nx.DiGraph()
    for file_name in os.listdir(directory_to_search[index]):
        if len(file_name) <= file_length or file_name == stop_name:
            # if file_name == 'user1.json':
            print(file_name)
            g = nx.DiGraph()

            # generates user object
            user_object = read.read(directory_to_search[index] + file_name)

            # creates user stats object to store meta data
            user_stats_object = iterate(directory_to_search[index], user_object, depth_to_iterate, g, 0)

            # appends user stats object onto a list
            stats_object_dict[file_name[:-5]] = user_stats_object

            # appends user name and network score onto a list
            network_tuple_list.append((file_name[:-5], user_stats_object.network_score))
            # f = nx.compose(f, g)
    print('Time to process:', time.clock() - time_start)
    network_tuple_list.sort(key=lambda tup: tup[1])
    network_tuple_list.reverse()
    # nx.write_gexf(f, out_graph_directory[0] + 'test.gexf')

    influence_list = stats_driver.order_fake_influence(directory_to_search[index], index+1)
    for i in range(len(influence_list)):
        stats_object = stats_object_dict[influence_list[i][0]]
        stats_object.start_rank = i
        stats_object.end_rank = stats_driver.search_tuple(stats_object.user_id, network_tuple_list)
        try:
            with open(user_stats_out_directory[index] + stats_object.user_id + '.json', 'w+') as outfile:
                json.dump(stats_object.to_json(), outfile)
        except Exception as e:
            print(e)
    with open(test_out_directory[index] + network_stats_file_name, 'w+') as outfile:
        json.dump(dict(network_tuple_list), outfile)


def real_data_driver(depth_to_iterate):
    network_tuple_list = []
    stats_object_dict = {}
    time_start = time.clock()
    f = nx.DiGraph()
    for file_name in os.listdir(directory_to_search[0]):
        # if file_name == 'user1.json':
        if file_name != 'followers':
            print(file_name)
            g = nx.DiGraph()

            # generates user object
            user_object = read.read(directory_to_search[0] + file_name)

            # creates user stats object to store meta data
            user_stats_object = iterate(directory_to_search[0], user_object, depth_to_iterate, g, 1)

            # appends user stats object onto a list
            stats_object_dict[file_name[:-5]] = user_stats_object

            # appends user name and network score onto a list
            network_tuple_list.append((file_name[:-5], user_stats_object.network_score))
            f = nx.compose(f, g)
    print('Time to process:', time.clock() - time_start)
    network_tuple_list.sort(key=lambda tup: tup[1])
    network_tuple_list.reverse()
    nx.write_gexf(f, out_graph_directory[0] + 'test.gexf')
    influence_list = stats_driver.order_real_influence(directory_to_search[0])

    for i in range(len(influence_list)):
        stats_object = stats_object_dict[influence_list[i][0]]
        stats_object.start_rank = i
        stats_object.end_rank = stats_driver.search_tuple(stats_object.user_id, network_tuple_list)
        try:
            with open(user_stats_out_directory[0] + stats_object.user_id + '.json', 'w+') as outfile:
                json.dump(stats_object.to_json(), outfile)
        except Exception as e:
            print('Exception: ', e)
    with open(test_out_directory[0] + network_stats_file_name, 'w+') as outfile:
        json.dump(dict(network_tuple_list), outfile)

if __name__ == '__main__':

    while True:
        print('======================')
        print('1. Analyze score')
        print('2. Print Analysis')
        print('0. Exit')
        choice = input('Enter choice: ')

        if choice == '1':
            print('======================')
            print('1. Real data set')
            print('2. Fake data set 10k')
            print('3. Fake data set 100k')
            data_selection = input('Enter data source: ')
            print('== Start Analysis ==')
            if data_selection is '1':
                print('======================')
                depth = input('Enter depth to traverse (max 2): ')
                real_data_driver(depth)
                print('== Network Sorted ==')
            elif data_selection is '2':
                print('======================')
                depth = input('Enter depth to traverse (max 2): ')
                if int(depth) < 3:
                    fake_data_driver(depth, 1)
                    print('== Network Sorted ==')
                else:
                    print('Please enter an integer less than 3')
                    continue
            elif data_selection is '3':
                print('======================')
                depth = input('Enter depth to traverse (max 2): ')
                if int(depth) < 3:
                    fake_data_driver(depth, 2)
                    print('== Network Sorted ==')
                else:
                    print('Please enter an integer less than 3')
                    continue

        elif choice == '2':
            print('======================')
            print('== Compiling stats ==')
            print('1. Compile stats for Real data set')
            print('2. Compile stats for Fake data set 10k')
            print('3. Compile stats for Fake data set 100k')
            choice = input('Enter choice: ')
            stats_driver.compile_stats_driver(network_stats_file_name,
                                              directory_to_search,
                                              test_out_directory,
                                              user_stats_out_directory,
                                              choice)

        elif choice == '0':
            print('======================')
            print('= Program terminated =')
            print('======================')
            break

            # nx.write_gexf(g, '/home/trent/PycharmProjects/CSC 877 Twitter/fake_data_2/graphs/fake_data_2_test.gexf')



            # faster implementation, possible parallelization

            # def graph(user, d):
            #     depth = 0
            #     retn = kev_iterate(user.get_follower_list(), user, depth, d)
            #     while len(retn) != 0:
            #         depth += 1
            #         for r in retn:
            #             user_obj = read(directory_to_search + r + '.json')
            #             retn += kev_iterate(user_obj.get_follower_list(), user_obj, depth, d)
            #
            #
            # def iterate(followers, parent, n, d):
            #     if n < d:
            #         flws = []
            #         for f in followers:
            #             user_obj = read(directory_to_search + f + '.json')
            #             g.add_edge(parent, user_obj)
            #             flws.append(f)
            #         return flws
            #
            #     else:
            #         return []
