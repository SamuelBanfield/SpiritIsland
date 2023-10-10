def is_point_inside_polygon(polygon, point):
    intersections = 0
    
    # Iterate through each edge of the polygon
    for i in range(len(polygon)):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % len(polygon)]  # Wrap around for the last edge
        
        # Check if the point is on the same y-level as the edge
        if min(y1, y2) < point[1] <= max(y1, y2):
            if y1 == y2:
                if min(x1, x2) <= point[0] <= max(x1, x2):
                    return True
                continue 
            
            # Calculate the x-coordinate where the edge intersects the horizontal line through the point
            x_intersection = (point[1] - y1) * (x2 - x1) / (y2 - y1) + x1
            # Check if the intersection point is to the right of the point
            if x_intersection >= point[0]:
                # Increment the intersection count
                intersections += 1
    
    # If the number of intersections is odd, the point is inside the polygon
    return intersections % 2 == 1

print("!!")
if __name__ == "__main__":
    print("Hello")
    print(is_point_inside_polygon([[500, 499], [500, 600], [600, 600], [600, 500]], (0, 500)))
    