"""Pokedex application using SIFT descriptor."""
import argparse
import csv
import cv2
import os
import pickle


IMAGE_PATH_OS = 'dataset/{index}/{img}'
DATASET_PATH = 'dataset/pokemon.csv'
N_POKEMONS = 151
SIFT = cv2.xfeatures2d.SIFT_create()


def main():
    """Execute."""
    parser = argparse.ArgumentParser('pokedex using sift descriptor')
    parser.add_argument('-f', help='path to pokemon image', required=True)
    parser.add_argument('-n',
                        help='reload dataset from images',
                        action='store_true')
    args = parser.parse_args()
    test_images = []
    if os.path.exists('dataset.bin') and not args.n:
        keypoints_bin = open('dataset.bin', mode='rb')
        test_images = pickle.load(keypoints_bin)
    else:
        test_images = get_keypoints()
    pokemon = cv2.imread(args.f)
    match = find(pokemon, test_images)
    print (read_csv(match))


def find(pokemon, test_images):
    """Find pokemon in the dataset."""
    matches = []
    img_keypoints, img_descriptor = SIFT.detectAndCompute(pokemon, None)
    for test_image in test_images:
        keypoints = match(img_descriptor, test_image['descriptor'])
        if (len(keypoints) > 0):
            matches.append((test_image['pokemon'], len(keypoints)))
    return sorted(matches, key=lambda x: x[1], reverse=True)[0]


def get_keypoints():
    """Get descriptors directly from images."""
    keypoints_list = []
    for i in range(1, N_POKEMONS + 1):
        for filename in os.listdir('dataset/{i}/'.format(i=i)):
            image_path = IMAGE_PATH_OS.format(index=i, img=filename)
            test_image = cv2.imread(image_path)
            keypoints, descriptor = SIFT.detectAndCompute(test_image, None)
            img_descriptor = {
                'path': image_path,
                'descriptor': descriptor,
                'pokemon': i
            }
            keypoints_list.append(img_descriptor)
    pickle.dump(keypoints_list, open('dataset.bin', 'wb'))
    return keypoints_list


def match(pokemon, test):
    """Match input image with test images."""
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(pokemon, test, k=2)
    return filter_keypoints(matches)


def filter_keypoints(matches):
    """Filter keypoints to avoid false positives."""
    keypoints_filtered = []
    for m, n in matches:
        if m.distance < 0.3*n.distance:
            keypoints_filtered.append([m])
    return keypoints_filtered


def read_csv(match):
    """Read pokemon data in the dataset csv."""
    with open(DATASET_PATH, mode='r') as dataset:
        reader = csv.reader(dataset)
        for row in reader:
            if (row[0] == str(match[0])):
                return row[1]
    return 'Pokemon not found.'


if __name__ == '__main__':
    main()
