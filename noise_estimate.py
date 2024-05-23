import numpy as np
import cv2
import os
import glob
import pickle as pkl


def C(x, y):
    if x > y // 2:
        x = y - x

    mul = 1
    div = 1
    for _ in range(x):
        mul *= (y - _)
        div *= (_ + 1)
    
    return int(mul / div)

def factor(x):
    sum = 1
    for _ in range(x):
        sum += C(_, x)**2

    return sum


def delta(x):
    return x[:-1, ...] - x[1:, ...]

def nabla(x, n):
    for i in range(n):
        x = delta(x)
    return x


def test_on_dataset(path=r'D:\reading\data\datasets\MIT-train-test\traingt', out_name='res_dict'):
    np.random.seed(0)
    image_paths = glob.glob(os.path.join(path, '*.png'))
    sigmas = [_ for _ in range(0, 50, 5)]
    pi = np.pi
    res_dict = dict()
    for sigma in sigmas:
        img_res_list = []
        for path in image_paths:
            image = cv2.imread(path)
            for i in range(100):
                noise = sigma * np.random.randn(*image.shape)

                n_inp = noise + image
                n_inp = n_inp / 255.0

                b = delta(n_inp.copy())
                s_1 = np.mean(abs(b)) * np.sqrt(pi) /2 * 255.0

                # print(s_1)

                c = nabla(n_inp.copy(), 2)
                s_2 = np.mean(abs(c)) * np.sqrt(pi / 2) / np.sqrt(6) * 255.0


                c = nabla(n_inp.copy(), 3)
                s_3 = np.mean(abs(c)) * np.sqrt(pi / 2) / np.sqrt(20) * 255.0

                
                d = nabla(n_inp.copy(), 4)
                s_4 = np.mean(abs(d)) * np.sqrt(pi / 2) / np.sqrt(70)

                
                e = nabla(n_inp.copy(), 5)
                s_5 = np.mean(abs(e)) * np.sqrt(pi / 2) / np.sqrt(252)

                
                e = nabla(n_inp.copy(), 6)
                s_6 = np.mean(abs(e)) * np.sqrt(pi / 2) / np.sqrt(factor(6))

                
                e = nabla(n_inp.copy(), 10)
                s_10 = np.mean(abs(e)) * np.sqrt(pi / 2) / np.sqrt(184756)

                img_res_list.append(np.array([s_1, s_2, s_3, s_4, s_5, s_6, s_10])[None, :])
                img_res_list.append(np.array([s_1, s_2, s_3])[None, :])

        res = np.concatenate(img_res_list, axis=0)
        res = np.mean(res, axis=0)
        print(res)
        res_dict[sigma] = res

    print(res_dict)
    with open(f'{out_name}.pkl', 'wb') as f:
        pkl.dump(res_dict, f)



test_on_dataset(r'D:\Experiments\LowLight\codes\noise_estimation\mine\mit', 'res_dict')
