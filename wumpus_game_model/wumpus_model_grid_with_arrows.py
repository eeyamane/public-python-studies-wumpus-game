import random
import json
import traceback
from .wumpus_model_basic import Place, WumpusWorld, Adventurer, Treasure, Wumpus, Bat, Pit, GameState
from .wumpus_model_simple_grid import GridedPlace, SimpleGridRandomWumpusWorld, SimpleGridRandomGameEngine


class GridWithArrowsWumpusWorld(SimpleGridRandomWumpusWorld):
    def __init__(self, filename, width = 8, height = 5, wumpus_qty = 1, bats_qty = 1, pits_qty = 2):
        self._filename = filename

        #if there's not a file, create a new random world
        if (filename == None):
            super().__init__(width, height, wumpus_qty, bats_qty, pits_qty)
        
        else:
            try:
                with open(filename, 'r') as f: 
                    json_world = json.load(f)

                    version = json_world['version']
                    if (version != 'v-f-2'):
                        print('File version not supported. Creating a new random world.')
                        super().__init__()
                    else:
                        self.__init_from_file(json_world)
            except IOError as e: 
                print('Error opening file ' + filename, e)
                raise e


    def __init_from_file(self, json_world):
        self._x = json_world['width']
        self._y = json_world['height']
        self._places = []
        self._places_visited = []
        self._init_grid(self._x, self._y)

        #connects places based in x, y, forming a grid
        self._connect_places_in_grid(self._x, self._y)

        for elem in json_world['elements']:
            symb = elem['symbol']
            x = elem['x']
            y = elem['y']
            place = self._places[x][y]
            if symb == 'A':
                arrows = elem['arrows']
                self.add_element(x, y, self._create_element_from_symbol(symb, place, arrows))
            else:
                self.add_element(x, y, self._create_element_from_symbol(symb, place, 0))

        for visited in json_world['places_visited']:
            x = visited['x']
            y = visited['y']
            self._places_visited[x][y] = True


    def _create_element_from_symbol(self, symbol, place, arrows):
        if symbol == 'A':
            self._adventurer = Adventurer(place)
            self._adventurer.set_qty_arrows(arrows)
            return self._adventurer
        elif symbol == 'W':
            return Wumpus(place)
        elif symbol == 'B':
            return Bat(place)
        elif symbol == 'P':
            return Pit(place)
        elif symbol == 'T':
            return Treasure(place)
        else:
            return None

    
    def save_to_file(self, filename):
        dict_json = self.__generate_dict_with_elements_to_json()
        dict_json = self.__generate_dict_with_visited_places_to_json(dict_json)
        dict_json['version'] = 'v-f-2'
        dict_json['width'] = self._x
        dict_json['height'] = self._y
        json_object = json.dumps(dict_json)
        try:
            f = open(filename, 'w')
            f.write(json_object)
            f.close()
        except IOError as e:
            print('Error saving file ' + filename, e)
            traceback.print_exc()


    def __generate_dict_with_elements_to_json(self):
        dict_json = dict()
        dict_json['places_visited'] = list()
        dict_json['elements'] = list()
        
        for x in range(self._x):
            for y in range(self._y):
                elements = self._places[x][y].get_elements()
                for elem in elements:
                    if isinstance(elem, Adventurer):
                        dict_json['elements'].append({'symbol': elem.get_symbol(), 'x': x, 'y': y, 'arrows': elem.get_qty_arrows()})
                    else:
                        dict_json['elements'].append({'symbol': elem.get_symbol(), 'x': x, 'y': y})

        return dict_json


    def __generate_dict_with_visited_places_to_json(self, dict_json):
        dict_json['places_visited'] = list()
        
        for x in range(self._x):
            for y in range(self._y):
                if self._places_visited[x][y] == True:
                    dict_json['places_visited'].append({'x': x, 'y': y})

        return dict_json


class GridWithArrowsGameEngine(SimpleGridRandomGameEngine):
    def __init__(self, filename):
        self._filename = filename
        if (filename == None):
            print('You can load a file with a world previously created.')
            answer = input('If you want to load a file, type its name: \n')
            if answer == None or answer == '':
                self._filename = None
            else: 
                self._filename = answer
        
        try:
            self._world = GridWithArrowsWumpusWorld(self._filename)
            self._game_state = GameState.START
        except Exception as e:
            print('Error creating world.', e)
            raise e


    def _print_possible_shoots(self):
        valid_shoots = list()
        if self._world.get_adventurer().get_qty_arrows() > 0:
            adv_place = self._world.get_adventurer().is_on_place
            #up
            if adv_place.y < self._world.get_world_height()-1:
                print('[SU] Shoot Up')
                valid_shoots.append('SU')
            #down
            if adv_place.y > 0:
                print('[SD] Shoot Dow')
                valid_shoots.append('SD')
            #left
            if adv_place.x > 0:
                print('[SL] Shoot Left')
                valid_shoots.append('SL')
            #right
            if adv_place.x < self._world.get_world_width()-1:
                print('[SR] Shoot Right')
                valid_shoots.append('SR')
        else:
            print('(You have no more arrows to shoot.)')
        return valid_shoots


    def _print_possible_moves(self):
        adv_place = self._world.get_adventurer().is_on_place
        valid_moves = list()
        #up
        if adv_place.y < self._world.get_world_height()-1:
            print('[MU] Move Up')
            valid_moves.append('MU')
        #down
        if adv_place.y > 0:
            print('[MD] Move Down')
            valid_moves.append('MD')
        #left
        if adv_place.x > 0:
            print('[ML] Move Left')
            valid_moves.append('ML')
        #right
        if adv_place.x < self._world.get_world_width()-1:
            print('[MR] Move Right')
            valid_moves.append('MR') 
        return valid_moves


    def _present_options_to_user(self):
        print('You can: ')
        options_available = self._print_possible_moves()
        options_available.extend(self._print_possible_shoots())
        print('[S] Save game and exit... ')
        answer = input('So, what do you want to do ? \n').upper()
        if answer == 'S':
            answer = input('Enter filename: \n')
            self._world.save_to_file(answer)
            self._game_state = GameState.END_BUT_NOT_GAME_OVER
            print('Goodbye, see you soon.')
        elif answer in options_available:
            action_type = answer[0:1]
            if (action_type == 'M'):
                self._move_adventurer(answer[1:])
            else:
                self._adventurer_shoots(answer[1:])
            self._game_state = GameState.EVALUATE_GAME_STATE
        else:
            print('Invalid option')
            self._present_options_to_user()


    def _move_adventurer(self, direction):
        adventurer = self._world.get_adventurer()
        adv_place = adventurer.is_on_place
        if direction == 'U': 
            x = adv_place.x
            y = adv_place.y + 1
        elif direction == 'D':
            x = adv_place.x
            y = adv_place.y - 1
        elif direction == 'L':
            x = adv_place.x - 1
            y = adv_place.y
        elif direction == 'R':
            x = adv_place.x + 1
            y = adv_place.y

        self._world.remove_element(adventurer.is_on_place.x, adventurer.is_on_place.y, adventurer)
        self._world.add_element(x, y, adventurer)


    def _adventurer_shoots(self, direction):
        adventurer = self._world.get_adventurer()
        adv_place = adventurer.is_on_place

        #return coordinates of two places the arrow can reach (the second can be unreacheable, so -1, -1 in this case)
        x1 = -1
        y1 = -1
        if direction == 'U': 
            x = adv_place.x
            y = adv_place.y + 1
            if y < self._world.get_world_height() - 1:
                x1 = x
                y1 = y + 1
        elif direction == 'D':
            x = adv_place.x
            y = adv_place.y - 1
            if y > 0:
                x1 = x
                y1 = y - 1
        elif direction == 'L':
            x = adv_place.x - 1
            y = adv_place.y
            if x > 0:
                x1 = x - 1
                y1 = y
        elif direction == 'R':
            x = adv_place.x + 1
            y = adv_place.y
            if y < self._world.get_world_width() - 1:
                x1 = x + 1
                y1 = y

        self._check_arrow_shoot(x, y, x1, y1)


    def _check_arrow_shoot(self, x, y, x1, y1):
        res = self._check_arrow_shoot_at_place(x, y)
        if res == 'miss' and x1 >= 0 and y1 >= 0:
            res = self._check_arrow_shoot_at_place(x1, y1)

        if (res == 'miss'):
            print('Your arrow hits nothing')

    def _check_arrow_shoot_at_place(self, x, y):
        elements = self._world.get_elements(x, y)
        for elem in elements:
            if isinstance(elem, Wumpus):
                print('You hear a terrible scream of pain. Your arrow hit the Wumpus!')
                print('Wumpus is dead.')
                self._world.remove_element(x, y, elem)
                return 'hit'
        return 'miss'


    def game_loop(self):
        while True:
            match self._game_state:
                case GameState.START:
                    self._state_started()
                case GameState.EVALUATE_GAME_STATE:
                    self._world.print_visited_world()
                    self._state_evaluate_update_to_user()
                case GameState.UPDATE_TO_USER:
                    self._present_options_to_user()
                case GameState.WAIT_USER_ACTION:
                    self._wait_user_action()
                case GameState.END:
                    self._end_game()
                    return
                case GameState.END_BUT_NOT_GAME_OVER:
                    self._world.print_full_world()
                    return
        
