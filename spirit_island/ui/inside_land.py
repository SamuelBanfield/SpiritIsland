def is_point_inside_polygon(polygon, point):
    # Everything is an integer, so this is a sneaky way of avoiding being in line with a vertex
    point = [int(point[0]) + 0.5, int(point[1]) + 0.5]
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
            if x_intersection >= point[0]:
                intersections += 1

    # If the number of intersections is odd, the point is inside the polygon
    return intersections % 2 == 1
