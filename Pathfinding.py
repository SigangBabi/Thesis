import cv2
import numpy as np
import matplotlib.pyplot as plt
import heapq


def load_map_with_specific_color_obstacles_and_roads(
    image_path, scale=0.5, target_hsv_lower=None, target_hsv_upper=None, road_hsv_lower=None, road_hsv_upper=None):
    # Step 1: Load and resize the map image
    map_resized = cv2.resize(cv2.imread(image_path), None, fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST)

    # Step 2: Initialize the grid with obstacles (default: 1 for obstacles, 0 for free space)
    grid = np.ones((map_resized.shape[0], map_resized.shape[1]), dtype=np.uint8)

    # Step 3: Convert to HSV for color-based detection
    map_hsv = cv2.cvtColor(map_resized, cv2.COLOR_BGR2HSV)

    # Step 4: Detect roads and set them as traversable
    if road_hsv_lower is not None and road_hsv_upper is not None:
        road_mask = cv2.inRange(map_hsv, road_hsv_lower, road_hsv_upper)
        grid[np.where(road_mask > 0)] = 0  # Set roads as traversable

    # Step 5: Detect specific color range as obstacles
    if target_hsv_lower is not None and target_hsv_upper is not None:
        obstacle_mask = cv2.inRange(map_hsv, target_hsv_lower, target_hsv_upper)
        grid[np.where(obstacle_mask > 0)] = 1  # Set obstacles

    #grid[200:220, :] = 0

    return map_resized, grid


# A* Algorithm for pathfinding
def a_star(grid, start, goal):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        neighbors = [
            (current[0] + 1, current[1]),
            (current[0] - 1, current[1]),
            (current[0], current[1] + 1),
            (current[0], current[1] - 1),
        ]
        for neighbor in neighbors:
            if 0 <= neighbor[0] < grid.shape[0] and 0 <= neighbor[1] < grid.shape[1]:
                if grid[neighbor] == 1:  # Skip obstacles
                    continue
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None  # No path found


# Visualization with the original map
def visualize_with_obstacles(map_img, grid, path=None, start=None, goal=None):
    plt.figure(figsize=(12, 12))

    # Overlay obstacles on the map image
    obstacle_overlay = np.zeros_like(map_img, dtype=np.uint8)
    obstacle_overlay[grid == 1] = [255, 0, 0]  # Red color for obstacles
    map_with_obstacles = cv2.addWeighted(map_img, 0.7, obstacle_overlay, 0.3, 0)

    plt.imshow(map_with_obstacles, origin="upper")  # Display the map with obstacles

    if path:
        path_coords = np.array(path)
        plt.plot(path_coords[:, 1], path_coords[:, 0], color="blue", linewidth=2, label="Path")

    if start:
        plt.scatter(start[1], start[0], color="green", s=100, label="Start")

    if goal:
        plt.scatter(goal[1], goal[0], color="red", s=100, label="Goal")

    plt.legend()
    plt.grid(True)
    plt.show()

def get_goal_point_from_user(map_img):
    """
    Allows the user to click on the map to specify the goal point.
    Returns the clicked point as (row, col).
    """
    goal_point = []

    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:  # Left mouse button click
            goal_point.append((y, x))  # OpenCV uses (x, y), but we need (row, col)
            print(f"Goal Point Selected: {goal_point[-1]}")
            cv2.destroyWindow("Select Goal Point")

    cv2.imshow("Select Goal Point", map_img)
    cv2.setMouseCallback("Select Goal Point", mouse_callback)
    cv2.waitKey(0)

    if goal_point:
        return goal_point[0]  # Return the selected goal point
    else:
        print("No goal point selected.")
        return None


# Main
map_path = "campus_map.png"  # Path to your map image
scale_factor = 1  # Adjust the scale as needed

# Define HSV ranges
road_hsv_lower = np.array([95, 30, 190])  # Adjust for road color (example: light gray)
road_hsv_upper = np.array([115, 50, 255])
obstacle_hsv_lower = np.array([110, 0, 230])  # Example obstacle HSV range
obstacle_hsv_upper = np.array([120, 20, 255])

# Load the map with roads and obstacles
map_img, campus_grid = load_map_with_specific_color_obstacles_and_roads(
    map_path, scale=scale_factor, target_hsv_lower=obstacle_hsv_lower, target_hsv_upper=obstacle_hsv_upper,
    road_hsv_lower=road_hsv_lower, road_hsv_upper=road_hsv_upper
)

# Define start and goal points (in grid coordinates)
start_point = (510, 100)
goal_point = get_goal_point_from_user(map_img)


if goal_point:
    # Run A* algorithm
    path = a_star(campus_grid, start_point, goal_point)

    # Visualize the results
    visualize_with_obstacles(map_img, campus_grid, path=path, start=start_point, goal=goal_point)
else:
    print("Pathfinding aborted: No goal point selected.")
