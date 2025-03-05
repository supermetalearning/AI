""" Analyzer.py - Task List:
✅ Grid_Rows
✅ Grid_Columns
✅ Grid_Dimensions
✅ Grid_Unique_Color_List
✅ Grid_Color_Frequency
✅ Grid_Majority_Color
✅ Grid_Vertically_Symmetric
✅ Grid_Horizontally_Symmetric
✅ Grid_Diagonally_Symmetric
✅ Grid_90_Degree_Symmetry

✅ Grid_Object_Count

✅ Object_Height = Height in Pixels
✅ Object_Width = Width in Pixels
✅ Object_Size = Number of Pixels
✅ Object_Solid = True or False
✅ Object_Hollow = True or False
✅ Object_SingleColored = True or False
✅ Object_Symmetric = True or False

More functionality to come soon!"""



#Find the Rows (aka Height) in the Grid
def grid_rows(grid):
    return len(grid)



#Find the number of Columns (aka Width) in the Grid
def grid_columns(grid):
    if not grid:
        return 0
    return len(grid[0])



#Return the Dimensions of the Matrix
def grid_dimensions(grid):
    return (grid_rows(grid), grid_columns(grid))



#Number of Unique Colors in the Grid
def grid_unique_colors(grid):
    unique_numbers = set()
    for row in grid:
        for number in row:
            unique_numbers.add(number)  # 0 is now explicitly considered a unique color
    return len(unique_numbers)



#Count frequency of each color in the grid
def grid_color_frequency(grid):
    color_counts = {}
    for row in grid:
        for color in row:
            if color in color_counts:  # Removed the color != 0 check to include 0
                color_counts[color] += 1
            else:
                color_counts[color] = 1
    return color_counts



#Find the Majority Color in the Grid
def grid_majority_color(grid):
    color_counts = grid_color_frequency(grid)
    return max(color_counts, key=color_counts.get)






#Check if Grid is Vertically Symmetric
def grid_is_vertically_symmetric(grid):
    # Handle empty grid case
    if not grid:
        return True
        
    rows = len(grid)
    cols = len(grid[0])
    
    # For each row, check if elements mirror across middle column
    for row in grid:
        for i in range(cols // 2):
            if row[i] != row[cols - 1 - i]:
                return False
                
    return True






#Check if Grid is Horizontally Symmetric
def grid_is_horizontally_symmetric(grid):
    # Handle empty grid case
    if not grid:
        return True
        
    rows = len(grid)
    cols = len(grid[0])
    
    # For each column, check if elements mirror across middle row
    for c in range(cols):
        for r in range(rows // 2):
            if grid[r][c] != grid[rows - 1 - r][c]:
                return False
                
    return True




#Check if Grid is Diagonally Symmetric
def grid_is_diagonally_symmetric(grid):
    # Handle empty grid case
    if not grid:
        return True
        
    rows = len(grid)
    cols = len(grid[0])
    
    # Grid must be square for diagonal symmetry
    if rows != cols:
        return False
    
    # Check main diagonal (top-left to bottom-right)
    for i in range(rows):
        for j in range(i + 1, cols):
            if grid[i][j] != grid[j][i]:
                return False
                
    return True







#Check if Grid has 90-degree Rotational Symmetry
def grid_has_90_degree_symmetry(grid):
    # Handle empty grid case
    if not grid:
        return True
        
    rows = len(grid)
    cols = len(grid[0])
    
    # Grid must be square for 90 degree rotational symmetry
    if rows != cols:
        return False
            
    for r in range(rows):
        for c in range(cols):
            # For 90 degree rotation: (r,c) -> (c, n-1-r)
            if grid[r][c] != grid[c][rows-1-r]:
                return False
    return True














#Find the Number of Objects in the Grid using Connected Components
def grid_object_count(grid):
    # Handle empty grid case
    if not grid:
        return 0
            
    # Get grid dimensions
    rows = len(grid)
    cols = len(grid[0])
    
    # Create visited array to track processed cells
    visited = [[False]*cols for _ in range(rows)]
    object_count = 0
    
    # Depth-first search to find connected components
    def dfs(r, c):
        # Check boundary conditions and validity:
        # - Within grid bounds
        # - Not already visited
        # - Not background color (0)
        if (r < 0 or r >= rows or 
            c < 0 or c >= cols or
            visited[r][c] or 
            grid[r][c] == 0):
            return
            
        # Mark current cell as visited
        visited[r][c] = True
        
        # Recursively explore all 8 adjacent neighbors
        # This includes diagonals (-1,-1) to (1,1)
        for dr in [-1,0,1]:
            for dc in [-1,0,1]:
                dfs(r+dr, c+dc)
    
    # Main loop to find all objects
    for i in range(rows):
        for j in range(cols):
            # If we find an unvisited non-background cell,
            # it's the start of a new object
            if not visited[i][j] and grid[i][j] != 0:
                object_count += 1
                # Use DFS to mark all connected cells regardless of color
                dfs(i, j)
                
    return object_count







# Extract a subgrid containing just the object
def get_object_subgrid(grid, pixels, bounds):
    """Extract a subgrid containing just the object"""
    min_r, max_r, min_c, max_c = bounds
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    
    # Create empty subgrid
    subgrid = [[0 for _ in range(width)] for _ in range(height)]
    
    # Fill in the object pixels
    for r, c in pixels:
        subgrid[r - min_r][c - min_c] = grid[r][c]
        
    return subgrid

def describe_objects(grid):
    # Handle empty grid case
    if not grid:
        return []
            
    # Get grid dimensions
    rows = len(grid)
    cols = len(grid[0])
    
    # Create visited array to track processed cells
    visited = [[False]*cols for _ in range(rows)]
    objects = []
    
    def get_object_bounds(r, c, target_color):
        """Get min/max coordinates and all pixels of a single-colored object using DFS"""
        min_r = max_r = r
        min_c = max_c = c
        pixels = set()
        
        def dfs(r, c):
            nonlocal min_r, max_r, min_c, max_c
            
            if (r < 0 or r >= rows or 
                c < 0 or c >= cols or
                visited[r][c] or 
                grid[r][c] != target_color):  # Only continue if same color
                return
                
            visited[r][c] = True
            pixels.add((r,c))
            
            min_r = min(min_r, r)
            max_r = max(max_r, r)
            min_c = min(min_c, c)
            max_c = max(max_c, c)
            
            # Check all 8 adjacent cells
            for dr in [-1,0,1]:
                for dc in [-1,0,1]:
                    dfs(r+dr, c+dc)
                    
        dfs(r, c)
        return min_r, max_r, min_c, max_c, pixels
    
    def is_solid(pixels, bounds):
        """Check if object has no internal holes"""
        min_r, max_r, min_c, max_c = bounds
        area = (max_r - min_r + 1) * (max_c - min_c + 1)
        return len(pixels) == area
        
    def is_hollow(pixels, bounds):
        """Check if object has internal holes"""
        min_r, max_r, min_c, max_c = bounds
        # Object is hollow if it has internal pixels not part of the object
        for r in range(min_r+1, max_r):
            for c in range(min_c+1, max_c):
                if (r,c) not in pixels and all((r+dr,c+dc) in pixels 
                    for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]):
                    return True
        return False
    
    # Main loop to find and describe all objects
    for i in range(rows):
        for j in range(cols):
            if not visited[i][j] and grid[i][j] != 0:
                current_color = grid[i][j]
                min_r, max_r, min_c, max_c, pixels = get_object_bounds(i, j, current_color)
                bounds = (min_r, max_r, min_c, max_c)
                
                # Get object's subgrid for symmetry analysis
                subgrid = get_object_subgrid(grid, pixels, bounds)
                
                # Convert set of pixels to sorted list for consistent output
                pixel_list = sorted(list(pixels))
                
                obj_desc = {
                    'position': pixel_list,  # Now contains all pixel coordinates
                    'height': max_r - min_r + 1,
                    'width': max_c - min_c + 1,
                    'size': len(pixels),
                    'colors': [current_color],  # Now always a single color
                    'is_single_colored': True,  # Always true by definition
                    'is_solid': is_solid(pixels, bounds),
                    'is_hollow': is_hollow(pixels, bounds),
                    'vertical_symmetry': grid_is_vertically_symmetric(subgrid),
                    'horizontal_symmetry': grid_is_horizontally_symmetric(subgrid),
                    'diagonal_symmetry': grid_is_diagonally_symmetric(subgrid),
                    'rotational_90_symmetry': grid_has_90_degree_symmetry(subgrid)
                }
                objects.append(obj_desc)
                
    return objects














def analyze_grid(grid):
    """Analyzes a grid and returns a dictionary containing all grid and object properties"""
    
    # Grid level analysis
    analysis = {
        'rows': grid_rows(grid),
        'columns': grid_columns(grid),
        'dimensions': grid_dimensions(grid),
        'unique_colors': grid_unique_colors(grid),
        'color_frequency': grid_color_frequency(grid),
        'majority_color': grid_majority_color(grid),
        'vertical_symmetry': grid_is_vertically_symmetric(grid),
        'horizontal_symmetry': grid_is_horizontally_symmetric(grid),
        'diagonal_symmetry': grid_is_diagonally_symmetric(grid),
        'rotational_90_symmetry': grid_has_90_degree_symmetry(grid),
        'objects': []
    }
    
    # Get detailed object analysis
    objects = describe_objects(grid)
    
    # Add each object's properties
    for obj in objects:
        object_info = {
            'position': obj['position'],
            'height': obj['height'],
            'width': obj['width'], 
            'size': obj['size'],
            'colors': obj['colors'],
            'is_single_colored': obj['is_single_colored'],
            'is_solid': obj['is_solid'],
            'is_hollow': obj['is_hollow'],
            'vertical_symmetry': obj['vertical_symmetry'],
            'horizontal_symmetry': obj['horizontal_symmetry'],
            'diagonal_symmetry': obj['diagonal_symmetry'],
            'rotational_90_symmetry': obj['rotational_90_symmetry']
        }
        analysis['objects'].append(object_info)
    
    return analysis














grid = [
        [0,0,0,0,8,3,3,3,3,8,0,0,0,0,8,0,0,0,0,8,0,0,0,0],
        [0,0,0,0,8,3,3,3,3,8,0,0,0,0,8,0,0,0,0,8,0,0,0,0],
        [0,0,0,0,8,3,3,3,3,8,0,0,0,0,8,0,0,0,0,8,0,0,0,0],
        [0,0,0,0,8,3,3,3,3,8,0,0,0,0,8,0,0,0,0,8,0,0,0,0],
        [8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8],
        [3,3,3,3,8,6,6,6,6,8,3,3,3,3,8,0,0,0,0,8,0,0,0,0],
        [3,3,3,3,8,6,6,6,6,8,3,3,3,3,8,0,0,0,0,8,0,0,0,0],
        [3,3,3,3,8,6,6,6,6,8,3,3,3,3,8,0,0,0,0,8,0,0,0,0],
        [3,3,3,3,8,6,6,6,6,8,3,3,3,3,8,0,0,0,0,8,0,0,0,0],
        [8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8],
        [0,0,0,0,8,3,3,3,3,8,0,0,0,0,8,0,0,0,0,8,0,0,0,0],
        [0,0,0,0,8,3,3,3,3,8,0,0,0,0,8,0,0,0,0,8,0,0,0,0],
        [0,0,0,0,8,3,3,3,3,8,0,0,0,0,8,0,0,0,0,8,0,0,0,0],
        [0,0,0,0,8,3,3,3,3,8,0,0,0,0,8,0,0,0,0,8,0,0,0,0],
        [8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8],
        [0,0,0,0,8,0,0,0,0,8,0,0,0,0,8,0,0,0,0,8,0,0,0,0],
        [0,0,0,0,8,0,0,0,0,8,0,0,0,0,8,0,0,0,0,8,0,0,0,0],
        [0,0,0,0,8,0,0,0,0,8,0,0,0,0,8,0,0,0,0,8,0,0,0,0],
        [0,0,0,0,8,0,0,0,0,8,0,0,0,0,8,0,0,0,0,8,0,0,0,0],
        [8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8],
        [0,0,0,0,8,0,0,0,0,8,0,0,0,0,8,6,6,6,6,8,0,0,0,0],
        [0,0,0,0,8,0,0,0,0,8,0,0,0,0,8,6,6,6,6,8,0,0,0,0],
        [0,0,0,0,8,0,0,0,0,8,0,0,0,0,8,6,6,6,6,8,0,0,0,0],
        [0,0,0,0,8,0,0,0,0,8,0,0,0,0,8,6,6,6,6,8,0,0,0,0],
      ]


















def print_analysis_results(analysis):
    """Prints analysis results in a formatted way"""
    # Color mapping dictionary
    color_map = {
        0: "Black",
        1: "Blue",
        2: "Red",
        3: "Green",
        4: "Yellow",
        5: "Grey",
        6: "Pink",
        7: "Orange",
        8: "Azure",
        9: "Brown"
    }

    def get_color_description(color_num):
        color_name = color_map.get(color_num, str(color_num))
        return f"{color_num} ({color_name})"

    def get_object_name(index):
        return f"Object_{index:03d}"

    def create_box(text_lines):
        # Find the longest line to determine box width
        width = max(len(line) for line in text_lines)
        # Create the box
        box_top = "╔" + "═" * (width + 2) + "╗"
        box_bottom = "╚" + "═" * (width + 2) + "╝"
        # Create the box with content
        result = [box_top]
        for line in text_lines:
            result.append(f"║ {line}{' ' * (width - len(line))} ║")
        result.append(box_bottom)
        return "\n".join(result)

    # Print basic grid info
    print("\n=== Grid Analysis ===")
    print(f"Rows: {analysis['rows']}")
    print(f"Columns: {analysis['columns']}")
    print(f"Dimensions: {analysis['dimensions']}")
    print(f"Unique Colors: {analysis['unique_colors']}")
    
    # Format color frequency
    print("\n=== Color Distribution ===")
    color_freq = {get_color_description(k): v for k, v in analysis['color_frequency'].items()}
    majority_color = get_color_description(analysis['majority_color'])
    
    # Print color frequencies
    for color, freq in color_freq.items():
        print(f"{color}: {freq}")
    print(f"\nMajority Color: {majority_color}")
    
    # Print symmetry information
    print("\n=== Grid Symmetry Analysis ===")
    print(f"Vertical: {analysis['vertical_symmetry']}")
    print(f"Horizontal: {analysis['horizontal_symmetry']}")
    print(f"Diagonal: {analysis['diagonal_symmetry']}")
    print(f"90° Rotation: {analysis['rotational_90_symmetry']}")
    
    # Print objects analysis
    print("\n=== Objects Analysis ===")
    for i, obj in enumerate(analysis['objects'], 1):
        object_name = get_object_name(i)
        
        # Create list of lines for this object
        object_lines = [
            object_name,
            f"Height: {obj['height']}",
            f"Width: {obj['width']}",
            f"Size: {obj['size']}",
            f"Single Colored: {obj['is_single_colored']}",
            f"Solid: {obj['is_solid']}",
            f"Hollow: {obj['is_hollow']}",
            "Symmetry Properties:",
            f"  Vertical: {obj['vertical_symmetry']}",
            f"  Horizontal: {obj['horizontal_symmetry']}",
            f"  Diagonal: {obj['diagonal_symmetry']}",
            f"  90° Rotation: {obj['rotational_90_symmetry']}",
            f"Colors: {[get_color_description(c) for c in obj['colors']]}"
        ]
        
        # Print the boxed object description
        print(f"\n{create_box(object_lines)}")

print_analysis_results(analyze_grid(grid))