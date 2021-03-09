from pathlib import Path
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

from smoothdiff.smdiff import smdiff


if __name__ == "__main__":
    # vladimir noise
    parent_path = Path(__file__).parents[1].joinpath('input_data')

    parent_path = parent_path.joinpath('кпд')
    path = parent_path.joinpath('кпд.txt')

    x = np.array([])
    fyy = np.array([])
    with open(path) as f:
        f.readline()
        f.readline()
        for line in f:
            split = line.strip().split('\t', 2)
            x_item = datetime.strptime(split[0], "%d.%m.%Y %H:%M:%S")
            x = np.append(x, x_item)
            fyy = np.append(fyy, float(split[1]))

    # vladimir noise handling-------------------------------

    # # to make pickle
    # import pickle

    # # to write
    # data_save = {
    #     'x': x,
    #     'fyy': fyy
    # }
    # with open(parent_path.joinpath('кпд.bin'), 'wb') as f:
    #     pickle.dump(data_save, f)

    # # to read
    # with open(parent_path.joinpath('кпд.bin'), 'rb') as f:
    #     data = pickle.load(f)
    # x = data['x']
    # fyy = data['fyy']

    x_full = x.copy()
    fyy_full = fyy.copy()

    x = x[100000:]
    fyy = fyy[100000:]

    # make x in hours
    x_hr = np.array([])
    dt_list = (x - x[0]).tolist()
    x_hr = np.concatenate((
        x_hr, 
        [dt.days * 24 + dt.seconds / 3600 for dt in dt_list]
    ))

    x = x_hr
    fyy *= 1.01325  # atm -> bars
    # ------------------------------------------------------

    fdata = (x, fyy)

    nz = 8  # num of finite elements
    wz = 1e-8  # weight of regularisation
    zdata = (nz, wz)

    fs, Dfs, err, curv, z, U = smdiff(fdata, zdata)

    plt.figure(1)
    plt.plot(x, fs)

    plt.figure(2)
    plt.plot(x, fyy, '*r')

    plt.figure(3)
    plt.plot(x, fyy - fs, '*r')

    plt.figure(4)
    plt.plot(x, 0.3 * (fyy - fs), '*r')

    plt.show()

    # write noise to file
    import pandas as pd
    res_str = pd.DataFrame({
            't,hr': x,
            'p,bars': 0.3 * (fyy - fs)
            }).to_csv(sep='\t', index=False, line_terminator='\n')

    with open(parent_path.joinpath('шум_cut.txt'), "w") as f:
        f.write(res_str)
