import collections

import numpy as np

import advent_tools


def main():
    data = advent_tools.read_all_integers()
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def run_part_1(data):
    return sum(len(faces) for faces in (get_all_faces(data)))


def get_all_faces(data):
    faces = [set() for _ in range(3)]
    for line in data:
        for i, face_set in enumerate(faces):
            add_or_remove(face_set, tuple(line))
            other_face = list(line)
            other_face[i] += 1
            add_or_remove(face_set, tuple(other_face))
    return faces


def add_or_remove(faces, plane):
    if plane in faces:
        faces.remove(plane)
    else:
        faces.add(plane)


def run_part_2(data):
    droplet = get_droplet_voxels(data)
    outside = fill_space(droplet, (0, 0, 0))
    outside_faces = get_all_faces(zip(*np.where(outside)))
    remove_edge_faces(outside_faces)
    return sum(len(faces) for faces in outside_faces)


def get_droplet_voxels(data):
    droplet = np.zeros(tuple(max(coords) + 3 for coords in zip(*data)), dtype=bool)
    for voxel in data:
        droplet[tuple(coord + 1 for coord in voxel)] = True
    return droplet


def fill_space(droplet, start_voxel):
    filled = np.zeros_like(droplet)
    to_consider = collections.deque([start_voxel])
    while to_consider:
        voxel = to_consider.popleft()
        if (all(0 <= x < max_val for x, max_val in zip(voxel, droplet.shape))
                and not filled[voxel] and not droplet[voxel]):
            filled[voxel] = True
            to_consider.extend(add_to_each(voxel, 1))
            to_consider.extend(add_to_each(voxel, -1))
    return filled


def add_to_each(point, add):
    for i in range(len(point)):
        plus_point = list(point)
        plus_point[i] += add
        yield tuple(plus_point)


def remove_edge_faces(all_faces):
    for i, plane_faces in enumerate(all_faces):
        min_val = min(face[i] for face in plane_faces)
        max_val = max(face[i] for face in plane_faces)
        edge_faces = [
            face for face in plane_faces if face[i] == min_val or face[i] == max_val
        ]
        plane_faces.difference_update(edge_faces)


if __name__ == '__main__':
    main()
