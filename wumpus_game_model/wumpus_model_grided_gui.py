import random
import json
import traceback
from .wumpus_model_basic import Place, WumpusWorld, Adventurer, Treasure, Wumpus, Bat, Pit, GameState

class GridedPlace(Place):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

    def get_coords_print_version(self):
        return '(' + str(self.x+1) + ', ' + str(self.y+1) + ')'



class GridedGUIWumpusWorld(WumpusWorld):
    def __init__(self, filename, width = 8, height = 5, wumpus_qty = 1, bats_qty = 1, pits_qty = 2):
        self._filename = filename

        #if there's not a file, create a new random world
        if (filename == None):
            self.__init_random(width, height, wumpus_qty, bats_qty, pits_qty)
        
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


    def __init_random(self, width = 8, height = 5, wumpus_qty = 1, bats_qty = 1, pits_qty = 2):
        self._x = width
        self._y = height
        self._places = []
        self._places_visited = []
        self._init_grid(width, height)

        #connects places based in x, y, forming a grid
        self._connect_places_in_grid(width, height)

        self._wumpus_qty = wumpus_qty
        self._bats_qty = bats_qty
        self._pits_qty = pits_qty
        self._wumpus = set()
        self._pits = set()
        self._bats = set()
        self._treasure = None

        self._adventurer = Adventurer(self._places[0][0])
        self.add_element(0, 0, self._adventurer)
        self._places_visited[0][0] = True
        
        #ramdomly places wumpus, bats, pits, etc
        #a place can not contain two of these elements
        while self._treasure == None:
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            if len(self.get_elements(x, y)) == 0:
                self._treasure = Treasure(self._places[x][y])
                self.add_element(x, y, self._treasure)

        i = 0
        while i < wumpus_qty:
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            if len(self.get_elements(x, y)) == 0:
                w = Wumpus(self._places[x][y])
                self._wumpus.add(w)
                self.add_element(x, y, w)
                i = i + 1
        i = 0
        while i < bats_qty:
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            if len(self.get_elements(x, y)) == 0:
                self.add_element(x, y, Bat(self._places[x][y]))
                i = i + 1
        i = 0
        while i < pits_qty:
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            if len(self.get_elements(x, y)) == 0:
                self.add_element(x, y, Pit(self._places[x][y]))
                i = i + 1


    def __init_from_file(self, json_world):
        self._x = json_world['width']
        self._y = json_world['height']
        self._places = []
        self._places_visited = []
        self._init_grid(self._x, self._y)

        self._wumpus_qty = 0
        self._bats_qty = 0
        self._pits_qty = 0
        self._wumpus = set()
        self._pits = set()
        self._bats = set()
        self._treasure = None

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


    def _init_grid(self, width, height):
        for x in range(width):
            self._places.append([])
            self._places_visited.append([])
            for y in range(height):
                self._places[x].append(GridedPlace(x, y))
                self._places_visited[x].append(False)


    def is_place_visited(self, x, y):
        return self._places_visited[x][y]


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


    def _connect_places_in_grid(self, width, height):
        for x in range(width):
            for y in range(height):
                place = self._places[x][y]
                if x > 0:
                    place.connected_places.add(self._places[x-1][y])
                if x < width-1:
                    place.connected_places.add(self._places[x+1][y])
                if y > 0:
                    place.connected_places.add(self._places[x][y-1])
                if y < height-1:
                    place.connected_places.add(self._places[x][y+1])

    def get_adventurer(self):
        return self._adventurer

    def add_element(self, x, y, element):
        super().add_element(x, y, element)
        if isinstance(element, Adventurer):
            self._places_visited[x][y] = True            
        elif isinstance(element, Wumpus):
            self._wumpus_qty = self._wumpus_qty + 1
            self._wumpus.add(element)
        elif isinstance(element, Pit):
            self._pits_qty = self._pits_qty + 1
            self._pits.add(element)
        elif isinstance(element, Bat):
            self._bats_qty = self._bats_qty + 1
            self._bats.add(element)
        elif isinstance(element, Treasure):
            self._treasure = element

    def _print_line_full_world(self):
        print('+', end='')
        for x in range(self._x):
            print('---+', end='')
        print('')

    def _print_cell_full_world(self, place):
        characteristics =  place.get_characteristics()
        elements = place.get_elements()
        text = ''
        for ch in characteristics:
            text = text + ch.get_symbol()

        for el in elements:
            text = text + el.get_symbol()
        
        if len(text) == 1:
            text = ' ' + text + ' '
        else:
            while len(text) < 3:
                text = text + ' '

        text = text + '|'
        print(text, end='')

    def _print_cell_visited_world(self, place):
        if self._places_visited[place.x][place.y]:
            self._print_cell_full_world(place)
        else:
            print('   |', end='')


    def _print_caption(self):
        elem_captions = list()
        char_captions = list()

        for x in range(self._x):
            for y in range(self._y):
                place = self._places[x][y]
                for elem in place.get_elements():
                    elem_captions.append(elem.get_symbol() + ': ' + elem.get_name())
                for char in place.get_characteristics():
                    char_captions.append(char.get_symbol() + ': ' + char.get_name())

        print ('Captions: ', end='')
        i = 1
        for text in set(elem_captions + char_captions):
            if i <= 3:
                print(text, end=', ')
                i = i + 1
            else:
                print(text)
                i = 1
            

    def print_full_world(self):
        print('Printing full world...')
        y = self._y - 1
        while y >= 0:
            self._print_line_full_world()

            print('|', end='')
            for x in range(self._x):
                place = self._places[x][y]
                self._print_cell_full_world(place)
            print('')
            y = y - 1

        self._print_line_full_world()
        self._print_caption()


    def print_full_visited_world(self):
        y = self._y - 1
        while y >= 0:
            self._print_line_full_world()

            print('|', end='')
            for x in range(self._x):
                visited = self._places_visited[x][y]
                if visited == True:
                    print(' V |', end='')
                else:
                    print('   |', end='')
            print('')
            y = y - 1

        self._print_line_full_world()


    def print_visited_world(self):
        y = self._y - 1
        while y >= 0:
            self._print_line_full_world()

            print('|', end='')

            for x in range(self._x):
                place = self._places[x][y]
                self._print_cell_visited_world(place)
            print('')
            y = y - 1

        self._print_line_full_world()


    def get_world_qty_pits(self):
        return self._pits_qty

    def get_world_qty_bats(self):
        return self._bats_qty