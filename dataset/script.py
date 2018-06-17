import os
import cv2

# def main():
    # idx = 15
    # for i in range(0, 10):
    # for p in range(1, 30):
    #     img = cv2.imread('pokemon/{p}.png'.format(p=p))
    #     cv2.imwrite('{p}/{p}-{idx}.png'.format(p=p, idx=idx), img)
        # idx += 1

# def main():
#     for filename in os.listdir('dd'):
#         img = cv2.imread('dd/' + str(filename), 0)
#         img = cv2.resize(img, (256,256), interpolation = cv2.INTER_CUBIC)
#         filename = filename.split(' - ')[0]
#         cv2.imwrite('{f}/{f}-13.png'.format(f=filename), img)

# def main():
#     idx = 8
#     i = 15
#     nome = 'wartortle'
#     for filename in os.listdir(nome):
#         img = cv2.imread(nome + '/' + filename)
#         cv2.imwrite('{idx}/{idx}-{i}.png'.format(idx=idx, i=i), img)
#         i += 1

# def main():
#     idx = 100
#     for i in range(87, 152):
#         os.remove('{i}/{i}-{idx}.png'.format(i=i, idx=idx))
#         idx += 1

if __name__ == '__main__':
    main()
