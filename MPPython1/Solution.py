
from Traversals import bfs_path
import heapq
from collections import deque
from Simulator import Simulator
import sys

class Solution:

    def __init__(self, problem, isp, graph, info):
        self.problem = problem
        self.isp = isp
        self.graph = graph
        self.info = info



    def bfs(self,graph,isp,end):
        paths = {}

        graph_size = len(graph)
        priors = [-1]*graph_size
        search_queue = deque()
        search_queue.append(isp)
        while search_queue:
            node = search_queue.popleft()
            for neighbor in graph[node]:
                if (priors[neighbor] == -1 and neighbor != isp):
                    priors[neighbor] = node
                    search_queue.append(neighbor)

        path = []
        current_node = end 
        while (current_node != -1):
            path.append(current_node)
            current_node = priors[current_node]
        path = path[::-1]
        paths[end] = path 

        return paths

    def alterantepath(self,n,currentpath):
        toremove = currentpath[len(currentpath)-2]
        self.graph[n].remove(toremove)
        self.graph[toremove].remove(n)
        new_path = self.bfs(self.graph,self.isp,n)
        self.graph[n].append(toremove)
        self.graph[toremove].append(n)
        return new_path

    def allpathsN(self,node):
        start = self.bfs(self.graph,self.isp,node)
        start = start[node]
        newpaths = [start]
        for i in range(10):
            newp = self.alterantepath(node,start)
            if newp[node] not in newpaths:
                newpaths.append(newp[node])
                start = newp[node]

        return newpaths

    def Dprime(self,n,bfs_paths):
        d_n = bfs_paths[n]
        toremove = d_n[len(d_n)-2] #get the 2nd to last element of the shortest path d(n) 
        self.graph[n].remove(toremove)
        self.graph[toremove].remove(n)
        new_path = self.bfs(self.graph,self.isp,n)
        self.graph[n].append(toremove)
        self.graph[toremove].append(n)
        return new_path

    def subsets(self,n,dn,bfs_paths): #get all paths that contain dn as subset
        sets = {}
        dnset = set(dn)
        for client in self.info["list_clients"]:
            clientset = set(bfs_paths[client])
            if dnset.issubset(clientset) and dn != bfs_paths[client]:
                sets[client] = bfs_paths[client]
        return sets

    def newpaths(self,bfs_paths):
        explored = []
        new = {}
        rho1 = self.info["rho1"]
        rho2 = self.info["rho2"]
        cb = self.info["cost_bandwidth"]
        print(rho1)
        print(rho2)
        print(cb)
        for client in bfs_paths:
            subsets = self.subsets(client,bfs_paths[client],bfs_paths)
            if len(subsets) > 1 and client not in explored:
                payments = [self.info["payments"][c] for c in subsets]
                alphas = [self.info["alphas"][x] for x in subsets]
                bandwidths = [self.info["bandwidths"][y] for y in subsets]

                mpay = min(payments)
                mapay = max(payments)
                malphas = max(alphas)
                minalphas = min(alphas)
                mbetas = max(bandwidths)
                minbetas = min(bandwidths)
                dc = bfs_paths[client]
                if self.info["bandwidths"][client] < len(subsets):
                    if self.info["alphas"][client] > malphas or mpay > self.info["payments"][client]:
                        new[client] = self.Dprime(client,bfs_paths)[client]
                    else:
                        if mapay <= self.info["payments"][client] and self.info["alphas"][client] <= 2:
                            new[client] = dc
                            #new[client] = self.Dprime(client,bfs_paths)[client]
                        else:
                            scopy = []
                            for i in range(self.info["bandwidths"][client], len(subsets)+1):
                                self.info["bandwidths"][client] += 1
                            #self.info["bandwidths"][client] += 75
                            new[client] = dc
                else:
                    if self.info["alphas"][client] > malphas:
                        new[client] = self.Dprime(client,bfs_paths)[client]
                     
                        #new[client] = dc
                    else:
                        #new[client] = dc 
                        new[client] = self.Dprime(client,bfs_paths)[client]
                        


            else:
                if client not in explored:
                    new[client] = bfs_paths[client]
                #new[client] = self.Dprime(client,bfs_paths)[client]

            #for s in subsets:
                #explored.append(s)
                

        return new


    def output_paths(self):
        """
        This method must be filled in by you. You may add other methods and subclasses as you see fit,
        but they must remain within the Solution class.
        """
        packets = self.info["list_clients"]
        output = bfs_path(self.graph,self.isp,self.info["list_clients"])
        print(self.allpathsN(1000))
        k = self.newpaths(output)
        paths, bandwidths, priorities = k, self.info["bandwidths"] , {}



        # Note: You do not need to modify all of the above. For Problem 1, only the paths variable needs to be modified. If you do modify a variable you are not supposed to, you might notice different revenues outputted by the Driver locally since the autograder will ignore the variables not relevant for the problem.
        # WARNING: DO NOT MODIFY THE LINE BELOW, OR BAD THINGS WILL HAPPEN
        return (paths, bandwidths, priorities)


