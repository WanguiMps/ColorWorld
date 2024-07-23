def get_limits(color):
    limits = {
        'red': ((0, 50, 50), (10, 255, 255)),  # Adjust the HSV limits as needed
        'blue': ((100, 50, 50), (130, 255, 255)),
        'green': ((40, 50, 50), (80, 255, 255)),
        'yellow': ((20, 50, 50), (30, 255, 255)),
        'cyan': ((80, 50, 50), (100, 255, 255)),
        'magenta': ((140, 50, 50), (160, 255, 255)),
        'white': ((0, 0, 200), (180, 20, 255)),
        'black': ((0, 0, 0), (180, 255, 30))
    }
    return limits[color]

