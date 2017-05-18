import json
from random import randint

def generate_fake_user():

     for i in range(1,101):               #user id range
        followers_count = randint(20,2000)
        followers_count = int(followers_count*(2*10**4/(followers_count)**2.101))
        print(followers_count)
        average_retweet_count = randint(0,500)
        average_favorite_count = randint(0,1000)
        influence_score = round((followers_count*0.5) + (average_retweet_count*0.33) + (average_favorite_count*0.17),2)
        data = {
        "screen_name": "user"+str(i),
        "average_retweet_count" : str(average_retweet_count),
        "average_favorite_count" : str(average_favorite_count),
        "followers_count" : str(followers_count),
        "verified" : str(bool(randint(0,1))),
        "influence_score": str(influence_score),
        "follower_list": []
        }
        for j in range(1,followers_count+1):
            temp = "user"+str(randint(101,5000))       #follower id range
            if temp not in data['follower_list']:
                data['follower_list'] += [temp]
            else:
                data['followers_count'] = str(int(data['followers_count']) - 1)
        file = open("./fake_users/user"+str(i)+".json","w")
        json.dump(data,file, indent=4)
        file.close()


def read_json():
    for i in range(1,1001):
        with open("./fake_users/user"+str(i)+".json","r") as file:
            data = json.load(file)
            influence_score1000 = (float(data['followers_count'])*1.25*0.5) + (float(data['average_retweet_count'])*5*0.33) + (float(data['average_favorite_count'])*1.25*0.17)
            print(influence_score1000)
            influence_score100 = (float(data['followers_count'])*0.5/8) + (float(data['average_retweet_count'])*0.5*0.33) + (float(data['average_favorite_count'])*0.25*0.17)
            print(influence_score100)



if __name__ == "__main__":
    generate_fake_user()
