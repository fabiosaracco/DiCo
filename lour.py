import os
import numpy as np
import random
import datetime as dt
from tqdm import trange, tqdm
import igraph



def update(file_names):
    return '[{0:s}: {1:%H:%M:%S}]'.format(file_names, dt.datetime.now())


def LouR(file_names, g, n,reshuffles, verbose=True):
    #edgelist=[e.tuple for e in g.es]
    #nodelist=sorted(list(set([item for sublist in edgelist for item in sublist])))
    nodelist=list(range(n))
    Loug=g.community_multilevel(return_levels=False)
    edgelist=[g.es[i].tuple for i in range(len(g.es))]
    # Loug is a membership list, i.e. for every element the community it belongs to.
    mod=g.modularity(Loug)
    membership=Loug.membership
    print(update(file_names)+'\tModularity of the original order=%.5f' %(mod))
    for ii in trange(reshuffles):
        #rifrullo=random.sample(list(range(len(nodelist))),len(nodelist))
        rifrullo=list(range(len(nodelist)))
        random.shuffle(rifrullo)
        newedges=[]
        for i in range(len(edgelist)):
            newedges.append((rifrullo[edgelist[i][0]],rifrullo[edgelist[i][1]]))
        gaux=igraph.Graph()
        gaux.add_vertices(nodelist)
        gaux.add_edges(newedges)
        Lougaux=gaux.community_multilevel(return_levels=False)
        if mod<gaux.modularity(Lougaux):
            mod=gaux.modularity(Lougaux)
            membaux=Lougaux.membership
            for i in range(len(membaux)):
                membership[i]=membaux[rifrullo[i]]
            Loug=igraph.VertexClustering(g,membership)
            if verbose:
                tqdm.write(update(file_names)+'\tstep: {0:d}, ({1:.2f}%): Modularity={2:.5f}'.format(ii, 100*(ii+1)/reshuffles, g.modularity(Loug)))
    if not verbose:
        print(update(file_names)+'\tFinal modularity=%.5f' %(mod))
    return Loug

def LouR_w(file_names, g, n,reshuffles):
    nodelist=list(range(n))
    Loug=g.community_multilevel(return_levels=False, weights=g.es['weight'])
    edgelist=[g.es[i].tuple for i in range(len(g.es))]
    weight_dict=dict(zip(edgelist,g.es['weight']))
    mod=g.modularity(Loug)
    membership=Loug.membership
    print(update(file_names)+'\tModularity of the original order=%.5f' %(mod))
    for ii in trange(reshuffles):
        #rifrullo=random.sample(list(range(len(nodelist))),len(nodelist))
        rifrullo=list(range(len(nodelist)))
        random.shuffle(rifrullo)
        
        gaux=igraph.Graph()
        gaux.add_vertices(nodelist)
        for i in range(len(edgelist)):
            gaux.add_edge(source=rifrullo[edgelist[i][0]], target=rifrullo[edgelist[i][1]], weight=weight_dict[edgelist[i]])
        Lougaux=gaux.community_multilevel(return_levels=False, weights=gaux.es['weight'])
        if mod<gaux.modularity(Lougaux):
            mod=gaux.modularity(Lougaux)
            membaux=Lougaux.membership
            for i in range(len(membaux)):
                membership[i]=membaux[rifrullo[i]]
            Loug=igraph.VertexClustering(g,membership)
            print(update(file_names)+'\tstep: {0:d}, ({1:.2f}%): Modularity={2:.5f}'.format(ii, 100*(ii+1)/reshuffles, g.modularity(Loug)))
    return Loug


def reshuffled_Lou(g, n, mod_0, ii):
    nodelist=list(range(n))
    edgelist=[g.es[i].tuple for i in range(len(g.es))]
    # Loug is a membership list, i.e. for every element the community it belongs to.
    
    #rifrullo=random.sample(list(range(len(nodelist))),len(nodelist))
    rifrullo=list(range(len(nodelist)))
    random.shuffle(rifrullo)
    newedges=[]
    for i in range(len(edgelist)):
        newedges.append((rifrullo[edgelist[i][0]],rifrullo[edgelist[i][1]]))
    gaux=igraph.Graph()
    gaux.add_vertices(nodelist)
    gaux.add_edges(newedges)
    Lougaux=gaux.community_multilevel(return_levels=False)
    
    mod=gaux.modularity(Lougaux)
    membaux=Lougaux.membership
    for i in range(len(membaux)):
        membership[i]=membaux[rifrullo[i]]
    if mod_0<mod:
        print('%s\tstep: %d (%s%): Modularity=%.4f' %(time_is_now, counter, str(100*ii/reshuffles).zfill(2), mod))
    return (mod, membership)