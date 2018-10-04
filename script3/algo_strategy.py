import gamelib
import random
import math
import statistics
from sys import maxsize


'''
Most of the algo code you write will be in this file unless you create new
modules yourself. Start by modifying the 'on_turn' function.

Advanced strategy tips:

Additional functions are made available by importing the AdvancedGameState
class from gamelib/advanced.py as a replcement for the regular GameState class
in game.py.

You can analyze action frames by modifying algocore.py.

The GameState.map object can be manually manipulated to create hypothetical
board states. Though, we recommended making a copy of the map to preserve
the actual current map state.
'''

class AlgoStrategy(gamelib.AlgoCore):
    def __init__(self):
        super().__init__()
        random.seed()

    def on_game_start(self, config):
        '''
        Read in config and perform any initial setup here
        '''
        gamelib.debug_write('Configuring your custom algo strategy...')
        self.config = config
        global FILTER, ENCRYPTOR, DESTRUCTOR, PING, EMP, SCRAMBLER
        FILTER = config["unitInformation"][0]["shorthand"]
        ENCRYPTOR = config["unitInformation"][1]["shorthand"]
        DESTRUCTOR = config["unitInformation"][2]["shorthand"]
        PING = config["unitInformation"][3]["shorthand"]
        EMP = config["unitInformation"][4]["shorthand"]
        SCRAMBLER = config["unitInformation"][5]["shorthand"]

    def on_turn(self, cmd):
        '''
        This function is called every turn with the game state wrapper as
        an argument. The wrapper stores the state of the arena and has methods
        for querying its state, allocating your current resources as planned
        unit deployments, and transmitting your intended deployments to the
        game engine.
        '''
        game_state = gamelib.GameState(self.config, cmd)
        gamelib.debug_write('Performing turn {} of your custom algo strategy'.format(game_state.turn_number))

        self.starter_strategy(game_state)

        game_state.submit_turn()

    '''
    NOTE: All the methods after this point are part of the sample starter-algo
    strategy and can safey be replaced for your custom algo.
    '''
    def starter_strategy(self, game_state):
        '''
        Build the C1 logo. Calling this method first prioritises
        resources to build and repair the logo before spending them
        on anything else.
        '''
        self.build_c1_logo(game_state)

        '''
        Then build additional defenses.
        '''
        self.build_defences(game_state)

        '''
        Finally deploy our information units to attack.
        '''
        self.deploy_attackers(game_state)

    # Here we make the C1 Logo!
    def build_c1_logo(self, game_state):
        '''
        We use Filter firewalls because they are cheap

        First, we build the letter C.
        '''


        tower_locations_filter = [[6, 11], [6, 9], [10, 6], [16, 6], [20, 9], [20, 11]]
        game_state.attempt_spawn(FILTER, tower_locations_filter)
        tower_locations_destruct = [[3, 12], [8, 8], [13, 10], [19, 7], [23, 12]]
        game_state.attempt_spawn(DESTRUCTOR, tower_locations_destruct)
        tower_locations_encrypt = [[13, 5]]
        game_state.attempt_spawn(ENCRYPTOR, tower_locations_encrypt)

        self.prev_starting_bits = game_state.get_resource(game_state.BITS)
        self.prev_enemy_bits = game_state.get_resource(game_state.BITS, 1)
        self.prev_starting_cores = game_state.get_resource(game_state.CORES)
        self.prev_enemy_cores = game_state.get_resource(game_state.CORES, 1)
        self.prev_current_health = game_state.my_health
        self.prev_enemy_health = game_state.enemy_health
        self.prev_health = game_state.enemy_health
        self.prev_all_locations = [[]]

    def build_defences(self, game_state):


        current_health = game_state.my_health

        all_locations = []
        for i in range(game_state.ARENA_SIZE):
            for j in range(math.floor(game_state.ARENA_SIZE / 2)):
                if (game_state.game_map.in_arena_bounds([i, j])):
                    all_locations.append([i, j])

        '''
        Then we remove locations already occupied.
        '''
        possible_locations = self.filter_blocked_locations(all_locations, game_state)

        destroyed_locations_x = []
        destroyed_locations = [[]]

        '''
        while game_state.get_resource(game_state.CORES) >= 1 and len(possible_locations) > 0:
            if (len(possible_locations)>0):
                weighted_locations = [[]]
                for x in possible_locations:
                    weighted_locations.append(x)
                    for y in range(0,x[1]):
                        weighted_locations.append(x)
                location_index = random.randint(0, len(weighted_locations) - 1)
                build_location = weighted_locations[location_index]
                game_state.attempt_spawn(FILTER, build_location)
                possible_locations.remove(build_location)
                weighted_locations.remove(build_location)

            if ((self.prev_current_health - current_health) > 0):
                if (len(self.prev_all_locations)>0):
                    for x in possible_locations:
                        if x not in self.prev_all_locations:
                            destroyed_locations_x.append(x[0])
                            destroyed_locations.append(x)
                    if statistics.stdev(destroyed_locations_x) < 4:
                        game_state.attempt_spawn(DESTRUCTOR, destroyed_locations_x[0])
                        possible_locations.remove(destroyed_locations[0])
                    else:
                        for x in destroyed_locations:
                            game_state.attempt_spawn(FILTER, x)
                            possible_locations.remove(x)
                else:
                    weighted_locations = [[]]
                    for x in possible_locations:
                        weighted_locations.append(x)
                        for y in range(0, x[1]):
                            weighted_locations.append(x)
                    location_index = random.randint(0, len(weighted_locations) - 1)
                    build_location = weighted_locations[location_index]
                    game_state.attempt_spawn(FILTER, build_location)
                    possible_locations.remove(build_location)
                    weighted_locations.remove(build_location)
            else:
                weighted_locations = [[]]
                for x in possible_locations:
                    weighted_locations.append(x)
                    for y in range(0, x[1]):
                        weighted_locations.append(x)
                location_index = random.randint(0, len(weighted_locations) - 1)
                build_location = weighted_locations[location_index]
                game_state.attempt_spawn(FILTER, build_location)
                possible_locations.remove(build_location)
                weighted_locations.remove(build_location)

        '''

        if ((self.prev_current_health - current_health) > 0):
            if (len(self.prev_all_locations)>0):
                if (len(possible_locations) > len(self.prev_all_locations)):
                    # if there are more available locations then there were
                    for x in possible_locations:
                        if x not in self.prev_all_locations:
                            destroyed_locations_x.append(x[0])
                            destroyed_locations.append(x)


                    if statistics.stdev(destroyed_locations_x) < 4:
                        game_state.attempt_spawn(DESTRUCTOR, destroyed_locations_x[0])
                    else:
                        for x in destroyed_locations:
                            game_state.attempt_spawn(FILTER, x)


        '''
        While we have cores to spend, build a random Encryptor.
        '''
        while game_state.get_resource(game_state.CORES) >= game_state.type_cost(DESTRUCTOR) and len(possible_locations) > 0:
            # Choose a random location.
            weighted_locations = [[]]
            maximum = 0
            for x in possible_locations:
                if (x[1] > maximum):
                    maximum = x[1]
            for x in possible_locations:
                if (x[1] > (maximum - 2)):
                    for i in range(0,10):
                        weighted_locations.append(x)
                elif (x[1] > (maximum - 4)):
                    for i in range(0,5):
                        weighted_locations.append(x)
                else:
                    weighted_locations.append(x)
            location_index = random.randint(0, len(weighted_locations) - 1)
            build_location = weighted_locations[location_index]
            game_state.attempt_spawn(DESTRUCTOR, build_location)
            possible_locations.remove(build_location)
            weighted_locations.remove(build_location)




        self.prev_all_locations = possible_locations

    def deploy_attackers(self, game_state):


        starting_bits = game_state.get_resource(game_state.BITS)
        bits_to_spend = starting_bits
        enemy_bits = game_state.get_resource(game_state.BITS, 1)
        current_health = game_state.my_health
        enemy_health = game_state.enemy_health
        friendly_edges = game_state.game_map.get_edge_locations(game_state.game_map.BOTTOM_LEFT) + game_state.game_map.get_edge_locations(game_state.game_map.BOTTOM_RIGHT)
        deploy_locations = self.filter_blocked_locations(friendly_edges, game_state)

        #While we still want to spend more bits, deploy a random information unit
        while bits_to_spend >= 1 and len(deploy_locations) > 0:
            ping_value = 1
            scrambler_value = 1
            emp_value = 1

            #Stop if values were set below zero
            if ping_value + scrambler_value + emp_value < 1:
                break

            #Choose a random deploy location
            deploy_index = random.randint(0, len(deploy_locations) - 1)
            deploy_location = deploy_locations[deploy_index]

            #Adjust weights slightly based on game state
            if enemy_health <= 5:
                ping_value *= 2

            if enemy_bits > starting_bits or current_health <= 5:
                scrambler_value *= 2
            if bits_to_spend < 3:
                emp_value = 0

            deploy_location = [0,0]
            #Choose a random unit based on weights, higher weights are more likely to be chosen
            if ((self.prev_enemy_bits - enemy_bits) > enemy_bits*.3):
                unit_to_spawn = SCRAMBLER
                deploy_location = deploy_locations[int(len(deploy_locations)/2)]
                bits_to_spend -= 3
            elif ((self.prev_enemy_health - enemy_health) > 0):
                deploy_location = self.prev_deploy_location
                unit_to_spawn = PING
                bits_to_spend -= 1
            elif ((self.prev_enemy_health - enemy_health) == 0 and game_state.turn_number > 2):
                deploy_location = self.prev_deploy_location
                unit_to_spawn = EMP
                bits_to_spend -= 1
            else:
                deploy_index = random.randint(0, len(deploy_locations) - 1)
                deploy_location = deploy_locations[deploy_index]
                unit_to_spawn = PING
                bits_to_spend -= 1
                self.prev_deploy_location = deploy_location


            game_state.attempt_spawn(unit_to_spawn, deploy_location)

        self.prev_starting_bits = game_state.get_resource(game_state.BITS)
        self.prev_enemy_bits = game_state.get_resource(game_state.BITS, 1)
        self.prev_starting_cores = game_state.get_resource(game_state.CORES)
        self.prev_enemy_cores = game_state.get_resource(game_state.CORES, 1)
        self.prev_current_health = game_state.my_health
        self.prev_enemy_health = game_state.enemy_health
        self.prev_health = game_state.my_health


    def filter_blocked_locations(self, locations, game_state):
        filtered = []
        for location in locations:
            if not game_state.contains_stationary_unit(location):
                filtered.append(location)
        return filtered

if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
