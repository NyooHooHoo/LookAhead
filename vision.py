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


def distance_from(objects, target, x):
    dists = []
    for object_ in objects:
        if object_.name == target:
            verticies = object_.bounding_poly.normalized_vertices
            dist = x - (verticies[0].x + verticies[1].x)/2
            dists.append(dist)
    if dists:
        return min(dists)
    return "not found"
        

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