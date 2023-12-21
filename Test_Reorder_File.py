import pandas as pd
import numpy as np
import csv
import os
import matplotlib.pyplot as plt

path = "IBI"
start_time1 = 60000
end_time1 = 300001
start_time2 = -360001
end_time2 = -60000
cc_steps = 6
fs = 500
cc_max = []

def filelist(root):
    """Returns a fully-qualified list of filenames under root directory"""
    return [os.path.join(directory_path, f) for directory_path, directory_name,
            files in os.walk(root) for f in files if f.endswith(".csv")]

def calc_cc_max(filename):
    df = pd.read_csv(filename, delimiter=',')
    #print(df)
    last_ts = df.iloc[-1,0]

    # Get First time frame 1min - 5min for pat1 and pat2. Data of first pat1 is reduced by +-cc_steps Datapoints for crosscorrelation
    pat1_arr1 = np.array([i[1] for i in df.iloc if i[0] > start_time1 + cc_steps * fs and i[0] < end_time1 - cc_steps * fs])
    pat2_arr1 = np.array([i[2] for i in df.iloc if i[0] > start_time1 and i[0] < end_time1])
    # normalization of Arrays
    pat1_arr1 = (pat1_arr1 - min(pat1_arr1)) / (max(pat1_arr1) - min(pat1_arr1))
    pat2_arr1 = (pat2_arr1 - min(pat2_arr1)) / (max(pat2_arr1) - min(pat2_arr1))
    # calculate crosscorrelation
    cc1 = np.correlate(pat1_arr1, pat2_arr1)
    cc1 = cc1 / len(pat1_arr1)

    #print(last_ts + start_time2, last_ts + end_time2)

    # Get Second time frame -5min - -1min for pat1 and pat2. Data of first pat1 is reduced by +-cc_steps Datapoints for crosscorrelation
    pat1_arr2 = np.array([i[1] for i in df.iloc if i[0] > last_ts + start_time2 + cc_steps * fs and i[0] < last_ts + end_time2 - cc_steps * fs])
    pat2_arr2 = np.array([i[2] for i in df.iloc if i[0] > last_ts + start_time2 and i[0] < last_ts + end_time2])
    # normalization of Arrays
    pat1_arr2 = (pat1_arr2 - min(pat1_arr2)) / (max(pat1_arr2) - min(pat1_arr2))
    pat2_arr2 = (pat2_arr2 - min(pat2_arr2)) / (max(pat2_arr2) - min(pat2_arr2))
    # calculate crosscorrelation
    cc2 = np.correlate(pat1_arr2, pat2_arr2)
    cc2 = cc2 / len(pat1_arr2)

    plot_cc(pat1_arr1, pat2_arr1, pat1_arr2, pat2_arr2, cc1, cc2)

    return [max(cc1), max(cc2)]

def plot_cc(pat1_arr1, pat2_arr1, pat1_arr2, pat2_arr2, cc1, cc2):
    lag = np.arange(-6,7)
    plot1 = plt.subplot2grid((2, 3), (0, 0), colspan=2)
    plot2 = plt.subplot2grid((2, 3), (1, 0), colspan=2)
    plot3 = plt.subplot2grid((2, 3), (0, 2))
    plot4 = plt.subplot2grid((2, 3), (1, 2))

    plot1.plot(np.arange(0, len(pat1_arr1)/2,0.5), pat1_arr1)
    plot1.plot(np.arange(0, len(pat2_arr1)/2, 0.5), pat2_arr1)
    plot1.set_title('First Range')

    plot3.plot(lag, cc1)
    plot3.set_title('cc1')

    plot2.plot(np.arange(0, len(pat1_arr2) / 2, 0.5), pat1_arr2)
    plot2.plot(np.arange(0, len(pat2_arr2) / 2, 0.5), pat2_arr2)
    plot2.set_title('Second Range')

    plot4.plot(lag, cc2)
    plot4.set_title('cc2')

    plt.tight_layout()
    plt.show()
    return

if __name__ == "__main__":
    filenames = filelist("IBI")
    print("found", len(filenames), 'in path')

    for filename in filenames:
        cc = calc_cc_max(filename)
        cc_max.append(cc)
        print("processed file", len(cc_max))

    df_cc = pd.DataFrame(cc_max, columns=["cc1", "cc2"])
    #print(df_cc)

    df_cc.to_csv('RESULTS_cc_max.csv')
    print('Code finished:', len(cc_max), 'files were cross-correlated. File saved in dir:')