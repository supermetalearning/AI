#writing some of the DSL transformations



# First 15x15 grid with 7x7 rectangle in middle
grid1 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]



def Fill(grid, color):
    """
    Changes the color of the interior of an object while preserving the border.
    Works for objects represented by any number 1-9.
    
    Args:
        grid: 2D grid containing the object
        color: New color value to fill the interior with
        
    Returns:
        Modified grid with filled interior
    """
    rows = len(grid)
    cols = len(grid[0])
    
    # Create a copy of the input grid
    new_grid = [row[:] for row in grid]
    
    # Find interior points (points that have neighbors in all 8 directions)
    for i in range(1, rows-1):
        for j in range(1, cols-1):
            current = grid[i][j]
            if (1 <= current <= 9 and
                grid[i-1][j] == current and      # North
                grid[i+1][j] == current and      # South
                grid[i][j-1] == current and      # West
                grid[i][j+1] == current and      # East
                grid[i-1][j-1] == current and    # Northwest
                grid[i-1][j+1] == current and    # Northeast
                grid[i+1][j-1] == current and    # Southwest
                grid[i+1][j+1] == current):      # Southeast
                new_grid[i][j] = color
                
    return new_grid


def visualize_grid(grid):
    """
    Visualizes a 2D grid using matplotlib with a custom color map.
    
    Args:
        grid: 2D grid to visualize
    """
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.colors import ListedColormap
    
    # Define color map
    color_map = {
        0: "#000000",  # Black
        1: "#0000FF",  # Blue
        2: "#FF0000",  # Red
        3: "#00FF00",  # Green
        4: "#FFFF00",  # Yellow
        5: "#808080",  # Grey
        6: "#FFC0CB",  # Pink
        7: "#FFA500",  # Orange
        8: "#F0FFFF",  # Azure
        9: "#A52A2A"   # Brown
    }
    
    # Convert grid to numpy array
    grid_array = np.array(grid)
    
    # Create custom colormap from color_map values
    colors = [color_map[i].lower() for i in range(len(color_map))]
    custom_cmap = ListedColormap(colors)
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Plot with pixels as 1x1 boxes centered on integer coordinates
    plt.pcolormesh(np.arange(grid_array.shape[1] + 1),
                   np.arange(grid_array.shape[0] + 1),
                   grid_array,
                   cmap=custom_cmap,
                   vmin=0,
                   vmax=9)
    
    # Add gridlines aligned with pixel edges
    plt.grid(True, which='major', color='white', linewidth=0.5, alpha=0.3)
    
    # Set ticks to match grid coordinates
    plt.xticks(range(len(grid[0])))
    plt.yticks(range(len(grid)))
    
    # Invert y-axis to match array orientation
    plt.gca().invert_yaxis()
    
    plt.title('Grid Visualization')
    plt.show()



grid2 = Fill(grid1, 7)



visualize_grid(grid1)
visualize_grid(grid2)   


