import PySimpleGUI as sg
import json
import traceback
import random
import wumpus_game_model.wumpus_model_grided_gui as wm
import wumpus_game_model.wumpus_model_basic as wb
import random


#icons used:
# <a href="https://www.flaticon.com/free-icons/adventure" title="adventure icons">Adventure icons created by max.icons - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/smell" title="smell icons">Smell icons created by Muhammad Ali - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/bat" title="bat icons">Bat icons created by Freepik - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/hole" title="hole icons">Hole icons created by Freepik - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/monster" title="monster icons">Monster icons created by Freepik - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/treasure" title="treasure icons">Treasure icons created by Freepik - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/wind" title="wind icons">Wind icons created by Freepik - Flaticon</a>

WORLD_WIDTH = 8
WORLD_HEIGHT = 5
WORLD_BATS = 2
WORLD_PITS = 2

WINDOW_NAME = 'Wumpus World Game'

MENU_NEW_RANDOM = 'New Random Game'
MENU_SAVE_FILE = 'Save File'
MENU_OPEN_FILE = 'Open File'
MENU_EXIT = 'Exit Game'
MENU_OPTIONS = 'Game Options'
MENU_ABOUT = 'About'

KEY_MENU = '-MENUBAR-'
IMAGES_DIR = 'wumpus_game_grided_gui/'
IMAGE_SIZE = (65, 65)
GAME_STATE = 0
KEY_ARROW_QTY = '-ARROWS-'

BUTTON_SHOOT = 'Shoot!'
BUTTON_SAVE_OPTION = 'Save and refresh'
BUTTON_CANCEL_OPTION = 'Cancel changes'

KEY_INPUT_WIDTH  = '-WORLD-WIDTH-'
KEY_INPUT_HEIGHT = '-WORLD-HEIGHT-'
KEY_INPUT_BATS = '-WORLD-BATS-'
KEY_INPUT_PITS = '-WORLD-PITS-'

wumpus_world = wm.GridedGUIWumpusWorld(filename=None, width=WORLD_WIDTH, height=WORLD_HEIGHT, bats_qty=WORLD_BATS, pits_qty=WORLD_PITS)
GAME_STATE = wm.GameState.START

#creates a new game world
def create_new_random_world():
    print('Creating new Random World...')
    global wumpus_world, GAME_STATE
    wumpus_world = wm.GridedGUIWumpusWorld(filename=None, width=WORLD_WIDTH, height=WORLD_HEIGHT, bats_qty=WORLD_BATS, pits_qty=WORLD_PITS)
    GAME_STATE = wm.GameState.START
    

sg.theme('Reddit')


def update_game_grid():
    global wumpus_world
    #wumpus_world.print_full_world()
    for i in range(WORLD_WIDTH):
        for j in range(WORLD_HEIGHT):
            elements = wumpus_world.get_elements(i, j)
            characteristics = wumpus_world.get_characteristics(i, j)
            
            if wumpus_world.get_adventurer() in elements:
                update_game_grid_adventurer(i, j, elements, characteristics)
            else:
                if wumpus_world.is_place_visited(i, j):
                    update_game_grid_visited(i, j, elements, characteristics)
                else:
                    update_game_grid_not_visited(i, j)


def update_game_grid_not_visited(i, j):
    window[(i, j)].update(image_filename=IMAGES_DIR+'not_visited.png', image_size=IMAGE_SIZE)


def update_game_grid_visited(i, j, elements, characteristics):
    c_stinks, c_breeze, c_dead =  check_characteristics(characteristics)
    e_adventurer, e_pit, e_wumpus, e_bat, e_treasure, e_deadwumpus = check_elements(elements)

    if e_bat:
        update_game_grid_visited_with_bat(i, j, c_stinks, c_breeze)
    elif e_pit:
        update_game_grid_visited_with_pit(i, j, c_stinks, c_breeze)        
    elif e_wumpus:
        update_game_grid_visited_with_wumpus(i, j, c_breeze)
    elif e_treasure:
        update_game_grid_visited_with_treasure(i, j, c_stinks, c_breeze)
    elif e_deadwumpus:
        update_game_grid_visited_with_deadwumpus(i, j, c_breeze)
    else:
        update_game_grid_visited_no_elements(i, j, c_stinks, c_breeze)


def update_game_grid_visited_no_elements(i, j, c_stinks, c_breeze):
    if c_stinks: 
        if c_breeze:
            window[(i, j)].update(image_filename=IMAGES_DIR+'smell_breeze.png', image_size=IMAGE_SIZE)
        else:
            window[(i, j)].update(image_filename=IMAGES_DIR+'smell.png', image_size=IMAGE_SIZE)
    else:
        if c_breeze:
            window[(i, j)].update(image_filename=IMAGES_DIR+'breeze.png', image_size=IMAGE_SIZE)
        else:
            window[(i, j)].update(image_filename=IMAGES_DIR+'empty.png', image_size=IMAGE_SIZE)



def update_game_grid_visited_with_bat(i, j, c_stinks, c_breeze):
    if c_stinks: 
        if c_breeze:
            window[(i, j)].update(image_filename=IMAGES_DIR+'bat_stinks_breeze.png', image_size=IMAGE_SIZE)
        else:
            window[(i, j)].update(image_filename=IMAGES_DIR+'bat_stinks.png', image_size=IMAGE_SIZE)
    else:
        if c_breeze:
            window[(i, j)].update(image_filename=IMAGES_DIR+'bat_breeze.png', image_size=IMAGE_SIZE)
        else:
            window[(i, j)].update(image_filename=IMAGES_DIR+'bat.png', image_size=IMAGE_SIZE)

def update_game_grid_visited_with_pit(i, j, c_stinks, c_breeze):
    if c_stinks: 
        if c_breeze:
            window[(i, j)].update(image_filename=IMAGES_DIR+'pit_stinks_breeze.png', image_size=IMAGE_SIZE)
        else:
            window[(i, j)].update(image_filename=IMAGES_DIR+'pit_stinks.png', image_size=IMAGE_SIZE)
    else:
        if c_breeze:
            window[(i, j)].update(image_filename=IMAGES_DIR+'pit_breeze.png', image_size=IMAGE_SIZE)
        else:
            window[(i, j)].update(image_filename=IMAGES_DIR+'pit.png', image_size=IMAGE_SIZE)

def update_game_grid_visited_with_wumpus(i, j, c_breeze):
    if c_breeze:
        window[(i, j)].update(image_filename=IMAGES_DIR+'wumpus_breeze.png', image_size=IMAGE_SIZE)
    else:
        window[(i, j)].update(image_filename=IMAGES_DIR+'wumpus.png', image_size=IMAGE_SIZE)

def update_game_grid_visited_with_treasure(i, j, c_stinks, c_breeze):
    if c_stinks: 
        if c_breeze:
            window[(i, j)].update(image_filename=IMAGES_DIR+'treasure_stinks_breeze.png', image_size=IMAGE_SIZE)
        else:
            window[(i, j)].update(image_filename=IMAGES_DIR+'treasure_stinks.png', image_size=IMAGE_SIZE)
    else:
        if c_breeze:
            window[(i, j)].update(image_filename=IMAGES_DIR+'treasure_breeze.png', image_size=IMAGE_SIZE)
        else:
            window[(i, j)].update(image_filename=IMAGES_DIR+'treasure.png', image_size=IMAGE_SIZE)

def update_game_grid_visited_with_deadwumpus(i, j, c_breeze):
    if c_breeze:
        window[(i, j)].update(image_filename=IMAGES_DIR+'deadwumpus_breeze.png', image_size=IMAGE_SIZE)
    else:
        window[(i, j)].update(image_filename=IMAGES_DIR+'deadwumpus.png', image_size=IMAGE_SIZE)


def check_characteristics(characteristics):
    c_stinks = c_breeze = c_dead = False
    for charac in characteristics:
        if charac.get_symbol() == wb.characteristic_stinks.get_symbol():
            c_stinks = True
        elif charac.get_symbol() == wb.characteristic_breeze.get_symbol():
            c_breeze = True
        elif charac.get_symbol() == wb.characteristic_death.get_symbol():
            c_dead = True
    return c_stinks, c_breeze, c_dead


def check_elements(elements):
    e_adventurer = e_pit = e_wumpus = e_bat = e_treasure = e_deadwumpus = False
    for elem in elements:
        if elem.get_name() == wb.ELEMENT_NAME_PIT:
            e_pit = True
        elif elem.get_name() == wb.ELEMENT_NAME_WUMPUS:
            e_wumpus = True
        elif elem.get_name() == wb.ELEMENT_NAME_BAT:
            e_bat = True
        elif elem.get_name() == wb.ELEMENT_NAME_ADVENTURER:
            e_adventurer = True
        elif elem.get_name() == wb.ELEMENT_NAME_TREASURE:
            e_treasure = True
        elif elem.get_name() == wb.ELEMENT_NAME_DEAD_WUMPUS:
            e_deadwumpus = True
    return e_adventurer, e_pit, e_wumpus, e_bat, e_treasure, e_deadwumpus 



def update_game_grid_adventurer(i, j, elements, characteristics):
    c_stinks, c_breeze, c_dead =  check_characteristics(characteristics)
    e_adventurer, e_pit, e_wumpus, e_bat, e_treasure, e_deadwumpus = check_elements(elements)
    global GAME_STATE
    
    if GAME_STATE == wm.GameState.END:
        return

    if c_dead and e_pit:
        window[(i, j)].update(image_filename=IMAGES_DIR+'adventurer_pit.png', image_size=IMAGE_SIZE)
        print('The adventurer fell into a bottomless pit. Game Over.')
        end_game()
    elif c_dead and e_wumpus:
        window[(i, j)].update(image_filename=IMAGES_DIR+'adventurer_wumpus.png', image_size=IMAGE_SIZE)
        print('The adventurer encountered the Wumpus. Game Over.')
        end_game()
    elif c_stinks and c_breeze:
        window[(i, j)].update(image_filename=IMAGES_DIR+'adventurer_stinks_breeze.png', image_size=IMAGE_SIZE)
        print('The adventurer feels the smell of a nearby Wumpus and a gentle breeze from a nearby Pit.')
    elif c_stinks and e_deadwumpus:
        window[(i, j)].update(image_filename=IMAGES_DIR+'adventurer_deadwumpus.png', image_size=IMAGE_SIZE)
        print('The adventurer walks over the body of the dead Wumpus.')
    elif e_bat: 
        window[(i, j)].update(image_filename=IMAGES_DIR+'bat.png', image_size=IMAGE_SIZE)
        print('Adventurer found a place with bat.')
        print('The bat is taking the Adventurer to a random place...')
        reposition_adventurer()
        update_game_grid()
    elif e_treasure:
        window[(i, j)].update(image_filename=IMAGES_DIR+'treasure.png', image_size=IMAGE_SIZE)
        print('Adventurer found the treasure. Game Over.')
        end_game()
    elif c_stinks:
        window[(i, j)].update(image_filename=IMAGES_DIR+'adventurer_stinks.png', image_size=IMAGE_SIZE)
        print('The adventurer feels the smell of a nearby Wumpus.')
    elif c_breeze:
        window[(i, j)].update(image_filename=IMAGES_DIR+'adventurer_breeze.png', image_size=IMAGE_SIZE)
        print('The adventurer feels a gentle breeze from a nearby Pit.')
    else:
        window[(i, j)].update(image_filename=IMAGES_DIR+'adventurer.png', image_size=IMAGE_SIZE)


def reposition_adventurer():
    x = random.randint(0, WORLD_WIDTH-1)
    y = random.randint(0, WORLD_HEIGHT-1)
    new_place_elements = wumpus_world.get_elements(x, y)
    if len(new_place_elements) == 0:
        adventurer = wumpus_world.get_adventurer()
        wumpus_world.remove_element(adventurer.is_on_place.x, adventurer.is_on_place.y, adventurer)
        wumpus_world.add_element(x, y, adventurer)
    else:
        reposition_adventurer()
    

def end_game():
    global GAME_STATE
    global wumpus_world
    for i in range(WORLD_WIDTH):
        for j in range(WORLD_HEIGHT):
            wumpus_world._places_visited[i][j] = True
    GAME_STATE = wm.GameState.END
    update_game_grid()


def check_arrow_shoot(x, y):
    global wumpus_world
    adventurer = wumpus_world.get_adventurer()
    if adventurer.get_qty_arrows() > 0:
        adventurer.use_arrow()
        check_arrow_shoot_wumpus_hit(adventurer, x, y)
    else:
        print('The Adventurer has no more arrows to shoot.')

def check_arrow_shoot_wumpus_hit(adventurer, x, y):
    global wumpus_world
    adv_x = adventurer.is_on_place.x
    adv_y = adventurer.is_on_place.y
    for i in range(min(x, adv_x), max(x, adv_x)+1):
        for j in range(min(y, adv_y), max(y, adv_y)+1):
            for element in wumpus_world.get_elements(i, j):
                if element.get_name() == wb.ELEMENT_NAME_WUMPUS:
                    print('The Adventurer hears a terrible scream of pain. The arrow hit the Wumpus!')
                    print('Wumpus is dead.')
                    wumpus_world.remove_element(i, j, element)
                    wumpus_world.add_element(event[0], event[1], wb.DeadWumpus(wumpus_world._places[i][j]))
                    wumpus_world._places_visited[i][j] = True
                    return
    print('The arrow hits nothing.')


#creates gui 
def create_layout():
    menu_def = [
                ['Game', [MENU_NEW_RANDOM, MENU_SAVE_FILE, MENU_OPEN_FILE, MENU_EXIT]],
                ['Settings', [MENU_OPTIONS, MENU_ABOUT]]
                ]
    arrow_elements = [
        [sg.Text('Arrows: ')],
        [sg.Button(BUTTON_SHOOT)],
        [sg.Input(key=KEY_ARROW_QTY, size=(5,1), default_text=wumpus_world.get_adventurer().get_qty_arrows(), readonly=True)],
    ]
    world_grid = [[sg.Button(size=(8, 4), key=(j,i), pad=(0,0), button_color=(sg.theme_background_color(), sg.theme_background_color()),
               image_filename=IMAGES_DIR+'not_visited.png', image_size=IMAGE_SIZE, border_width=2 ) for j in range(WORLD_WIDTH)] for i in range(WORLD_HEIGHT)]
    layout = [
        [sg.Menu(menu_def, key=KEY_MENU)],
        [sg.Column(arrow_elements), sg.Column(world_grid)],
        [sg.Output(size=(60, 12), echo_stdout_stderr=True)]
    ]
    return layout

def create_layout_window_options():
    layout = [
        [sg.Text('World width: '), sg.Input(key=KEY_INPUT_WIDTH, default_text=str(WORLD_WIDTH))],
        [sg.Text('World height: '), sg.Input(key=KEY_INPUT_HEIGHT, default_text=str(WORLD_HEIGHT))],
        [sg.Text('Number of pits in world: '), sg.Input(key=KEY_INPUT_PITS, default_text=str(WORLD_PITS))],
        [sg.Text('Number of bats in world: '), sg.Input(key=KEY_INPUT_BATS, default_text=str(WORLD_BATS))],
        [sg.Button(BUTTON_SAVE_OPTION), sg.Button(BUTTON_CANCEL_OPTION)]
    ]
    return layout

window = sg.Window(WINDOW_NAME, create_layout(), finalize=True)
window_options = None
create_new_random_world()
update_game_grid()

selected_color = ('red', 'white')

# Run the Event Loop
while True:
    wind, event, values = sg.read_all_windows()

    if event == MENU_EXIT:
        break

    elif event == sg.WIN_CLOSED and window_options == None:
        break

    elif event == BUTTON_CANCEL_OPTION or (event == sg.WIN_CLOSED and window_options != None):
        window_options = None
        window.reappear()

    elif event == BUTTON_SAVE_OPTION:
        WORLD_WIDTH = int(values[KEY_INPUT_WIDTH])
        WORLD_HEIGHT = int(values[KEY_INPUT_HEIGHT])
        WORLD_PITS = int(values[KEY_INPUT_PITS])
        WORLD_BATS = int(values[KEY_INPUT_BATS])
        window_options.close()
        window_options = None
        
        create_new_random_world()
        window.close()
        window = sg.Window(WINDOW_NAME, create_layout(), finalize=True)
        update_game_grid()
        print('New random game created with new options')

    elif event == MENU_NEW_RANDOM:
        create_new_random_world()
        update_game_grid()

    elif event == MENU_SAVE_FILE:
        filename = sg.popup_get_file('Save Game', save_as=True)
        if filename != None:
            wumpus_world.save_to_file(filename)
            print('Game saved to file ', filename)

    elif event == MENU_OPEN_FILE:
        filename = sg.popup_get_file('Open Saved Game')
        if filename != None:
            wumpus_world = wm.GridedGUIWumpusWorld(filename)
            WORLD_WIDTH = wumpus_world.get_world_width()
            WORLD_HEIGHT = wumpus_world.get_world_height()
            WORLD_PITS = wumpus_world.get_world_qty_pits()
            WORLD_BATS = wumpus_world.get_world_qty_bats()

            GAME_STATE = wm.GameState.START
            window.close()
            window = sg.Window(WINDOW_NAME, create_layout(), finalize=True)
            update_game_grid()
            print('Game loaded from file ', filename)

    elif event == MENU_OPTIONS:
        window_options = sg.Window('Options', create_layout_window_options(), finalize=True)
        

    elif event == MENU_ABOUT:
        window.disappear()
        sg.popup('About this program', 'Version 1.0', 'Wumpus game by eeyamane', 'Studies version')
        window.reappear()


    elif event == BUTTON_SHOOT and GAME_STATE != wm.GameState.END:
        if GAME_STATE == wm.GameState.START:
            GAME_STATE = wm.GameState.UPDATE_GAME_STATE
            window[BUTTON_SHOOT].update(button_color=selected_color)
        else: 
            GAME_STATE = wm.GameState.START
            window[BUTTON_SHOOT].update(button_color=sg.theme_button_color())

    elif GAME_STATE == wm.GameState.START and isinstance(event, tuple):
        adventurer = wumpus_world.get_adventurer()
        #if is a click in grid, checks if is adjacent to where is adventurer
        adv_x = adventurer.is_on_place.x
        adv_y = adventurer.is_on_place.y
        if abs(adv_x - event[0]) > 1 or abs(adv_y - event[1]) > 1 or abs(adv_x - event[0]) + abs(adv_y - event[1]) == 2:
            print('Place is not allowed. Adventurer can only walk one place at a time.')
        else:
            wumpus_world.remove_element(adventurer.is_on_place.x, adventurer.is_on_place.y, adventurer)
            wumpus_world.add_element(event[0], event[1], adventurer)
            update_game_grid()
            window[KEY_ARROW_QTY].update(wumpus_world.get_adventurer().get_qty_arrows())

    elif GAME_STATE == wm.GameState.UPDATE_GAME_STATE and isinstance(event, tuple):
        adventurer = wumpus_world.get_adventurer()
        #if is a click in grid, checks if the aiming place is at most two adjacent places
        adv_x = adventurer.is_on_place.x
        adv_y = adventurer.is_on_place.y
        if (abs(adv_x - event[0]) <= 2 and adv_y == event[1]) or (abs(adv_y - event[1]) <= 2 and adv_x == event[0]): 
            check_arrow_shoot(event[0], event[1])
            GAME_STATE = wm.GameState.START
            window[BUTTON_SHOOT].update(button_color=sg.theme_button_color())
            update_game_grid()
        else:
            print('The arrow can not reach this place. Arrow can reach two adjacent places from the Adventurer.')

window.close()