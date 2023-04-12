import random
import json
import traceback
from wumpus_model_basic import Place, WumpusWorld, Adventurer, Treasure, Wumpus, Bat, Pit, GameState
from wumpus_model_simple_grid import GridedPlace, SimpleGridRandomWumpusWorld, SimpleGridRandomGameEngine


class SimpleGridRandomWithFileWumpusWorld(SimpleGridRandomWumpusWorld):
    def __init__(self, filename):
        self._filename = filename

        #if there's not a file, create a new random world
        if (filename == None):
            super().__init__()
        
        else:
            try:
                f = open(filename, 'r')
                json_world = json.load(f)

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
                    self.add_element(x, y, self._create_element_from_symbol(symb, place))

                for visited in json_world['places_visited']:
                    x = visited['x']
                    y = visited['y']
                    self._places_visited[x][y] = True

                f.close()
            except IOError as e: 
                print('Error opening file ' + filename, e)
                traceback.print_exc()


    def _create_element_from_symbol(self, symbol, place):
        if symbol == 'A':
            self._adventurer = Adventurer(place)
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
        dict_json = dict()
        dict_json['width'] = self._x
        dict_json['height'] = self._y
        dict_json['elements'] = list()
        dict_json['places_visited'] = list()
        
        for x in range(self._x):
            for y in range(self._y):
                elements = self._places[x][y].get_elements()
                for elem in elements:
                    dict_json['elements'].append({'symbol': elem.get_symbol(), 'x': x, 'y': y})

        for x in range(self._x):
            for y in range(self._y):
                if self._places_visited[x][y] == True:
                    dict_json['places_visited'].append({'x': x, 'y': y})

        json_object = json.dumps(dict_json)
        try:
            f = open(filename, 'w')
            f.write(json_object)
            f.close()
        except IOError as e:
            print('Error saving file ' + filename, e)
            traceback.print_exc()



class SimpleGridRandomWithFileGameEngine(SimpleGridRandomGameEngine):
    def __init__(self, filename):
        self._filename = filename
        if (filename == None):
            print('You can load a file with a world previously created.')
            answer = input('If you want to load a file, type its name: \n')
            if answer == None or answer == '':
                self._filename = None
            else: 
                self._filename = answer
        self._world = SimpleGridRandomWithFileWumpusWorld(self._filename)
        self._game_state = GameState.START


    def _present_options_to_user(self):
        print('You can: ')
        options_numbers, options_places = self._print_possible_moves()
        print('[S] Save game and exit... ')
        answer = input('So, what do you want to do ? \n')
        if answer == 'S':
            answer = input('Enter filename: \n')
            self._world.save_to_file(answer)
            self._game_state = GameState.END_BUT_NOT_GAME_OVER
            print('Goodbye, see you soon.')
        elif answer in options_numbers:
            new_place = options_places[int(answer)-1]
            print('You decide to move to ' + new_place.get_coords_print_version())
            print('You move there and...')
            adventurer = self._world.get_adventurer()
            self._world.remove_element(adventurer.is_on_place.x, adventurer.is_on_place.y, adventurer)
            self._world.add_element(new_place.x, new_place.y, adventurer)
            self._game_state = GameState.EVALUATE_GAME_STATE
        else:
            print('Invalid option')
            self._present_options_to_user()


    def game_loop(self):
        while True:
            match self._game_state:
                case GameState.START:
                    self._state_started()
                case GameState.EVALUATE_GAME_STATE:
                    self._world.print_visited_world()
                    self._world.print_full_world()
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
        
