import pandas as pd
import numpy as np
import argparse
import os

# divide cc results by length of input array
SCALE_CC = True

# Cross-correlation mode (options 'valid', 'same', 'full'; default is 'valid')
# https://numpy.org/doc/stable/reference/generated/numpy.convolve.html#numpy.convolve
CC_MODE = 'valid'

# max lag for cross-correlation in seconds
CC_MAX_LAG_S = 6

input_path = "IBI"
start_time1 = 60000
end_time1 = 300001
start_time2 = -360001
end_time2 = -60000
fs = 500
cc_steps = int(1000*CC_MAX_LAG_S / fs)
cc_max = []

def filelist(root):
    """Returns a fully-qualified list of filenames under root directory"""
    return [os.path.join(directory_path, f) for directory_path, directory_name,
            files in os.walk(root) for f in files if f.endswith(".csv")]

def normalize(arr):
    #normalization 1
    #norm_arr = (arr - min(arr)) / (max(arr) - min(arr))

    #normalization 2
    norm_arr = (arr - np.mean(arr))/np.std(arr)

    return norm_arr


def calc_cc_max(filename):
    df = pd.read_csv(filename, delimiter=',')

    last_ts = df.iloc[-1,0]

    # Get First time frame 1min - 5min for pat1 and pat2. Data of first pat1 is reduced by +-cc_steps Datapoints for crosscorrelation
    pat1_arr1 = np.array([i[1] for i in df.iloc if i[0] > start_time1 + cc_steps * fs and i[0] < end_time1 - cc_steps * fs])
    pat2_arr1 = np.array([i[2] for i in df.iloc if i[0] > start_time1 and i[0] < end_time1])

    # normalization of Arrays
    pat1_arr1 = normalize(pat1_arr1)
    pat2_arr1 = normalize(pat2_arr1)

    # calculate crosscorrelation
    cc1 = np.correlate(pat1_arr1, pat2_arr1, CC_MODE)
    
    # optionally scale result
    if SCALE_CC: 
        cc1 = cc1 / len(pat1_arr1)

    # Get Second time frame -5min - -1min for pat1 and pat2. Data of first pat1 is reduced by +-cc_steps Datapoints for crosscorrelation
    pat1_arr2 = np.array([i[1] for i in df.iloc if i[0] > last_ts + start_time2 + cc_steps * fs and i[0] < last_ts + end_time2 - cc_steps * fs])
    pat2_arr2 = np.array([i[2] for i in df.iloc if i[0] > last_ts + start_time2 and i[0] < last_ts + end_time2])

    # normalization of Arrays
    pat1_arr2 = normalize(pat1_arr2)
    pat2_arr2 = normalize(pat2_arr2)

    # calculate crosscorrelation
    cc2 = np.correlate(pat1_arr2, pat2_arr2, CC_MODE)

    # optionally scale result
    if SCALE_CC: 
        cc2 = cc2 / len(pat1_arr2)

    return [max(cc1), max(cc2)]

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--datadir",
        help="Directory path to IBI files",
        default=input_path,
        type=str,
    )
    parser.add_argument(
        "--savedir",
        help="where to save .csv with results",
        default="",
        type=str,
    )

    args = parser.parse_args()
    path = args.datadir
    path_save = args.savedir

    filenames = filelist(path)
    print("found", len(filenames), 'in path')

    for filename in filenames:
        cc = calc_cc_max(filename)
        cc_max.append(cc)
        print("processed file", len(cc_max), filename)

    df_cc = pd.DataFrame(cc_max, columns=["cc1", "cc2"])

    df_cc.to_csv(path_save + 'RESULTS_cc_max.csv', index=False)
    print('Code finished:', len(cc_max), 'files were cross-correlated. File saved in dir:', path_save)
