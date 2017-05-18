# Trent Liu
# tliu3@mail.sfsu.edu
# 4/29/2017
#
# user stats class


class User_Stats:
    def __init__(self, user, depth_scores, depth_followers, network_score):
        self.user_id = user.user_id
        self.followers_count = user.followers_count
        self.influence_score = user.influence_score
        self.average_retweet_count = user.average_retweet_count
        self.average_favorite_count = user.average_retweet_count
        self.verified = user.verified
        self.network_score = network_score
        self.start_rank = 0
        self.end_rank = 0
        self.depth_scores = depth_scores
        self.depth_followers = depth_followers

        self.verified = False

    def __str__(self):
        return  'user_id: ' + self.user_id + '\n' + \
                'followers: ' + str(self.followers_count) + '\n' + \
                'average retweet count: ' + str(self.average_retweet_count) + '\n' \
                'average_favorite_count: ' + str(self.average_favorite_count) + '\n' \
                'verified: ' + str(self.verified) + '\n' \
                'influence score: ' + str(self.influence_score) + '\n' \
                'start rank: ' + str(self.start_rank) + '\n' \
                'end rank: ' + str(self.end_rank) + '\n' \
                'scores at each depth: ' + str(self.depth_scores) + '\n' \
                'followers at each depth: ' + str(self.depth_followers) + '\n'


    def to_json(self):
        return {'user_id': self.user_id,
                'followers_count': self.followers_count,
                'average_retweet_count': self.average_retweet_count,
                'average_favorite_count': self.average_favorite_count,
                'verified': self.verified,
                'influence_score': self.influence_score,
                'network_score': self.network_score,
                'start_rank': self.start_rank,
                'end_rank': self.end_rank,
                'depth_scores': self.depth_scores,
                'depth_followers': self.depth_followers}
