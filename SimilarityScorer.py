#this program will score the similarity between two grids

# d = Dimensional Similarity
# o = Object Similarity
# c = Color Similarity
# p = Pixel Similarity
# t = Total Similarity
# Call the First Function below to get the Final Result





def grids_total_similarity(grid1, grid2):
    """
    Calculate overall similarity score by combining dimensional, object, color and coordinate similarities
    with weighted averaging. Dimensional and coordinate similarities have higher weights
    since they are more fundamental structural measures.
            
    Args:
        grid1: First grid
        grid2: Second grid
                
    Returns:
        Float between 0-100 representing total similarity percentage
    """
    # Calculate individual similarity scores
    dim_similarity = grids_dimensional_similarity(grid1, grid2)
    obj_similarity = grids_objects_similarity(grid1, grid2) 
    color_similarity = grids_colors_similarity(grid1, grid2)
    coord_similarity = grids_coordinate_similarity(grid1, grid2)
            
    # Combine scores with weighted importance:
    # Dimensional: 35%
    # Coordinate: 35% 
    # Objects: 20%
    # Colors: 10%
    total_similarity = (dim_similarity * 0.35 +
                        coord_similarity * 0.35 +
                        obj_similarity * 0.20 +
                        color_similarity * 0.10)
                              
    return total_similarity























def grids_dimensional_similarity(grid1, grid2):
    """
    Calculate similarity score based on grid dimensions.
    Returns 100 if dimensions match exactly, 0 if completely different.
    """
    # Get dimensions of both grids
    rows1, cols1 = len(grid1), len(grid1[0])
    rows2, cols2 = len(grid2), len(grid2[0])
    
    # Calculate row and column similarity ratios
    row_similarity = min(rows1, rows2) / max(rows1, rows2)
    col_similarity = min(cols1, cols2) / max(cols1, cols2)
    
    # Overall dimensional similarity is average of row and column similarities
    # Multiply by 100 to get score between 0 and 100
    dim_similarity = ((row_similarity + col_similarity) / 2) * 100
    
    return dim_similarity













def grids_objects_similarity(grid1, grid2):
    """
    Calculate similarity score based on number and sizes of objects in the grids.
    Returns a score between 0 and 100, where:
    - 100 means identical number and sizes of objects
    - 0 means completely different objects
    """
    # Count number of objects in each grid
    objects1 = count_objects(grid1)
    objects2 = count_objects(grid2)
    
    # Calculate similarity based on number of objects
    count_similarity = min(objects1, objects2) / max(objects1, objects2)
    
    # Get sizes of all objects in each grid
    sizes1 = get_object_sizes(grid1)
    sizes2 = get_object_sizes(grid2)
    
    # Calculate size similarity
    size_similarity = compare_size_distributions(sizes1, sizes2)
    
    # Overall object similarity with weighted average:
    # 65% weight for count similarity, 35% weight for size similarity
    # Multiply by 100 to get score between 0 and 100
    object_similarity = ((count_similarity * 0.65) + (size_similarity * 0.35)) * 100
    
    return object_similarity

def count_objects(grid):
    """Helper function to count distinct objects in a grid"""
    visited = set()
    count = 0
    
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] != 0 and (i,j) not in visited:
                flood_fill(grid, i, j, visited)
                count += 1
    return count

def get_object_sizes(grid):
    """Helper function to get list of object sizes in grid"""
    visited = set()
    sizes = []
    
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] != 0 and (i,j) not in visited:
                size = flood_fill(grid, i, j, visited)
                sizes.append(size)
    return sorted(sizes)

def flood_fill(grid, i, j, visited):
    """Helper function to flood fill and count size of an object"""
    if (i < 0 or i >= len(grid) or 
        j < 0 or j >= len(grid[0]) or
        grid[i][j] == 0 or
        (i,j) in visited):
        return 0
        
    visited.add((i,j))
    size = 1
    
    # Check all 4 directions
    size += flood_fill(grid, i+1, j, visited)
    size += flood_fill(grid, i-1, j, visited)
    size += flood_fill(grid, i, j+1, visited)
    size += flood_fill(grid, i, j-1, visited)
    
    return size

def compare_size_distributions(sizes1, sizes2):
    """Helper function to compare two lists of object sizes"""
    if not sizes1 and not sizes2:
        return 1.0
    if not sizes1 or not sizes2:
        return 0.0
        
    # Pad shorter list with zeros
    max_len = max(len(sizes1), len(sizes2))
    sizes1 = sizes1 + [0] * (max_len - len(sizes1))
    sizes2 = sizes2 + [0] * (max_len - len(sizes2))
    
    # Calculate similarity as ratio of minimum to maximum for each pair
    similarities = []
    for s1, s2 in zip(sizes1, sizes2):
        if s1 == 0 and s2 == 0:
            similarities.append(1.0)
        else:
            similarities.append(min(s1, s2) / max(s1, s2))
            
    return sum(similarities) / len(similarities)

















def grids_colors_similarity(grid1, grid2):
    """
    Calculate similarity score based on colors present in the grids and their frequencies.
    Returns a score between 0 and 100, where:
    - 100 means identical colors and frequencies
    - 0 means completely different colors
    
    Considers:
    1. Number of colors similarity
    2. Common colors similarity 
    3. Frequency similarity of common colors
    4. Overall frequency distribution similarity
    """
    # Get unique colors and their counts from each grid
    colors1 = {}
    colors2 = {}
    
    for row in grid1:
        for cell in row:
            if cell != 0:  # Ignore background
                colors1[cell] = colors1.get(cell, 0) + 1
                
    for row in grid2:
        for cell in row:
            if cell != 0:  # Ignore background
                colors2[cell] = colors2.get(cell, 0) + 1
    
    # If both grids have no colors (empty), return 100
    if not colors1 and not colors2:
        return 100.0
        
    # If one grid has colors and other doesn't, return 0
    if not colors1 or not colors2:
        return 0.0

    # 1. Calculate number of colors similarity
    num_colors1 = len(colors1)
    num_colors2 = len(colors2)
    number_similarity = min(num_colors1, num_colors2) / max(num_colors1, num_colors2)

    # 2. Calculate common colors similarity
    common_colors = set(colors1.keys()) & set(colors2.keys())
    all_colors = set(colors1.keys()) | set(colors2.keys())
    common_color_similarity = len(common_colors) / len(all_colors)
    
    # 3. Calculate frequency similarity for common colors
    frequency_similarities = []
    for color in common_colors:
        count1 = colors1[color]
        count2 = colors2[color]
        frequency_similarities.append(min(count1, count2) / max(count1, count2))
    
    freq_similarity = (sum(frequency_similarities) / len(frequency_similarities)) if frequency_similarities else 0

    # 4. Calculate overall frequency distribution similarity
    freq_dist1 = sorted([count for count in colors1.values()], reverse=True)
    freq_dist2 = sorted([count for count in colors2.values()], reverse=True)
    
    # Pad shorter list with zeros
    max_len = max(len(freq_dist1), len(freq_dist2))
    freq_dist1 = freq_dist1 + [0] * (max_len - len(freq_dist1))
    freq_dist2 = freq_dist2 + [0] * (max_len - len(freq_dist2))
    
    # Compare frequency distributions
    dist_similarities = []
    for f1, f2 in zip(freq_dist1, freq_dist2):
        if f1 == 0 and f2 == 0:
            dist_similarities.append(1.0)
        else:
            dist_similarities.append(min(f1, f2) / max(f1, f2))
    
    dist_similarity = sum(dist_similarities) / len(dist_similarities)

    # Final similarity score with weighted average of all four components:
    # - 15% weight for number of colors similarity
    # - 35% weight for common colors similarity
    # - 25% weight for frequency similarity
    # - 25% weight for distribution similarity
    color_similarity = ((number_similarity * 0.15) + 
                       (common_color_similarity * 0.35) + 
                       (freq_similarity * 0.25) +
                       (dist_similarity * 0.25)) * 100
    
    return color_similarity













def grids_coordinate_similarity(grid1, grid2):
    """
    Calculate similarity score by comparing values at matching coordinates between two grids,
    even when dimensions differ.
        
    Args:
        grid1: First grid
        grid2: Second grid
            
    Returns:
        Float between 0-100 representing coordinate-wise similarity percentage
    """
    # Get dimensions of both grids
    rows1, cols1 = len(grid1), len(grid1[0])
    rows2, cols2 = len(grid2), len(grid2[0])
        
    # Find overlapping dimensions
    min_rows = min(rows1, rows2)
    min_cols = min(cols1, cols2)
    max_rows = max(rows1, rows2)
    max_cols = max(cols1, cols2)
        
    total_positions = max_rows * max_cols
    matching_positions = 0
        
    # Compare overlapping coordinates
    for i in range(min_rows):
        for j in range(min_cols):
            if grid1[i][j] == grid2[i][j]:
                matching_positions += 1
                    
    # Non-overlapping positions count as mismatches
    # They're already accounted for in total_positions
        
    similarity_score = (matching_positions / total_positions) * 100
    return similarity_score
    




