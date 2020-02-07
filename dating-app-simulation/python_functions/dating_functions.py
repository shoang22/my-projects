import networkx as nx #This has to be networkx v1.x not 2.x, but small modifications should allow for verion 2.x
import random
import numpy as np
import time
import scipy


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
def like_score(node_b, node_a, gender_a, age_a, ethnicity_a,attractiveness_a,
               gender_b, age_b, ethnicity_b,attractiveness_b,origin_network,runs,i,list_score_m,list_score_f):
    
    """
    
    firstly, this function will generate a "like_score" based on male
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
    
    # first checking to see if node_a is male
    if gender_a == "Male":
        # increasing probability based on attractiveness
        score_m = 0.4*attractiveness_b
        score_f = 0.3*attractiveness_a
        
#         # increasing probability based on similarity
#         if abs(age_a-age_b) <= 2:
#             # increasing probability based on age similarity
#             score_m += 0.1*1
#             score_f += 0.2*1

        # The score of the male is increased by .3 * a value between 0 and 1, maximised when the age_b (female) minus
        # age_a (male) is as close to -3.996 as possible.
        score_m =+ .3 * (1-abs((scipy.stats.norm(-3.996,3.31662**2).cdf(age_b-age_a)-.5)*2))
        # The score of the female is increased by .4 * a value between 0 and 1, maximised when the age_a (male) minus
        # age_b (female) is as close to 2.0464 as possible.
        score_f =+ .4 * (1-abs((scipy.stats.norm(2.0464,2.90659**2).cdf(age_a-age_b)-.5)*2))


            
        if abs(attractiveness_a-attractiveness_b) <= 0.2:
            # increasing probability based on attractiveness similarity
            score_m += 0.2
            score_f += 0.1
            
#         if (age_a - age_b) > 0: #male older than female
#             # probability increases dramatically when the male is older than the female.
#             score_m += 0.3*1
#             score_f += 0.4*1
        
        like_a = score_m
        like_b = score_f
        #else: # the female is older than the male
            # probability does not increase when the female is older than the male.
            #score_m -= 0.3*0.5
            #score_f -= 0.4*0.5
            
            # add adge for male
            # node_a -> node_b with male score

    else: #female
        score_f = 0.3*attractiveness_a
        score_m = 0.4*attractiveness_b
        
        # The score of the male is increased by .3 * a value between 0 and 1, maximised when the age_b (female) minus
        # age_a (male) is as close to -3.996 as possible.
        score_m =+ .3 * (1-abs((scipy.stats.norm(-3.996,3.31662**2).cdf(age_b-age_a)-.5)*2))
        # The score of the female is increased by .4 * a value between 0 and 1, maximised when the age_a (male) minus
        # age_b (female) is as close to 2.0464 as possible.
        score_f =+ .4 * (1-abs((scipy.stats.norm(2.0464,2.90659**2).cdf(age_a-age_b)-.5)*2))
        
        # similarity of age
#         if abs(age_a-age_b) <= 2:
#             score_f += 0.2*1
#             score_m += 0.1*1
        # similarity of attractiveness
        if abs(attractiveness_a-attractiveness_b) <= 0.2:
            score_f += 0.1
            score_m += 0.2
        #female older than male
#         if (age_a - age_b) > 0:
#             score_f += 0.4*1
#             score_m += 0.3*1
        # the 
        else:
            score_f += 0.4*0.5
            score_m += 0.3*0.5
            
        # add adge for female
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
        if like_a > 0.5:
            if random.random() <= high_like_male_prob: 
                # add a liking edge for node_a to node_b
                #print("node {} (gender {}) liked node {} (gender{})".format(node_a,gender_a,node_b,gender_b))
                origin_network.add_edge(node_a, node_b, Time=runs + 1, Type="random_edge", 
                                        time_order = i, message = 0, like = 1, like_message = 0, dislike = 0, match = 0,like_score = like_a)
                male_like_count += 1
                like_record.append([node_a,node_b])
            else: # male dislikes female
                origin_network.add_edge(node_a, node_b, Time=runs + 1, Type="random_edge", 
                                        time_order = i, message = 0, like = 0, dislike = 1, match = 0,like_score = like_a)
                dislike_record.append([node_a,node_b])
        else: # the individual is less than 50% for like score
            if random.random() <= low_like_male_prob:
                #print("node {} (gender {}) liked node {} (gender{})".format(node_a,gender_a,node_b,gender_b))
                # add a liking edge for node_a to node_b
                origin_network.add_edge(node_a, node_b, Time=runs + 1, Type="random_edge", 
                                        time_order = i, message = 0, like = 1, like_message = 0, dislike = 0, match = 0,like_score = like_a)
                male_like_count += 1
                like_record.append([node_a,node_b])
            else: # male dislikes female
                origin_network.add_edge(node_a, node_b, Time=runs + 1, Type="random_edge", 
                                        time_order = i, message = 0, like = 0, dislike = 1, match = 0,like_score = like_a)
                dislike_record.append([node_a,node_b])
                
    else: # node_a is a female
        if like_a > 0.7:
            if random.random() <= high_like_female_prob:
                #print("node {} (gender {}) liked node {} (gender{})".format(node_a,gender_a,node_b,gender_b))
                # add a liking edge for node_a to node_b
                origin_network.add_edge(node_a, node_b, Time=runs + 1, Type="random_edge", 
                                        time_order = i, message = 0, like = 1, like_message = 0, dislike = 0, match = 0,like_score = like_a)
                female_like_count += 1
                like_record.append([node_a,node_b])
            else: # female dislikes male
                origin_network.add_edge(node_a, node_b, Time=runs + 1, Type="random_edge", 
                                        time_order = i, message = 0, like = 0, dislike = 1, match = 0,like_score = like_a)
                dislike_record.append([node_a,node_b])
        else: # the individual is less than 50% for like score
            if random.random() <= low_like_female_prob:
                #print("node {} (gender {}) liked node {} (gender{})".format(node_a,gender_a,node_b,gender_b))
                # add a liking edge for node_a to node_b
                origin_network.add_edge(node_a, node_b, Time=runs + 1, Type="random_edge", 
                                        time_order = i, message = 0, like = 1, like_message = 0, dislike = 0, match = 0,like_score = like_a)
                female_like_count += 1
                like_record.append([node_a,node_b])
            else: # male dislikes female
                origin_network.add_edge(node_a, node_b, Time=runs + 1, Type="random_edge", 
                                        time_order = i, message = 0, like = 0, dislike = 1, match = 0,like_score = like_a)
                
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
                        match = 1,like_score = origin_network[node_a][node_b]["like_score"])
    origin_network.add_edge(node_b, node_a, 
                        Time=runs + 1, 
                        Type="random_edge", 
                        time_order = i, 
                        message = 0, 
                        like = origin_network[node_b][node_a]["like"], 
                        dislike = origin_network[node_b][node_a]["dislike"], 
                        match = 1,like_score = origin_network[node_b][node_a]["like_score"])

    
    
    match_records.append([node_a,node_b])
    match_records.append([node_b,node_a])
    match += 1
    return origin_network, match_records, match
####################################################################################



################################################...