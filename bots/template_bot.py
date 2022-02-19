import sys

import random

from src.player import *
from src.structure import *
from src.game_constants import GameConstants as GC

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
        dist = [[sys.maxint for i in range(self.MAP_WIDTH)] for j in range(self.MAP_HEIGHT)]
        # run through the grid the see which nodes are the homies 
        for x in range(self.MAP_WIDTH): 
            for y in range(self.MAP_HEIGHT): 
                st = map[x][y].structure 
                if st is not None: 
                    if st.team == player_info.team: 
                        dist[x][y] = 0
                        my_structs.append(st)

        # run multisourced dijkstra (consider doing every turn to rerank)

        print(nodes)
        if(turn_num > 1): 
            assert(1 == 2)
        return
