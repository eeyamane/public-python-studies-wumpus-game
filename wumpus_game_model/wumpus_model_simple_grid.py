import random
from .wumpus_model_basic import Place, WumpusWorld, Adventurer, Treasure, Wumpus, Bat, Pit, GameState

class GridedPlace(Place):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

    def get_coords_print_version(self):
        return '(' + str(self.x+1) + ', ' + str(self.y+1) + ')'


class SimpleGridRandomWumpusWorld(WumpusWorld):
    def __init__(self, width = 8, height = 5, wumpus_qty = 1, bats_qty = 1, pits_qty = 2):
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

    def _init_grid(self, width, height):
        for x in range(width):
            self._places.append([])
            self._places_visited.append([])
            for y in range(height):
                self._places[x].append(GridedPlace(x, y))
                self._places_visited[x].append(False)

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


    def get_adventurer(self):
        return self._adventurer


    def add_element(self, x, y, element):
        super().add_element(x, y, element)
        if isinstance(element, Adventurer):
            self._places_visited[x][y] = True            



class SimpleGridRandomGameEngine:
    def __init__(self, width = 8, height = 5, wumpus_qty = 1, bats_qty = 1, pits_qty = 2):
        self._world = SimpleGridRandomWumpusWorld(width, height, wumpus_qty, bats_qty, pits_qty)
        self._game_state = GameState.START

    def _state_started(self):
        print('Welcome to the dungeon, adventurer. Your goal is to find the treasure and not get killed.')
        print('You can walk around, but beware of Wumpus and bottomless pits.')
        print('You can avoid them sensing some characteristics.')
        print('If there is a Wumpus nearby, you will fell a stink smell.')
        print('If there is a pit nearby, you will find a breeze.')
        print('If you find a bat, it will carry you to a random place.')
        print('')
        self._game_state = GameState.EVALUATE_GAME_STATE


    #presents the characteristics of the place to the user
    def _print_place_characteristics(self, adv_place): 
        str_charac = set()
        for ch in adv_place.get_characteristics():
            gamestat, msg = ch.evaluate()
            str_charac.add(msg)
            if gamestat != GameState.NOT_CHANGED:
                self._game_state = gamestat

        for msg in str_charac:
            print(msg)


    def _state_evaluate_update_to_user(self):
        adventurer = self._world.get_adventurer()
        adv_place = adventurer.is_on_place

        print('You are at the position ' + adv_place.get_coords_print_version())
        self._print_place_characteristics(adv_place)

        #check the adventurer interaction with another element in the same place, if that's the case
        for elem in adv_place.get_elements():
            if elem != adventurer:
                gamestat, msg = adventurer.evaluate_with_other_element(elem)
                print(msg)
                if gamestat != GameState.NOT_CHANGED:
                    self._game_state = gamestat

                #elements with personalized actions
                if gamestat == GameState.UPDATE_GAME_STATE:
                    if isinstance(elem, Bat):
                        self._bat_found()
                        self._game_state = GameState.NOT_CHANGED
                        break

        if (self._game_state == GameState.EVALUATE_GAME_STATE):
            self._game_state = GameState.UPDATE_TO_USER
        if (self._game_state == GameState.NOT_CHANGED):
            self._game_state = GameState.EVALUATE_GAME_STATE
            

    #moves the adventurer to a random place, that must be empty
    def _bat_found(self):
        x = random.randint(0, self._world.get_world_width()-1)
        y = random.randint(0, self._world.get_world_height()-1)
        new_place_elements = self._world.get_elements(x, y)
        if len(new_place_elements) == 0:
            adventurer = self._world.get_adventurer()
            self._world.remove_element(adventurer.is_on_place.x, adventurer.is_on_place.y, adventurer)
            self._world.add_element(x, y, adventurer)
        else:
            self._bat_found()


    def _print_possible_moves(self):
        adv_place = self._world.get_adventurer().is_on_place
        opt_numbers = list()
        opt_places = list()
        i = 1
        for adjacent in adv_place.connected_places:
            print ('[' + str(i) + '] Move to ' + adjacent.get_coords_print_version())
            opt_numbers.append(str(i))
            opt_places.append(adjacent)
            i = i + 1
        return opt_numbers, opt_places


    def _present_options_to_user(self):
        print('You can: ')
        options_numbers, options_places = self._print_possible_moves()
        answer = input('So, what do you want to do ? \n')
        if answer in options_numbers:
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


    def _end_game(self):
        print('Game Over')
        self._world.print_full_world()


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
        
        
