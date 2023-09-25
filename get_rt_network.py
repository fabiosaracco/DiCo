import json
import numpy as np
from bicm import BipartiteGraph as BG



def get_rt_network(flat_json_file, rt_list2np=True):
    """
    It creates a verified users adjacency list (verified users -> unverified retweeters)
    and the retweet network edge list containing the author of the original tweet, the retweeter and the tweet id.
    
    :param flat_json_file: the location of the jsonl file, using v2 standard. It should have been flatten (see twarc).
    :type flat_json_file: str
    
    :return verified_adj_list: verified users adjacency list, the keys are the verified users' ids
    :type verified_adj_list: dict
    
    :return rt_list: each entry is composed by 3 elements: the user id of the author of the tweet, the user id of the retweeter and the tweet id of the original message (i.e. the retweeted one)
    :type rt_list: list
    
    """
    verified_adj_list={}
    rt_list=[]
    with open(flat_json_file, 'r') as f:
        line=f.readline()
        while line!='':
            cacca=json.loads(line)
        
            # is it a RT?
            if 'referenced_tweets' in cacca.keys() and cacca['referenced_tweets'][0]['type']=='retweeted':
            
                # the author of the original message
                _source=cacca['referenced_tweets'][0]['author']
                _sid=_source['id']
                # the retweeter of the message
                _target=cacca['author']
                _tid=_target['id']
                # the message
                _tweet_id=cacca['id']
            
                # the RT edgelist
                rt_list.append([_sid, _tid, _tweet_id])
                print('{:,}'.format(len(rt_list)), end='\r')
                # is it eligible for the DC bipartite network
                if _source['verified'] and not _target['verified']:
                    if _sid in verified_adj_list.keys():
                        if _tid not in verified_adj_list[_sid]:
                            verified_adj_list[_sid].append(_tid)
                    else:
                        verified_adj_list[_sid]=[_tid]
        
            line=f.readline()
            
    if rt_list2np:
        rt_list_np=np.zeros(len(rt_list), dtype=[('source', 'U200'),('target', 'U200'),('tweet_id', 'U200')])

        rt_list_np['source']=[link[0] for link in rt_list]
        rt_list_np['target']=[link[1] for link in rt_list]
        rt_list_np['tweet_id']=[link[2] for link in rt_list]    
        
        return verified_adj_list, rt_list_np
    else:
        return verified_adj_list, rt_list
            
