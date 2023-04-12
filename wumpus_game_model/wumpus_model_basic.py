import random
from abc import ABC, abstractmethod
from enum import Enum


class GameState(Enum):
    NOT_CHANGED = 1
    START = 2
    EVALUATE_GAME_STATE = 3
    UPDATE_TO_USER = 4
    WAIT_USER_ACTION = 5
    UPDATE_GAME_STATE = 6
    END = 7
    END_BUT_NOT_GAME_OVER = 8


class Characteristic(ABC):
    @abstractmethod
    def evaluate(self):
        pass

    def get_symbol(self):
        return ' '

    def get_name(self):
        return ' '


class ItStinks(Characteristic):
    def evaluate(self):
        return GameState.NOT_CHANGED, 'It stinks! A Wumpus is around here.'

    def get_symbol(self):
        return '*'

    def get_name(self):
        return 'Stinks'


class GentleBreeze(Characteristic):
    def evaluate(self):
        return GameState.NOT_CHANGED, 'A gentle breeze. A pit is around here.'

    def get_symbol(self):
        return '~'

    def get_name(self):
        return 'Breeze'



class Stoned(Characteristic):
    def evaluate(self):
        return GameState.NOT_CHANGED, 'A stone wall, can not go further. Get back.'

    def get_symbol(self):
        return '#'

    def get_name(self):
        return 'Stoned'

    
class Dead(Characteristic):
    def evaluate(self):
        return GameState.END, 'You are dead'

    def get_symbol(self):
        return '+'

    def get_name(self):
        return 'Death'


characteristic_stinks = ItStinks()
characteristic_breeze = GentleBreeze()
characteristic_wall = Stoned()
characteristic_death = Dead()

ELEMENT_NAME_PIT = 'Pit'
ELEMENT_NAME_WALL = 'Wall'
ELEMENT_NAME_WUMPUS = 'Wumpus'
ELEMENT_NAME_DEAD_WUMPUS = 'DeadWumpus'
ELEMENT_NAME_BAT = 'Bat'
ELEMENT_NAME_ADVENTURER = 'Adventurer'
ELEMENT_NAME_TREASURE = 'Treasure'

class Element(ABC):
    def __init__(self, place):
        self.is_on_place = place
        self.gives_main_characteristics = set()
        self.gives_adjacent_characteristics = set()

    def get_symbol(self):
        return ' '

    def get_name(self):
        return 'Element'


class Pit(Element):
    def __init__(self, place):
        super().__init__(place)
        self.gives_main_characteristics.add(characteristic_death)
        self.gives_adjacent_characteristics.add(characteristic_breeze)

    def get_symbol(self):
        return 'P'

    def get_name(self):
        return ELEMENT_NAME_PIT


class Wall(Element):
    def __init__(self, place):
        super().__init__(place)
        self.gives_main_characteristics.add(characteristic_wall)

    def get_symbol(self):
        return 'S'

    def get_name(self):
        return ELEMENT_NAME_WALL


class Wumpus(Element):
    def __init__(self, place):
        super().__init__(place)
        self.gives_main_characteristics.add(characteristic_death)
        self.gives_adjacent_characteristics.add(characteristic_stinks)

    def get_symbol(self):
        return 'W'

    def get_name(self):
        return ELEMENT_NAME_WUMPUS


class DeadWumpus(Element):
    def __init__(self, place):
        super().__init__(place)
        self.gives_main_characteristics.add(characteristic_stinks)
        self.gives_adjacent_characteristics.add(characteristic_stinks)

    def get_symbol(self):
        return 'D'

    def get_name(self):
        return ELEMENT_NAME_DEAD_WUMPUS


class Bat(Element):
    def __init__(self, place):
        super().__init__(place)

    def get_symbol(self):
        return 'B'

    def get_name(self):
        return ELEMENT_NAME_BAT


class Treasure(Element):
    def __init__(self, place):
        super().__init__(place)

    def get_symbol(self):
        return 'T'

    def get_name(self):
        return ELEMENT_NAME_TREASURE


class Adventurer(Element):
    def __init__(self, place, qty_of_arrows = 2):
        super().__init__(place)
        self._qty_of_arrows = qty_of_arrows

    def get_symbol(self):
        return 'A'
    
    def get_name(self):
        return ELEMENT_NAME_ADVENTURER

    def evaluate_with_other_element(self, other):
        if isinstance(other, Pit):
            return GameState.END, 'You fall into a bottomless pit. Goodbye.'
        if isinstance(other, Wumpus):
            return GameState.END, 'Wumpus attacks you. You do not survive.'
        if isinstance(other, Wall):            
            return GameState.UPDATE_GAME_STATE, 'You hit a wall.'
        if isinstance(other, Bat):            
            return GameState.UPDATE_GAME_STATE, 'A mega bat finds you and moves you around.'
        if isinstance(other, Treasure):            
            return GameState.END, 'You found the treasure. Now you are rich and live happily ever after.'

    def get_qty_arrows(self):
        return self._qty_of_arrows

    def set_qty_arrows(self, arrows):
        self._qty_of_arrows = arrows

    def use_arrow(self):
        self._qty_of_arrows = self._qty_of_arrows - 1


class Place:
    def __init__(self):
        self._characteristics = set()
        self._elements = set()
        self.connected_places = set()

    def add_characteristics(self, charact):
        self._characteristics = self._characteristics.union(charact)

    def clear_characteristics(self):
        self._characteristics.clear()

    def get_characteristics(self):
        return self._characteristics

    def add_element(self, elem):
        self._elements.add(elem)
        elem.is_on_place = self
        self.add_characteristics(elem.gives_main_characteristics)

        for adjacent in self.connected_places:
            adjacent.add_characteristics(elem.gives_adjacent_characteristics)


    def update_characteristics_from_adjacents(self):
        for adjacent_place in self.connected_places:
            for adjacent_element in adjacent_place.get_elements():
                self.add_characteristics(adjacent_element.gives_adjacent_characteristics)


    def remove_element(self, elem):
        self._elements.remove(elem)
        elem.is_on_place = None

        # clear all characteristics and sets them back with remaining elements
        self.clear_characteristics()
        for remaining in self._elements:
            self.add_characteristics(remaining.gives_main_characteristics)
        self.update_characteristics_from_adjacents()

        #clear all characteristis from connected places and set them back with characteristics
        #from all its connected places places
        for adjacent_place in self.connected_places:
            adjacent_place.clear_characteristics()
            for adjacent_element in adjacent_place.get_elements():
                adjacent_place.add_characteristics(adjacent_element.gives_main_characteristics)
            adjacent_place.update_characteristics_from_adjacents()

    def get_elements(self):
        return self._elements


class WumpusWorld:
    def __init__(self, width, height):
        self._x = width
        self._y = height
        self._places = []
        
        for x in range(width):
            self._places.append([])
            for y in range(height):
                self._places[x].append(Place())

    def add_element(self, x, y, element):
        place = self._places[x][y]
        place.add_element(element)

    def remove_element(self, x, y, element):
        place = self._places[x][y]
        place.remove_element(element)

    def get_elements(self, x, y):
        place = self._places[x][y]
        return place.get_elements()

    def get_characteristics(self, x, y):
        place = self._places[x][y]
        return place.get_characteristics()

    def get_world_width(self):
        return self._x

    def get_world_height(self):
        return self._y
