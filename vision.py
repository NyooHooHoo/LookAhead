def localize_objects(path):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """
    from google.cloud import vision

    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    objects = client.object_localization(image=image).localized_object_annotations

    return objects


def looking_at(objects, x, y):
    areas, names = [], []
    for object_ in objects:
        verticies = object_.bounding_poly.normalized_vertices
        x1, x2, y1, y2 = verticies[0].x, verticies[1].x, verticies[1].y, verticies[2].y
        if x1 <= x and x <= x2 and y1 <= y and y <= y2:
            areas.append((x2-x1)*(y2-y1))
            names.append(object_.name)
    if names:
        return names[areas.index(min(areas))]
    return "not found"

N = 100
# choose a number that will never appear
previous_N_closest = [-69420 for _ in range(0, N)]

# moves back all of the elements in previous_N_closest, returns rolling average
def move_back_N(dir):
    for i in range(0, N - 1):
        previous_N_closest[i] = previous_N_closest[i + 1]
    previous_N_closest[N - 1] = dir
    total_counted, sum = 0, 0
    for i in range(0, N):
        if previous_N_closest[i] != -69420:
            total_counted += 1
            sum += previous_N_closest[i]
    if total_counted == 0:
        return 0
    else:
        return sum / total_counted

# custom comparator for sorting by name of the identified object
def comp(param):
    return param.name

# finds the closest x distance - returns the rolling average
# -69420 means nothing's there, x < 0 means turn left, 0 < x means turn right, perfect 0 means you're staring at it
def x_distance(objects, target, x):
    sorted(objects, key=comp)

    # first index of an object that matches the target
    ind = -1

    for i, object_ in objects:
        if object_.name == target:
            ind = i
            break
    
    if ind == -1:
        return move_back_N(-69420)
    else:
        verticies = objects[ind].bounding_poly.normalized_vertices
        # if it's between, it's just zero
        cur_dist = 0
        if x < verticies[0].x:
            return abs(x - verticies[0].x)
        elif verticies[1].x < x:
            return abs(x - verticies[1].x)
        return move_back_N(cur_dist)


def detect_obstacle(objects):
    areas, names = [], []
    for object_ in objects:
        verticies = object_.bounding_poly.normalized_vertices
        x1, x2, y1, y2 = verticies[0].x, verticies[1].x, verticies[1].y, verticies[2].y
        areas.append((x2-x1)*(y2-y1))
        names.append(object_.name)
    if names:
        if max(areas) >= 0.25:
            return names[areas.index(max(areas))]
    return "not found"


def show_boxes(objects):
    print(f"Number of objects found: {len(objects)}")
    for object_ in objects:
        print(f"\n{object_.name} (confidence: {object_.score})")
        print("Normalized bounding polygon vertices: ")
        for vertex in object_.bounding_poly.normalized_vertices:
            print(f" - ({vertex.x}, {vertex.y})")


if __name__ == "__main__":
    objects = localize_objects("images/test2.jpg")
    print(looking_at(objects, 0.95, 0.75))