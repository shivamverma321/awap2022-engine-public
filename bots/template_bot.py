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
        
        self.cover = [[False for i in range(64)] for j in range(64)]

        return

    def play_turn(self, turn_num, map, player_info):
        self.MAP_WIDTH = len(map)
        self.MAP_HEIGHT = len(map[0])
        k = 1000
        # consider 1 generator 
        # consider where the generator is 
        # do generators have ids? 
        # can you build cell tower on road?

        # step 1: construct a list of nodes 
        # 0, 0 -> 60, 60 
        # pad grid up to multiples of 5 
        # nodes = []
        # for a in range(self.MAP_WIDTH // k): 
        #     for b in range(self.MAP_HEIGHT // k): 
        #         x = a * k
        #         y = b * k 
        #         total_terrain = 0
        #         total_population = 0
        #         for i in range(k): 
        #             for j in range(k): 
        #                 total_terrain += map[x + i][y + j].passability 
        #                 total_population += map[x + i][y + j].population
        #         nodes.append((x, y, total_terrain, total_population))
        
        my_structs = []
        # step 2: run dijkstra's to get distance to every node 
        
        def valid(x, y):
            return 0 <= x < self.MAP_WIDTH and 0 <= y < self.MAP_HEIGHT and map[x][y].structure is None
        

        goon = time.time()
        dist = [[5000.0*self.MAP_HEIGHT*self.MAP_WIDTH for i in range(self.MAP_HEIGHT)] for j in range(self.MAP_WIDTH)]
        pq = []
        vis = [[False for i in range(self.MAP_HEIGHT)] for j in range(self.MAP_WIDTH)]
        
        par = [[(self.MAP_WIDTH // 2, self.MAP_HEIGHT // 2) for i in range(self.MAP_HEIGHT)] for j in range(self.MAP_WIDTH)]

        def setcover(x, y): 
            for dx, dy in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1), (2, 0), (0, 2), (-2, 0), (0, -2)]: 
                nx, ny = dx + x, dy + y 
                if(0 <= nx < self.MAP_WIDTH and 0 <= ny < self.MAP_HEIGHT): 
                    self.cover[nx][ny] = True

        # run through the grid the see which nodes are the homies 
        for x in range(self.MAP_WIDTH): 
            for y in range(self.MAP_HEIGHT): 
                st = map[x][y].structure 
                if st is not None: 
                    if st.team == player_info.team: 
                        dist[x][y] = 0
                        my_structs.append(st)
                        hq.heappush(pq, (0, (x, y)))
                        if(st == StructureType.TOWER): 
                            setcover(x, y)
                        
        
        
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
                        if dist[x][y] != 0:
                            par[nx][ny] = par[x][y]
                        else:
                            par[nx][ny] = (nx, ny)
                        hq.heappush(pq, (dist[nx][ny], (nx, ny)))

        # print(time.time() - goon)
        # for i in range(self.MAP_WIDTH//10):
        #     for j in range(self.MAP_HEIGHT//10):
        #         print(i, j, dist[i][j])
        # run multisourced dijkstra (consider doing every turn to rerank)

        # construct a ranking for each coordinate

        def computecost(x, y): 
            totalpop = 0
            for dx, dy in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1), (2, 0), (0, 2), (-2, 0), (0, -2)]: 
                nx, ny = dx + x, dy + y 
                if(0 <= nx < self.MAP_WIDTH and 0 <= ny < self.MAP_HEIGHT and not self.cover[nx][ny]): 
                    totalpop += map[x][y].population 
            if totalpop == 0:
                return -1e18
            return totalpop * 10 - k * dist[x][y]

        r = []
        for x in range(self.MAP_WIDTH): 
            for y in range(self.MAP_HEIGHT): 
                # compute the population if i were to tower build a tower on this spot
                if(map[x][y].structure is None): 
                    cost = computecost(x, y)
                    hq.heappush(r, (-cost, (x, y)))

        # if(turn_num == 82): 
        #     print("SHIT")
        #     print(self.cover[6][15])
        #     print(self.cover[6][16])
        #     assert(1 == 2)

        if len(r) > 0:
            c, (gx, gy) = hq.heappop(r)
            b = True
            if c > 1e16:
                b = False
            gx, gy = par[gx][gy]
            roads = 0
            max_roads = 5
            towerbuilt = False
            while (player_info.money > 10.0 * map[gx][gy].passability) and (len(r) > 0) and roads < max_roads and b:
                # we know which x, y is the best thing build towards 
                # we are about to build on gx, gy
                # we need to decide to build a road or a tower 
                # claim: if there is any sort of population just build it
                if map[gx][gy].population > 0 and player_info.money > 250.0 * map[gx][gy].passability and (not self.cover[gx][gy]): 
                    self.build(StructureType.TOWER, gx, gy)
                    # setcover(gx, gy)
                elif map[gx][gy].population == 0: 
                    self.build(StructureType.ROAD, gx, gy)
                    roads += 1
                c, (gx, gy) = hq.heappop(r)
                gx, gy = par[gx][gy]
                if c > 1e16:
                    b = False
        


        dist = [[5000.0*self.MAP_HEIGHT*self.MAP_WIDTH for i in range(self.MAP_HEIGHT)] for j in range(self.MAP_WIDTH)]
        pq = []
        vis = [[False for i in range(self.MAP_HEIGHT)] for j in range(self.MAP_WIDTH)]
        par = [[(self.MAP_WIDTH // 2, self.MAP_HEIGHT // 2) for i in range(self.MAP_HEIGHT)] for j in range(self.MAP_WIDTH)]

        closestEnem = 1e18
        bestx, besty = 0, 0
        for x in range(self.MAP_WIDTH): 
            for y in range(self.MAP_HEIGHT): 
                st = map[x][y].structure 
                if st is not None: 
                    if st.team != player_info.team: 
                        if(dist[x][y] < closestEnem): 
                            bestx, besty = par[x][y]
                            closestEnem = dist[x][y]
        
        self.build(StructureType.ROAD, bestx, besty)
        return
