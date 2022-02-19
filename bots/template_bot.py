import sys

import random

import time

from src.player import *
from src.structure import *
from src.game_constants import GameConstants as GC

import heapq as hq

class MyPlayer(Player):

    def __init__(self):
        print("Init")
        self.turn = 0

        return

    def play_turn(self, turn_num, map, player_info):
        self.MAP_WIDTH = len(map)
        self.MAP_HEIGHT = len(map[0])
        k = 3
        # consider 1 generator 
        # consider where the generator is 
        # do generators have ids? 
        # can you build cell tower on road?

        # step 1: construct a list of nodes 
        # 0, 0 -> 60, 60 
        # pad grid up to multiples of 5 
        nodes = []
        for a in range(self.MAP_WIDTH // k): 
            for b in range(self.MAP_HEIGHT // k): 
                x = a * k
                y = b * k 
                total_terrain = 0
                total_population = 0
                for i in range(k): 
                    for j in range(k): 
                        total_terrain += map[x + i][y + j].passability 
                        total_population += map[x + i][y + j].population
                nodes.append((x, y, total_terrain, total_population))
        
        my_structs = []
        # step 2: run dijkstra's to get distance to every node 
        
        def valid(x, y):
            return 0 <= x < self.MAP_WIDTH and 0 <= y < self.MAP_HEIGHT and map[x][y].structure is None
        

        goon = time.time()
        dist = [[5000.0*self.MAP_HEIGHT*self.MAP_WIDTH for i in range(self.MAP_HEIGHT)] for j in range(self.MAP_WIDTH)]
        pq = []
        vis = [[False for i in range(self.MAP_HEIGHT)] for j in range(self.MAP_WIDTH)]
        # run through the grid the see which nodes are the homies 
        for x in range(self.MAP_WIDTH): 
            for y in range(self.MAP_HEIGHT): 
                st = map[x][y].structure 
                if st is not None: 
                    if st.team == player_info.team: 
                        dist[x][y] = 0
                        my_structs.append(st)
                        hq.heappush(pq, (0, (x, y)))
        
        while len(pq) > 0:
            _, pos = hq.heappop(pq)
            x, y = pos
            vis[x][y] = True

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = pos[0] + dx, pos[1] + dy
                if valid(nx, ny):
                    w = 10.0 * map[nx][ny].passability
                    if dist[nx][ny] > dist[x][y] + w:
                        dist[nx][ny] = dist[x][y] + w
                        hq.heappush(pq, (dist[nx][ny], (nx, ny)))

        print(time.time() - goon)
        for i in range(self.MAP_WIDTH//10):
            for j in range(self.MAP_HEIGHT//10):
                print(i, j, dist[i][j])
        # run multisourced dijkstra (consider doing every turn to rerank)
        
        print(dist[9][11])
        if(turn_num > 1): 
            assert(1 == 2)
        return
