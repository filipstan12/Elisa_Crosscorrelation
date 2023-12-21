READ ME 

How to use Script: 

python ReorderScript.py --datadir /path/to/Data --savedir /path/to/saving/location


What will the script do:
Extract IBI in Range 1-5min as well es the -5 - -1min range for each patient (2)
Correlate each arr with corresponding array of pat2 and calculate max corr in +-6 datasteps of 500ms each
Generate RESULTS.csv with cc1 and cc2, which represent crosscorr of first dataframe and second dataframe, respectively. 

Tunable parameters:
start_time1 = 60000 #where to start first dataframe in respect to start of measurment
end_time1 = 300001 #where to stop first dataframe in respect to start of measurment
start_time2 = -360001 #where to start second dataframe in respect to end of measurment
end_time2 = -60000 #where to end second dataframe in respect to end of measurment 
cc_steps = 6 #lag plus/minus in datapoints
fs = 500 #sampling FQ EKG

In order to change parameters open .py in Editor and change accordingly. 





