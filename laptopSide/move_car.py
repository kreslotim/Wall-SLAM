def move_car(start_pos, suggested_path):
    x, y = start_pos
    nodes = [(x, y)]
    direction = None

    for move in suggested_path:
        if move == 'right':
            if direction != 'right':
                nodes.append((x + 10, y))
                direction = 'right'
            x += 10
        elif move == 'down':
            if direction != 'down':
                nodes.append((x, y - 10))
                direction = 'down'
            y -= 10
        elif move == 'left':
            if direction != 'left':
                nodes.append((x - 10, y))
                direction = 'left'
            x -= 10
        elif move == 'up':
            if direction != 'up':
                nodes.append((x, y + 10))
                direction = 'up'
            y += 10

    return nodes


start_pos = (0, 0)
suggested_path = ['right', 'right', 'down', 'down', 'right', 'right', 'up', 'left']
nodes = move_car(start_pos, suggested_path)
print(nodes)