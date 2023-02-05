import gym
import random
import numpy as np
import time
from collections import deque
import pickle


from collections import defaultdict


EPISODES =  20000
LEARNING_RATE = .3
DISCOUNT_FACTOR = .99
EPSILON = 1
EPSILON_DECAY = .999


def default_Q_value():
    return 0

if __name__ == "__main__":

    random.seed(1)
    np.random.seed(1)
    env = gym.envs.make("FrozenLake-v1")
    env.seed(1)
    env.action_space.np_random.seed(1)


    # You will need to update the Q_table in your iteration
    Q_table = np.zeros([env.observation_space.n, env.action_space.n]) # starts with a pessimistic estimate of zero reward for each state.
    episode_reward_record = deque(maxlen=100)

    for i in range(EPISODES):
        episode_reward = 0
        done = False
        obs = env.reset()

        ##########################################################
        # YOU DO NOT NEED TO CHANGE ANYTHING ABOVE THIS LINE
        # TODO: Replace the following with Q-Learning

        while (not done):
            if random.uniform(0,1) < EPSILON:
                action = env.action_space.sample() # currently only performs a random action.
            else:
                action = np.argmax(Q_table[obs])
            
            new_obs,reward,done,info = env.step(action)
            
            old_entry = Q_table[obs, action]
            next_act = np.max(Q_table[new_obs])
            
            new_entry = (1-LEARNING_RATE) * old_entry + LEARNING_RATE * (reward + DISCOUNT_FACTOR * next_act)
            Q_table[obs, action] = new_entry
            
            
            episode_reward += reward # update episode reward
            EPSILON = EPSILON*EPSILON_DECAY
            
            obs = new_obs

        # END of TODO
        # YOU DO NOT NEED TO CHANGE ANYTHING BELOW THIS LINE
        ##########################################################

        # record the reward for this episode
        episode_reward_record.append(episode_reward) 

        
        if i%100 ==0 and i>0:
            print("LAST 100 EPISODE AVERAGE REWARD: " + str(sum(list(episode_reward_record))/100))
            print("EPSILON: " + str(EPSILON) )
    
    
    #### DO NOT MODIFY ######
    model_file = open('Q_TABLE.pkl' ,'wb')
    pickle.dump([Q_table,EPSILON],model_file)
    model_file.close()
    #########################