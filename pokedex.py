"""Pokedex application using SIFT descriptor."""
import argparse
import csv
import cv2


IMAGE_PATH = 'dataset/{index}/{index}-{version}.png'
DATASET_PATH = 'dataset/pokemon.csv'
N_POKEMONS = 151
SIFT = cv2.xfeatures2d.SIFT_create()


def main():
    """Execute."""
    parser = argparse.ArgumentParser('pokedex using sift descriptor')
    parser.add_argument('-f', help='path to pokemon image', required=True)
    args = parser.parse_args()
    pokemon = cv2.imread(args.f)
    match = find(pokemon)
    print (read_csv(match))


def find(pokemon):
    """Find pokemon in the dataset."""
    matches = []
    for i in range(1, N_POKEMONS + 1):
        for v in range(0, 3):
            test_image = cv2.imread(IMAGE_PATH.format(index=i, version=v))
            keypoints = match(pokemon, test_image)
            if (len(keypoints) > 0):
                matches.append((i, len(keypoints)))
    return sorted(matches, key=lambda x: x[1], reverse=True)[0]


def match(pokemon, test):
    """Match input image with test images."""
    img_keypoints, img_descriptor = SIFT.detectAndCompute(pokemon, None)
    tst_keypoints, tst_descriptor = SIFT.detectAndCompute(test, None)
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(img_descriptor, tst_descriptor, k=2)
    return filter_keypoints(matches)


def filter_keypoints(matches):
    """Filter keypoints to avoid false positives."""
    keypoints_filtered = []
    for m, n in matches:
        if m.distance < 0.7*n.distance:
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
