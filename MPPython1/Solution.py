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

    def test(self,output):
        paths = {}
        clients = self.info["list_clients"]
        for i in clients:
            if self.info["alphas"][i] > 1 and len(output[i]) > 2:
                arr = output[i]
                toremove = arr[len(arr)-2]
                self.graph[i].remove(toremove)
                self.graph[toremove].remove(i)
                new = self.bfs(self.graph,self.isp,i)
                self.graph[i].append(toremove)
                self.graph[toremove].append(i)
                paths[i] = new[i]
            else:
                paths[i] = output[i]
        return paths 

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
        new = {}

        for client in bfs_paths:
            subsets = self.subsets(client,bfs_paths[client],bfs_paths)
            if len(subsets) > 1:
                payments = [self.info["payments"][c] for c in subsets]
                alphas = [self.info["alphas"][x] for x in subsets]
                betas = [self.info["bandwidths"][y] for y in subsets]
                mpay = min(payments)
                mapay = max(payments)
                malphas = max(alphas)
                mbetas = max(betas)
                dc = bfs_paths[client]
                if self.info["alphas"][client] > malphas:
                    new[client] = self.Dprime(client,bfs_paths)[client]
                else:
                    new[client] = dc 
            else:
                new[client] = dc

        return new

    def output_paths(self):
        """
        This method must be filled in by you. You may add other methods and subclasses as you see fit,
        but they must remain within the Solution class.
        """
        packets = self.info["list_clients"]
        output = bfs_path(self.graph,self.isp,self.info["list_clients"])
        
        k = self.newpaths(output)
        paths, bandwidths, priorities = k, {} , {}

        p = packets[6]
        y = self.info["alphas"][p]
        a = self.Dprime(p,output)
        if len(a) > 1 and y > 1:
            print(a)
        else:
            print(a)
            print(y)


        # Note: You do not need to modify all of the above. For Problem 1, only the paths variable needs to be modified. If you do modify a variable you are not supposed to, you might notice different revenues outputted by the Driver locally since the autograder will ignore the variables not relevant for the problem.
        # WARNING: DO NOT MODIFY THE LINE BELOW, OR BAD THINGS WILL HAPPEN
        return (paths, bandwidths, priorities)





