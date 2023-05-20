def move_car(start_pos, suggested_path):
    x, y = start_pos
    nodes = [(x, y)]
    direction = None
    scale_factor=10;

    for move in suggested_path:
        if move == 'right':
            if direction != 'right':
                nodes.append((x + scale_factor, y))
                direction = 'right'
            x += scale_factor
        elif move == 'down':
            if direction != 'down':
                nodes.append((x, y -scale_factor))
                direction = 'down'
            y -= scale_factor
        elif move == 'left':
            if direction != 'left':
                nodes.append((x - scale_factor, y))
                direction = 'left'
            x -= scale_factor
        elif move == 'up':
            if direction != 'up':
                nodes.append((x, y + scale_factor))
                direction = 'up'
            y += scale_factor

    return nodes


start_pos = (0, 0)
suggested_path = ['right', 'right', 'down', 'down', 'right', 'right', 'up', 'left']
nodes = move_car(start_pos, suggested_path)
print(nodes)
