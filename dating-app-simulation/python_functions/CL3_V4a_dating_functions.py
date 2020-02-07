import networkx as nx #This has to be networkx v1.x not 2.x, but small modifications should allow for verion 2.x
import random
import numpy as np
import time
import dating_functions as df1
import scipy.stats
#import dating_function_CL2 as df2
#########################################################################################################################################################
def decide(coins_a,cost):
    """
    this function allows the agent to decide whether it wants 
    to swipe or browse profiles
    """
    
    if (random.random() > 0.85 and coins_a >= cost):
        action = "Browse"
    else:
        action = "Swipe"
        
    return action

###############################################################################################################################################


################################################################################################################################################
def potential_swipe_for_male(node_a, 
                             gender_a, age_a,
                             male_list, female_list, 
                             origin_network, age_range,
                             like_record, dislike_record):
    """
    this function selects a potential profile node a can swipe/like
    
    it selects this profile based on their age and gender
    it also checks to make sure they have not interacted before
    """
    
    
    # list of those in node_a's age group
    potential_nodes = [x for x,y in origin_network.nodes(data=True) if ((age_a - age_range) <= y['age'] <= (age_a + age_range))]
    

    for i in range(10):
        
        if gender_a == "Male":
            potential_nodes = [x for x,y in origin_network.nodes(data=True) if (((age_a - age_range) <= y['age'] <= (age_a + age_range)) and (y['gender']=="Female"))]

            node_b = random.choice(potential_nodes)
            
        else:
            potential_nodes = [x for x,y in origin_network.nodes(data=True) if (((age_a - age_range) <= y['age'] <= (age_a + age_range)) and (y['gender']=="Male"))]
            node_b = random.choice(potential_nodes)
            
        # ensuring that node_a and node_b have not interacted before
        if (([node_a,node_b] not in like_record) and ([node_a,node_b] not in dislike_record)):
            return node_b
        # if the two nodes are
        
    
   # print("Already interacted with all these nodes")
    return False
 ###############################################################################################################################################
     
def potential_swipe_for_female(node_a, 
                               gender_a, age_a,
                               male_list, female_list, 
                               origin_network, age_range,
                               like_record, dislike_record):
    """
    this function selects a potential profile node a can swipe/like
    
    it selects this profile based on their age and gender
    it also checks to make sure they have not interacted before
    """
    
    
    # list of those in node_a's age group
    #potential_nodes = [x for x,y in origin_network.nodes(data=True) if ((age_a - age_range) <= y['age'] <= (age_a + age_range))]
    # try is going to see if it exists
    try:
        mat
    # except is going to run if it does not exist
    except:
        # print("mat doesn't exist yet")
        return False
    
    if mat != []:
        mat = np.array(like_record)
        mat[mat[:,1]==node_a]

        pair_chosen = random.choice(mat)
        node_b = pair_chosen[0]


        for i in range(10):
            #potential_nodes = [x for x,y in origin_network.nodes(data=True) if (((age_a - age_range) <= y['age'] <= (age_a + age_range)) and (y['gender']=="Male"))]

            pair_chosen = random.choice(mat)
            node_b = pair_chosen[0]
            #node_b = random.choice(potential_nodes)

            # check if node_b likes node_a
            if ([node_b, node_a] in like_record) and (([node_a, node_b] not in like_record)) and ([node_a,node_b] not in dislike_record):
                 #make dure the potential matches that are male already liked node_a and node_a did not like or dislike node_b previously. 
                return node_b
            else: # else if node_b does not like node_a
                continue
        
    return False
    
###############################################################################################################################################


###############################################################################################################################################
def match_power(node_a,gender_a, age_a,attractiveness_a,ethnicity_a,
               node_b,gender_b, age_b, attractiveness_b,ethnicity_b,                                                  
               origin_network,
               runs,i,
               list_score_m,list_score_f):
    
    """
    
    firstly, this function will generate a "match_power" based on male
    and female preferences. The two individuals will then be tested
    to see if they will match based on a random number, but the like
    score will highly influnce their probability to like. 
    
    ----------------------------------------------------------------
    
    attributes that go into the equation:
    
    Age:
        females prefer older men, and men prefer younger females
        
    Attractiveness:
        males put a higher priority on attractiveness than females do
    
    -----------------------------------------------------------------
    
    similarity between the two people will how they like as well
    
    Age: 
        If the two people are within two years, increase the probability to like
    
    Attractiveness:
        If the two people are within 0.2 points in attractiveness, increase
        the proabbility to like
    
    
        
    """
#   'ethnicity': np.random.randint(1,5),         # 1:5 different races
#   'education': np.random.randint(1,4),         # 1:4 different eduction levels
#   'profession': np.random.randint(1,12),  
    
    # first checking to see if node_a is male
    if gender_a == "Male":
        # Ethnicity
        # If same ethnicity, score of both is from .5 inclusive to 1, *weight. If different ethnicity, from 0 to .5 * weight.
        if ethnicity_a == ethnicity_b:
            score_m =+ .3 * np.random.rand()/2 + .5
            score_f =+ .4 * np.random.rand()/2 + .5
        else:
            score_m =+ .3 * np.random.rand()/2
            score_f =+ .4 * np.random.rand()/2
       
        # Physical_attractiveness:
        # Based on standard bell curve, Standard Deviation of .341:
        score_m = 0.4 * (1-abs((scipy.stats.norm(0,0.341**2).cdf(attractiveness_a-attractiveness_b)-.5)*2))
        score_f = 0.3 * (1-abs((scipy.stats.norm(0,0.341**2).cdf(attractiveness_a-attractiveness_b)-.5)*2))
       
        # Age difference:
        # The score of the male is increased by .3 * a value between 0 and 1, maximised when the age_b (female) minus
        # age_a (male) is as close to -3.996 as possible.
        score_m =+ .3 * (1-abs((scipy.stats.norm(-3.996,3.31662**2).cdf(age_b-age_a)-.5)*2))
        # The score of the female is increased by .4 * a value between 0 and 1, maximised when the age_a (male) minus
        # age_b (female) is as close to 2.0464 as possible.
        score_f =+ .3 * (1-abs((scipy.stats.norm(2.0464,2.90659**2).cdf(age_a-age_b)-.5)*2))
       
       
        like_a = score_m
        like_b = score_f
       
    else: #female
        # Ethnicity
        # If same ethnicity, score of both is from .5 inclusive to 1, *weight. If different ethnicity, from 0 to .5 * weight.
        if ethnicity_a == ethnicity_b:
            score_m =+ .3 * np.random.rand()/2 + .5
            score_f =+ .4 * np.random.rand()/2 + .5
        else:
            score_m =+ .3 * np.random.rand()/2
            score_f =+ .4 * np.random.rand()/2
       
        # physical_attractiveness:
        # Based on standard bell curve, Standard Deviation of .341:
        score_m = 0.4 * (1-abs((scipy.stats.norm(0,0.341**2).cdf(attractiveness_a-attractiveness_b)-.5)*2))
        score_f = 0.3 * (1-abs((scipy.stats.norm(0,0.341**2).cdf(attractiveness_a-attractiveness_b)-.5)*2))
       
        # Age difference:
        # The score of the male is increased by .3 * a value between 0 and 1, maximised when the age_b (female) minus
        # age_a (male) is as close to -3.996 as possible.
        score_m =+ .3 * (1-abs((scipy.stats.norm(-3.996,3.31662**2).cdf(age_b-age_a)-.5)*2))
        # The score of the female is increased by .4 * a value between 0 and 1, maximised when the age_a (male) minus
        # age_b (female) is as close to 2.0464 as possible.
        score_f =+ .3 * (1-abs((scipy.stats.norm(2.0464,2.90659**2).cdf(age_a-age_b)-.5)*2))
       
       
        # add edge for female
        # node_a -> node_b with female score
        like_a = score_f
        like_b = score_m
       
   
   
    list_score_m.append(score_m)
    list_score_f.append(score_f)
    
    return origin_network, like_a, like_b, list_score_m, list_score_f


###############################################################################################################################################
def search(cost,node_a, gender_a, age_a,coins_a,
           attractiveness_a,ethnicity_a,
           attractiveness, ethnicity, gender,age,
           origin_network,runs,i,list_score_m,list_score_f,
           male_list, female_list, age_range,like_record, dislike_record,
           female_like_count, male_like_count):
    """
    this function will allow the agent to search someone up
    """
    
    
    # look at 10 people each time you browse
    
        
    if gender_a == "Male":
        node_b = potential_swipe_for_male(node_a, gender_a, age_a,male_list, female_list, origin_network, age_range,like_record,
                                              dislike_record)
        gender_b, age_b,attractiveness_b,ethnicity_b =  gender[node_b],age[node_b],attractiveness[node_b],ethnicity[node_b]
            
        origin_network, like_a, like_b, list_score_m, list_score_f = match_power(node_a,gender_a,
                                                                                age_a,attractiveness_a,ethnicity_a,
                                                                                node_b,gender_b, age_b,
                                                                                attractiveness_b,ethnicity_b,
                                                                                origin_network,runs,i,list_score_m,list_score_f)
        if like_a > 0.7:
            if random.random() <= 0.8:
                male_like_count += 1
                # add a liking edge for node_a to node_b
                #print("node {} (gender {}) liked node {} (gender{})".format(node_a,gender_a,node_b,gender_b))
                origin_network.add_edge(node_a, node_b, Time=runs + 1, Type="random_edge", 
                                        time_order = i, message = 0, like = 1, like_message = 0, dislike = 0, match = 0,match_power = like_a)
                like_record.append([node_a,node_b])
                coins_a -= cost

        
    else:
        node_b = df1.potential_swipe(node_a, 
                    gender_a, age_a,
                    male_list, female_list, 
                    origin_network, age_range,
                   like_record, dislike_record)
        gender_b, age_b,attractiveness_b,ethnicity_b = gender[node_b],age[node_b],attractiveness[node_b],ethnicity[node_b]
           
        origin_network, like_a, like_b, list_score_m, list_score_f = match_power(node_a,gender_a,age_a,attractiveness_a,ethnicity_a,
                                                                                node_b,gender_b, age_b,attractiveness_b,ethnicity_b,
                                                                                origin_network,runs,i,list_score_m,list_score_f)
        if like_a > 0.8:
            if random.random() <= 0.8:
                female_like_count += 1
                # add a liking edge for node_a to node_b
                #print("node {} (gender {}) liked node {} (gender{})".format(node_a,gender_a,node_b,gender_b))
                origin_network.add_edge(node_a, node_b, Time=runs + 1, Type="random_edge", 
                                        time_order = i, message = 0, like = 1, like_message = 0, dislike = 0, match = 0,match_power = like_a)
                like_record.append([node_a,node_b])
                coins_a -= cost
                

    return coins_a,like_record, node_b, gender_b, age_b,attractiveness_b,ethnicity_b, origin_network, female_like_count, male_like_count, like_a, like_b, list_score_m, list_score_f

###############################################################################################################################################


###############################################################################################################################################

def Match(node_a,node_b,gender_a, age_a, age_b,attractiveness_a,attractiveness_b,origin_network,match_records, runs, i, match):
    """
    Function: Match
    
    description:
    this function matches two individuals based on whether they have already liked each other,
    the liking has to be mutual.
    """
    


    # add adge for male
    # node_a -> node_b with male score
    origin_network.add_edge(node_a, node_b, 
                        Time=runs + 1, 
                        Type="random_edge", 
                        time_order = i, 
                        message = 0, 
                        like = origin_network[node_a][node_b]["like"], 
                        dislike = origin_network[node_a][node_b]["dislike"], 
                        match = 1,match_power = origin_network[node_a][node_b]["match_power"])
    origin_network.add_edge(node_b, node_a, 
                        Time=runs + 1, 
                        Type="random_edge", 
                        time_order = i, 
                        message = 0, 
                        like = origin_network[node_b][node_a]["like"], 
                        dislike = origin_network[node_b][node_a]["dislike"], 
                        match = 1,match_power = origin_network[node_b][node_a]["match_power"])

    
    
    match_records.append([node_a,node_b])
    match_records.append([node_b,node_a])
    match += 1
    return origin_network, match_records, match

###############################################################################################################################################

def Action2(node_a, coins_a,cost, 
            node_b, gender_a, gender_b, 
            like_a, like_b, attractiveness_a,
            attractiveness_b,origin_network,
            like_record,dislike_record,mess_like_record, 
            runs,i,male_like_count,female_like_count,male_like_w_message_count,female_like_w_message_count,
            prob_m_likes,prob_f_likes,dislikes):
    
    """
    Function: Action
    
    this function uses the like scores from the node attempting to like
    to establish a connection via like. The like score influences who can 
    match with who. Males are less picky than females, so they like more often
    than females do. 
    """
    # if this person already liked me, the chances of me liking them back is higher
    # [highly attracted, difference between this one and the last one: liklihood of a like with a message, 
    #  not very attracted, difference between this one and the third one: liklihood of a like with a message]
    
    # commented out because it is already defined
    #prob_m_likes = [0.6,0.8,0.05,0.1]
    #prob_f_likes = [0.6,0.8,0.03,0.06]
    if (([node_b, node_a] in like_record) and (([node_b, node_a] not in mess_like_record))):
        prob_m_likes[0] = prob_m_likes[0] + 0.05
        prob_m_likes[1] = prob_m_likes[1] + 0.05
        prob_m_likes[2] = prob_m_likes[2] + 0.05
        prob_m_likes[3] = prob_m_likes[3] + 0.05 
        prob_f_likes[0] = prob_f_likes[0] + 0.05
        prob_f_likes[1] = prob_f_likes[1] + 0.05
        prob_f_likes[2] = prob_f_likes[2] + 0.05
        prob_f_likes[3] = prob_f_likes[3] + 0.05 
    elif ([node_b, node_a] in mess_like_record): # check if node b already liked node a with a message. If so increase the probability of liking them back even more. 
        prob_m_likes[0] = prob_m_likes[0] + 0.07
        prob_m_likes[1] = prob_m_likes[1] + 0.07
        prob_m_likes[2] = prob_m_likes[2] + 0.07
        prob_m_likes[3] = prob_m_likes[3] + 0.07                                      
        prob_f_likes[0] = prob_f_likes[0] + 0.07
        prob_f_likes[1] = prob_f_likes[1] + 0.07
        prob_f_likes[2] = prob_f_likes[2] + 0.07
        prob_f_likes[3] = prob_f_likes[3] + 0.07
                                            
    
    # different genders have different probabilities
    if gender_a == "Male":
        # the individual is greater than 50% for like score 
        a = random.random()
        if like_a > 0.5:
            
            if a <= prob_m_likes[0]:
                # add a liking edge for node_a to node_b
#                 print("node {} (gender {}) liked node {} (gender{})".format(node_a,gender_a,node_b,gender_b))
                origin_network.add_edge(node_a, node_b, Time=runs + 1, Type="random_edge", 
                                        time_order = i, message = 0, like = 1, like_message = 0, dislike = 0, match = 0,match_power = like_a)
                male_like_count += 1
                like_record.append([node_a,node_b])
            elif (prob_m_likes[0] < a <= prob_m_likes[1]) and (coins_a >= cost):  # add like with a message
#                 print("node {} (gender {}) liked with message node {} (gender{})".format(node_a,gender_a,node_b,gender_b))
                origin_network.add_edge(node_a, node_b, Time=runs + 1, Type="random_edge", 
                                        time_order = i, message = 0, like = 0, like_message = 1, dislike = 0, match = 0,match_power = like_a)
                #male_like_count += 1
                male_like_w_message_count += 1
                mess_like_record.append([node_a,node_b])
                coins_a -= cost
                like_record.append([node_a,node_b])
                
            else: # male dislikes female
                origin_network.add_edge(node_a, node_b, Time=runs + 1, Type="random_edge", 
                                        time_order = i, message = 0, like = 0, like_message = 0, dislike = 1, match = 0,match_power = like_a)
                dislike_record.append([node_a,node_b])
                dislikes += 1
        else: # the individual is less than 50% for like score

            if (a <= prob_m_likes[2]) and (coins_a >= cost):
#                 print("node {} (gender {}) liked with message node {} (gender{})".format(node_a,gender_a,node_b,gender_b))
                # add a liking edge for node_a to node_b with message
                origin_network.add_edge(node_a, node_b, Time=runs + 1, Type="random_edge", 
                                        time_order = i, message = 0, like = 0, like_message = 1, dislike = 0, match = 0,match_power = like_a)
                #male_like_count += 1
                male_like_w_message_count += 1
                mess_like_record.append([node_a,node_b])
                coins_a -= cost
                like_record.append([node_a,node_b])
            elif prob_m_likes[2] < a <= prob_m_likes[3]:  # add like with a message
#                 print("node {} (gender {}) liked node {} (gender{})".format(node_a,gender_a,node_b,gender_b))
                # add a liking edge for node_a to node_b
                origin_network.add_edge(node_a, node_b, Time=runs + 1, Type="random_edge", 
                                        time_order = i, message = 0, like = 1, like_message = 0, dislike = 0, match = 0,match_power = like_a)
                
                male_like_count += 1
                like_record.append([node_a,node_b])
            
            
            else: # male dislikes female
                origin_network.add_edge(node_a, node_b, Time=runs + 1, Type="random_edge", 
                                        time_order = i, message = 0, like = 0, like_message = 0, dislike = 1, match = 0,match_power = like_a)
                dislike_record.append([node_a,node_b])
                dislikes += 1
                
    else: # node_a is a female
        b = random.random()
        if like_a > 0.6:
            if b <= prob_f_likes[0]:
#                 print("node {} (gender {}) liked node {} (gender{})".format(node_a,gender_a,node_b,gender_b))
                # add a liking edge for node_a to node_b
                origin_network.add_edge(node_a, node_b, Time=runs + 1, Type="random_edge", 
                                        time_order = i, message = 0, like = 1, like_message = 0, dislike = 0, match = 0,match_power = like_a)
                female_like_count += 1
                like_record.append([node_a,node_b])
            
            elif (prob_f_likes[0] < b <= prob_f_likes[1]) and (coins_a >= cost):  # add like with message
#                 print("node {} (gender {}) liked with message node {} (gender{})".format(node_a,gender_a,node_b,gender_b))
                origin_network.add_edge(node_a, node_b, Time=runs + 1, Type="random_edge", 
                                        time_order = i, message = 0, like = 0, like_message = 1, dislike = 0, match = 0,match_power = like_a)
                #female_like_count += 1
                female_like_w_message_count += 1
                mess_like_record.append([node_a,node_b])
                coins_a -= cost
                like_record.append([node_a,node_b])
            
            else: # female dislikes male
                origin_network.add_edge(node_a, node_b, Time=runs + 1, Type="random_edge", 
                                        time_order = i, message = 0, like = 0, like_message = 0, dislike = 1, match = 0,match_power = like_a)
                dislike_record.append([node_a,node_b])
                dislikes += 1
        else: # the individual is less than 50% for like score
            if (b <= prob_f_likes[2]) and (coins_a >= cost):
#                 print("node {} (gender {}) liked with message node {} (gender{})".format(node_a,gender_a,node_b,gender_b))
                # add a liking edge for node_a to node_b with message
                origin_network.add_edge(node_a, node_b, Time=runs + 1, Type="random_edge", 
                                        time_order = i, message = 0, like = 0, like_message = 1, dislike = 0, match = 0,match_power = like_a)
                #female_like_count += 1
                female_like_w_message_count += 1
                mess_like_record.append([node_a,node_b])
                coins_a -= cost
                like_record.append([node_a,node_b])
            elif prob_f_likes[2] < b <= prob_f_likes[3]:  # add like 
#                 print("node {} (gender {}) liked node {} (gender{})".format(node_a,gender_a,node_b,gender_b))
                # add a liking edge for node_a to node_b
                origin_network.add_edge(node_a, node_b, Time=runs + 1, Type="random_edge", 
                                        time_order = i, message = 0, like = 1, like_message = 0, dislike = 0, match = 0,match_power = like_a)
                female_like_count += 1
                like_record.append([node_a,node_b])

            
            else: # male dislikes female
                origin_network.add_edge(node_a, node_b, Time=runs + 1, Type="random_edge", 
                                        time_order = i, message = 0, like = 0, like_message = 0, dislike = 1, match = 0,match_power = like_a)
                dislikes += 1
                dislike_record.append([node_a,node_b])
                
                
    return origin_network, like_record, dislike_record, mess_like_record,male_like_count,male_like_w_message_count,female_like_w_message_count, female_like_count,coins_a,dislikes

###############################################################################################################################################
def message(origin_network,match,list_score_m,list_score_f,runs,i,match_records,gender,age,attractiveness):
    
    """
    Function: message
    
    this function allows two nodes to message each other based on their like score.
    the probabilities also differ for males and females.
    
    
    """
    
    # receive percentile to so that we can tell who the top matches are that will message
    p_low_m = np.percentile(np.asarray(list_score_m), 33)
    p_high_m = np.percentile(np.asarray(list_score_m), 66)

    p_low_f = np.percentile(np.asarray(list_score_f), 33)
    p_high_f = np.percentile(np.asarray(list_score_f), 66)
    
    # creating a message list to see if individual nodes have messaged each other
    message_list = list(["a","b"])
    
    # get the like scores
    match_power = nx.get_edge_attributes(origin_network,'match_power')
    male_messaging_prob = 0.206
    female_messaging_prob = 0.251                                    

    message_count = 0
    for j in range(match*3):
        # grabbing a match pair
        
        match_pair = random.choice(match_records)#random.shuffle(random.choice(match_records))

        # randomize the messenger and the receiver
        np.random.shuffle(np.array(match_pair))

        #print(match_pair)
        # checking to see if the either match has messaged each other
        # 73% of men initiate messages, and 27% of women initiate messages
        if ((match_pair not in message_list) and ([match_pair[1],match_pair[0]] not in message_list)):
            # initial_messages
            # picking two nodes
            node_a = match_pair[0]
            node_b = match_pair[1]
            # getting the gender 
            gender_a = gender[node_a]
            gender_b  = gender[node_b]

            # test if the person is male or female, and then giving them the probability for the
            # first message based on if they are male or female
            # males have a higher % chance to send the first message
            if gender_a == "male":
                if random.random() < 0.73:
                    messenger = node_a
                    receiver = node_b
                else:
                    receiver = node_a
                    messenger = node_b
            else: # node_a’s gender is female
                if random.random() < 0.27: # prob that the female will message
                    messenger = node_a
                    receiver = node_b
                else:
                    receiver = node_a
                    messenger = node_b
            # assumption: prob of initial message = prob of response message by 


        else: # they have already messaged each other
            messenger = match_pair[0]
            receiver = match_pair[1]
        gender_messenger = gender[messenger]
        gender_receiver = gender[receiver]
        gender_receiver = gender[receiver]
        ls_messenger = match_power[messenger,receiver]
        ls_receiver = match_power[receiver,messenger]

        if gender_receiver == "Male":
            if ls_messenger < p_low_m:
                prob = male_messaging_prob - 0.1
            elif p_low_m <= ls_messenger <= p_high_m:
                prob = male_messaging_prob
            else:
                prob = male_messaging_prob + 0.1
            if random.random() < prob:
                # adding one to the message for everytime they message each other
                origin_network.add_edge(messenger, receiver,
                                        Time=runs + 1, Type="random_edge", 
                                        time_order = i, 
                                        message = origin_network[messenger][receiver]["message"] + 1, 
                                        like = origin_network[messenger][receiver]["like"], 
                                        dislike = origin_network[messenger][receiver]["dislike"], 
                                        match = origin_network[messenger][receiver]["match"],
                                        match_power = origin_network[messenger][receiver]["match_power"])
                message_count += 1
        else: # gender_receiver =="Female":
            if ls_messenger < p_low_f:
                prob = female_messaging_prob - 0.1
            elif p_low_m <= ls_messenger <= p_high_f:
                prob = female_messaging_prob
            else:
                prob = female_messaging_prob + 0.1
            if random.random() < prob:
                origin_network.add_edge(messenger, receiver, 
                                        Time=runs + 1, Type="random_edge", 
                                        time_order = i, 
                                        message = origin_network[messenger][receiver]["message"] + 1, 
                                        like = origin_network[messenger][receiver]["like"], 
                                        dislike = origin_network[messenger][receiver]["dislike"], 
                                        match = origin_network[messenger][receiver]["match"],
                                        match_power = origin_network[messenger][receiver]["match_power"])
                message_count += 1
    return origin_network, message_count, message_list
###############################################################################################################################################
