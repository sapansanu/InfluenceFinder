# Trent Liu
# tliu3@mail.sfsu.edu
# 4/29/2017
#
# user class to be generated

class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.followers_count = 0
        self.influence_score = 0
        self.average_retweet_count = 0.0
        self.average_favorite_count = 0.0
        self.follower_list = []
        self.verified = False

    def __str__(self):
        return 'user_id: ' + self.user_id + '\n' + \
               'followers: ' + str(self.followers_count) + '\n' + \
               'average retweet count: ' + str(self.average_retweet_count) + '\n' \
                'average_favorite_count: ' + str(self.average_favorite_count) + '\n' \
                'verified: ' + str(self.verified) + '\n' \
                'follower_list: ' + str(self.follower_list) + '\n' \
               'influence score: ' + str(self.influence_score) + '\n'

    def get_user_id(self):
        return self.user_id

    def get_follower_list(self):
        return self.follower_list

    def get_influence_score(self):
        return self.influence_score

    def to_json(self):
        return {'user_id': self.user_id, 'followers': self.followers_count,
                'average_retweet_count': self.average_retweet_count,
                'average_favorite_count': self.average_favorite_count, 'verified': self.verified,
                'follower_list': self.follower_list, 'influence_score': self.influence_score}
