import json


def get_all_users_info(flat_json_file):
    """
    It gets all the info about users from the orginal jsonl file. It contains all Twitter user's public metrics.
    
    :param flat_json_file: the location of the jsonl file. It should have been flatten (see twarc)
    :type flat_json_file: str
    
    :return user_dict: verified users adjacency list, the keys are the verified users' ids
    :type user_dict: dict
    
    """
    
    user_dict={}
    counter=0

    with open(flat_json_file, 'r') as f:
        line=f.readline()
        while line!='':
            cacca=json.loads(line)
        
            # is it a RT?
            if 'referenced_tweets' in cacca.keys() and cacca['referenced_tweets'][0]['type']=='retweeted':
            
                # the author of the original message
                _source=cacca['referenced_tweets'][0]['author']
                _sid=_source['id']
            
                user_dict[_sid]={}
                user_dict[_sid]['username']=_source['username']
                user_dict[_sid]['name']=_source['name']
                user_dict[_sid]['public_metrics']=_source['public_metrics']
            
                # the retweeter of the message
                _target=cacca['author']
                _tid=_target['id']
            
                user_dict[_tid]={}
                user_dict[_tid]['username']=_target['username']
                user_dict[_tid]['name']=_target['name']
                user_dict[_tid]['public_metrics']=_target['public_metrics']
            
            
                counter+=1
            
                print('{:,}'.format(counter), end='\r')
        
            line=f.readline()
    return user_dict