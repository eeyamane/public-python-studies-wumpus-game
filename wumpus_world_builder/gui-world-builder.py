import PySimpleGUI as sg
import json
import traceback

WORLD_WIDTH = 7
WORLD_HEIGHT = 5
ARROWS_QTY = 2
KEY_WORLD_WIDTH = '-IN_WORLD_WIDTH-'
KEY_WORLD_HEIGHT = '-IN_WORLD_HEIGHT-'
KEY_ARROWS_QTY = '-IN_ARROWS_QTY-'
KEY_FILE_NAME = '-IN-FILE-NAME-'
WINDOW_NAME = 'Wumpus World Builder'

symbol_to_text = {
    'A': 'Adventurer',
    'W': 'Wumpus',
    'P': 'Pit',
    'B': 'Bat',
    'T': 'Treasure'
}

#creates world grid with an array 
world_array = list()
def init_world_array():
    global world_array
    world_array = list()
    for i in range(WORLD_WIDTH):
        world_array.append(list())
        for j in range(WORLD_HEIGHT):
            world_array[i].append(' ')


#creates a new world array grid with new size, copying (when possible) the old array's data
def update_world_array_resize():
    new_world_array = list()
    for i in range(WORLD_WIDTH):
        new_world_array.append(list())
        for j in range(WORLD_HEIGHT):
            new_world_array[i].append(' ')

    i = 0
    while i < WORLD_WIDTH and i < len(world_array):
        j = 0
        while j < WORLD_HEIGHT and j < len(world_array[i]):
            new_world_array[i][j] = world_array[i][j]
            j = j + 1
        i = i + 1
    return new_world_array


#updates elements at the world array - wumpus, treasure and adventurer can only have 1 instance
def update_array(event, selected_button):
    if selected_button in ('Adventurer', 'Wumpus', 'Treasure'):
        is_found = False
        for i in range(WORLD_WIDTH):
            for j in range(WORLD_HEIGHT):
                if world_array[i][j] == selected_button:
                    world_array[i][j] = ' '
                    window[(i, j)].update(' ')
                    is_found = True
                    break
            if is_found:
                break

    if world_array[event[0]][event[1]] == selected_button:
        window[event].update(' ')
        world_array[event[0]][event[1]] = ' '
    else:
        window[event].update(selected_button)
        world_array[event[0]][event[1]] = selected_button


#saves world as a json
def save_world_to_file(filename):
    dict_json = __generate_dict_with_elements_to_json()
    dict_json['version'] = 'v-f-2'
    dict_json['width'] = WORLD_WIDTH
    dict_json['height'] = WORLD_HEIGHT
    json_object = json.dumps(dict_json)
    try:
        f = open(filename, 'w')
        f.write(json_object)
        f.close()
        print('File saved.')
    except IOError as e:
        print('Error saving file ' + filename, e)
        traceback.print_exc()

#transforms world array into a json
def __generate_dict_with_elements_to_json():
    dict_json = dict()
    dict_json['places_visited'] = list()
    dict_json['elements'] = list()
    
    for x in range(WORLD_WIDTH):
        for y in range(WORLD_HEIGHT):
            element = world_array[x][y]
            if element == 'Adventurer':
                dict_json['elements'].append({'symbol': 'A', 'x': x, 'y': y, 'arrows': ARROWS_QTY})
            elif element != ' ':
                dict_json['elements'].append({'symbol': element[0:1], 'x': x, 'y': y})

    return dict_json


#load world from file
def load_world_from_file(filename):
    with open(filename, 'r') as f: 
        json_world = json.load(f)

        version = json_world['version']
        if (version != 'v-f-2'):
            print('File version not supported. Nothing will be done.')
        else:
            __load_from_json(json_world)

#load world from json
def __load_from_json(json_world):
    global WORLD_WIDTH, WORLD_HEIGHT, ARROWS_QTY
    WORLD_WIDTH = json_world['width']
    WORLD_HEIGHT = json_world['height']
    init_world_array()

    for elem in json_world['elements']:
        symb = elem['symbol']
        x = elem['x']
        y = elem['y']
        world_array[x][y] = symbol_to_text[symb]
        if symb == 'A':
            ARROWS_QTY = elem['arrows']


init_world_array()
sg.theme('Reddit')

#creates gui 
def create_layout():
    column_elements = [
        [sg.Text('Elements: ')],
        [sg.Button('Adventurer')],
        [sg.Button('Wumpus')],
        [sg.Button('Bat')],
        [sg.Button('Pit')],
        [sg.Button('Treasure')],
    ]
    world_grid = [[sg.Button(world_array[j][i], size=(4, 2), key=(j,i), pad=(0,0)) for j in range(WORLD_WIDTH)] for i in range(WORLD_HEIGHT)]
    column_world = [
        [sg.Text('World: ')],
        [sg.Column(world_grid)]
    ]
    layout = [
        [sg.Text('World Size: '), sg.Input(key=KEY_WORLD_WIDTH, size=(4,1), default_text=WORLD_WIDTH, enable_events=True), sg.Text(' x ') , sg.Input(key=KEY_WORLD_HEIGHT, size=(4,1), default_text=WORLD_HEIGHT, enable_events=True), sg.Button('Refresh')],
        [sg.Text('Arrows Qty: '), sg.Input(key=KEY_ARROWS_QTY, size=(4,1), default_text=ARROWS_QTY, enable_events=True)],
        [sg.Column(column_elements), sg.Column(column_world)],
        [sg.Text('File: '), sg.Input(key=KEY_FILE_NAME), sg.FileBrowse(), sg.Button('Load', enable_events=True)],
        [sg.FileSaveAs('Save', enable_events=True)]
    ]
    return layout


window = sg.Window(WINDOW_NAME, create_layout())

selected_button = None
selected_color = ('red', 'white')

# Run the Event Loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event in ('Adventurer', 'Wumpus', 'Pit', 'Bat', 'Treasure'):
        if selected_button != None:
            window[selected_button].update(button_color=sg.theme_button_color())
        window[event].update(button_color=selected_color)
        selected_button = event

    elif event == KEY_WORLD_WIDTH:
        try: 
            WORLD_WIDTH = int(values[KEY_WORLD_WIDTH])
        except ValueError as verr:
            window[KEY_WORLD_WIDTH].update(WORLD_WIDTH)

    elif event == KEY_WORLD_HEIGHT:
        try: 
            WORLD_HEIGHT = int(values[KEY_WORLD_HEIGHT])
        except ValueError as verr:
            window[KEY_WORLD_HEIGHT].update(WORLD_HEIGHT)

    elif event == KEY_ARROWS_QTY:
        try: 
            ARROWS_QTY = int(values[KEY_ARROWS_QTY])
        except ValueError as verr:
            window[KEY_ARROWS_QTY].update(ARROWS_QTY)

    elif event == ('Refresh'):
        world_array = update_world_array_resize()
        window.close()
        window = sg.Window(WINDOW_NAME, create_layout())

    elif isinstance(event, tuple) and selected_button != None:
        update_array(event, selected_button)

    elif event == 'Save':
        window[KEY_FILE_NAME].update(values['Save'])
        save_world_to_file(values['Save'])

    elif event == 'Load':
        load_world_from_file(values['Browse'])
        window.close()
        window = sg.Window(WINDOW_NAME, create_layout())


window.close()