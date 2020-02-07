import networkx as nx #This has to be networkx v1.x not 2.x, but small modifications should allow for verion 2.x
import random
import numpy as np
import time
import scipy

# Good
######################################################################################################################################################
def potential_swipe(node_a,
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
           
        #if ((node_a,node_b) not in origin_network.edges()):
        if (([node_a,node_b] not in like_record) and ([node_a,node_b] not in dislike_record)):
            return node_b
       
   
    return False
       
   
   
######################################################################################################################################################



######################################################################################################################################################
def match_power(node_b, node_a, gender_a, age_a, ethnicity_a,physical_attractiveness_a,
               gender_b, age_b, ethnicity_b,physical_attractiveness_b,origin_network,runs,i,list_score_m,list_score_f):
   
    """
   
    firstly, this function will generate a "match_power" based on male
    and female preferences. The two individuals will then be tested
    to see if they will match based on a random number, but the like
    score will highly influnce their probability to like.
   
    ----------------------------------------------------------------
   
    attributes that go into the equation:
   
    Age:
        females prefer older men, and men prefer younger females
       
    Physical_attractiveness:
        males put a higher priority on physical_attractiveness than females do
   
    -----------------------------------------------------------------
   
    similarity between the two people will how they like as well
   
    Age:
        If the two people are within two years, increase the probability to like
   
    Physical_attractiveness:
        If the two people are within 0.2 points in physical_attractiveness, increase
        the proabbility to like
   
   
       
    """
   
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
        score_m = 0.4 * (1-abs((scipy.stats.norm(0,0.341**2).cdf(physical_attractiveness_a-physical_attractiveness_b)-.5)*2))
        score_f = 0.3 * (1-abs((scipy.stats.norm(0,0.341**2).cdf(physical_attractiveness_a-physical_attractiveness_b)-.5)*2))
       
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
        score_m = 0.4 * (1-abs((scipy.stats.norm(0,0.341**2).cdf(physical_attractiveness_a-physical_attractiveness_b)-.5)*2))
        score_f = 0.3 * (1-abs((scipy.stats.norm(0,0.341**2).cdf(physical_attractiveness_a-physical_attractiveness_b)-.5)*2))
       
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
   


#########################################################################################################################################################
def Action(node_a, node_b, gender_a, gender_b, origin_network,like_record,dislike_record,
           runs,i,male_like_count,female_like_count,like_a,like_b,
           high_like_male_prob,low_like_male_prob,high_like_female_prob,low_like_female_prob):
    """
    Function: Action
   
    this function uses the like scores from the node attempting to like
    to establish a connection via like. The like score influences who can
    match with who. Males are less picky than females, so they like more often
    than females do.
    """
   
    # different genders have different probabilities
    if gender_a == "Male":
        # the individual is greater than 50% for like score
        if like_a > 0.3:
            if random.random() <= high_like_male_prob:
                # add a liking edge for node_a to node_b
                #print("node {} (gender {}) liked node {} (gender{})".format(node_a,gender_a,node_b,gender_b))
                origin_network.add_edge(node_a, node_b, Time=runs + 1, Type="random_edge",
                                        time_order = i, message = 0, like = 1, like_message = 0, dislike = 0, match = 0,match_power = like_a)
                male_like_count += 1
                like_record.append([node_a,node_b])
            else: # male dislikes female
                origin_network.add_edge(node_a, node_b, Time=runs + 1, Type="random_edge",
                                        time_order = i, message = 0, like = 0, dislike = 1, match = 0,match_power = like_a)
                dislike_record.append([node_a,node_b])
        else: # the individual is less than 50% for like score
            if random.random() <= low_like_male_prob:
                #print("node {} (gender {}) liked node {} (gender{})".format(node_a,gender_a,node_b,gender_b))
                # add a liking edge for node_a to node_b
                origin_network.add_edge(node_a, node_b, Time=runs + 1, Type="random_edge",
                                        time_order = i, message = 0, like = 1, like_message = 0, dislike = 0, match = 0,match_power = like_a)
                male_like_count += 1
                like_record.append([node_a,node_b])
            else: # male dislikes female
                origin_network.add_edge(node_a, node_b, Time=runs + 1, Type="random_edge",
                                        time_order = i, message = 0, like = 0, dislike = 1, match = 0,match_power = like_a)
                dislike_record.append([node_a,node_b])
               
    else: # node_a is a female
        if like_a > 0.4:
            if random.random() <= high_like_female_prob:
                #print("node {} (gender {}) liked node {} (gender{})".format(node_a,gender_a,node_b,gender_b))
                # add a liking edge for node_a to node_b
                origin_network.add_edge(node_a, node_b, Time=runs + 1, Type="random_edge",
                                        time_order = i, message = 0, like = 1, like_message = 0, dislike = 0, match = 0,match_power = like_a)
                female_like_count += 1
                like_record.append([node_a,node_b])
            else: # female dislikes male
                origin_network.add_edge(node_a, node_b, Time=runs + 1, Type="random_edge",
                                        time_order = i, message = 0, like = 0, dislike = 1, match = 0,match_power = like_a)
                dislike_record.append([node_a,node_b])
        else: # the individual is less than 50% for like score
            if random.random() <= low_like_female_prob:
                #print("node {} (gender {}) liked node {} (gender{})".format(node_a,gender_a,node_b,gender_b))
                # add a liking edge for node_a to node_b
                origin_network.add_edge(node_a, node_b, Time=runs + 1, Type="random_edge",
                                        time_order = i, message = 0, like = 1, like_message = 0, dislike = 0, match = 0,match_power = like_a)
                female_like_count += 1
                like_record.append([node_a,node_b])
            else: # male dislikes female
                origin_network.add_edge(node_a, node_b, Time=runs + 1, Type="random_edge",
                                        time_order = i, message = 0, like = 0, dislike = 1, match = 0,match_power = like_a)
               
                dislike_record.append([node_a,node_b])
               
               
    return origin_network, like_record, dislike_record, male_like_count, female_like_count
##############################################################################################################################################




###################################################################################################

def Match(node_a,node_b,origin_network,match_records, runs, i, match):
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
                        like = 0,
                        dislike = 0,
                        match = 1,match_power = origin_network[node_a][node_b]["match_power"])
    origin_network.add_edge(node_b, node_a,
                        Time=runs + 1,
                        Type="random_edge",
                        time_order = i,
                        message = 0,
                        like = 0,
                        dislike = 0,
                        match = 1,match_power = origin_network[node_b][node_a]["match_power"])

   
   
    match_records.append([node_a,node_b])
    match_records.append([node_b,node_a])
    match += 1
    return origin_network, match_records, match
####################################################################################



######################################################################################################################################################




######################################################################################################################################################
def message(origin_network,match,list_score_m,list_score_f,runs,i,match_records,gender,age,physical_attractiveness):
   
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
                   
            else:    
                if random.random() < 0.27: # gender is female, prob that the female will message
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
                                        like = 0,
                                        dislike = 0,
                                        match = 0,
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
                                        like = 0,
                                        dislike = 0,
                                        match = 0,
                                        match_power = origin_network[messenger][receiver]["match_power"])
                message_count += 1
    return origin_network, message_count, j, message_list
######################################################################################################################################################