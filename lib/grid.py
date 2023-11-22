import numpy as np

class CollidersGrid:
    def __init__(self, filename, safety_distance=3, drone_altitude=5):
        data = np.loadtxt(filename, delimiter=',', dtype='float64', skiprows=2)

        north_min = np.floor(np.amin(data[:, 0] - data[:, 3]))
        north_max = np.ceil(np.amax(data[:, 0] + data[:, 3]))
        north_size = int(np.ceil((north_max - north_min)))

        east_min = np.floor(np.amin(data[:, 1] - data[:, 4]))
        east_max = np.ceil(np.amax(data[:, 1] + data[:, 4]))
        east_size = int(np.ceil((east_max - east_min)))

        grid = np.zeros((north_size, east_size))
        points = []

        for obstacle_idx in range(data.shape[0]):
            north, east, alt, d_north, d_east, d_alt = data[obstacle_idx, :]

            if alt + d_alt + safety_distance > drone_altitude:
                north_start = int(north - d_north - safety_distance - north_min)
                north_end = int(north + d_north + safety_distance - north_min)

                east_start = int(east - d_east - safety_distance - east_min)
                east_end = int(east + d_east + safety_distance - east_min)

                grid[north_start:north_end, east_start:east_end] = 1
                points.append((north - north_min, east - east_min))

        self.grid = grid
        self.points = points
        self.north_size = north_size
        self.east_size = east_size

def colliders_grid(filename, safety_distance=3, drone_altitude=5):
    """From colliders.csv data create a grid with obstacles (1) and free space (0)

    Args:
        filename (str): colliders csv filename
        safety_distance (int): max distance between drone and obstacle
        drone_altitude (int): static drone altitude

    Returns:
        grid: NxN grid with 1 as obstacles and 0 as free space
        points: (list of tuples) all points of obstacle
    """
    
    data = np.loadtxt(filename, delimiter=',', dtype='float64', skiprows=2)

    north_min = np.floor(np.amin(data[:, 0] - data[:, 3]))
    north_max = np.ceil(np.amax(data[:, 0] + data[:, 3]))
    north_size = int(np.ceil((north_max - north_min)))

    east_min = np.floor(np.amin(data[:, 1] - data[:, 4]))
    east_max = np.ceil(np.amax(data[:, 1] + data[:, 4]))
    east_size = int(np.ceil((east_max - east_min)))

    grid = np.zeros((north_size, east_size))
    points = []

    for obstacle_idx in range(data.shape[0]):
        north, east, alt, d_north, d_east, d_alt = data[obstacle_idx, :]

        if alt + d_alt + safety_distance > drone_altitude:
            north_start = int(north - d_north - safety_distance - north_min)
            north_end = int(north + d_north + safety_distance - north_min)

            east_start = int(east - d_east - safety_distance - east_min)
            east_end = int(east + d_east + safety_distance - east_min)

            grid[north_start:north_end, east_start:east_end] = 1
            points.append([north - north_min, east - east_min])

    return grid, points