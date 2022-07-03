#!/usr/bin/env python3

import datetime
import sys
import os

if (len(sys.argv) != 2):
   print('Pass name of the directory with pgn files generated with \'get_archives.py\' script')
   exit(0)

remaining_times = ['','']
moves = [0, 0]
month_time_seconds = 0
total_time_seconds = 0
added_time = 0

dir_name = sys.argv[1]
files = os.listdir(dir_name)

for file_name in files:
   with open(dir_name + "/" + file_name, encoding = 'utf-8') as f:
      for line in f:
         if (line.find('TimeControl') != -1):
            time_control_str = line.split("\"")[1]
            if (time_control_str.find('+') != -1):
               time_control = int(time_control_str.split('+')[0])
               added_time = int(time_control_str.split('+')[1])
            else:
               time_control = int(time_control_str)
               added_time = 0

         if (line[0] == '1'):
            times = line.split("]}")
            remaining_times[0] = (times[-2].split(" ")[-1])
            remaining_times[1] = (times[-3].split(" ")[-1])

            h,m,s = remaining_times[0].split(':')
            remaining_times[0] = float(datetime.timedelta(hours=int(h),minutes=int(m),seconds=float(s)).total_seconds())

            h,m,s = remaining_times[1].split(':')
            remaining_times[1] = float(datetime.timedelta(hours=int(h),minutes=int(m),seconds=float(s)).total_seconds())

            month_time_seconds += 2*time_control - remaining_times[0] - remaining_times[1]

            if (added_time != 0):
               moves[0] = int(times[-2].split('.')[0])
               moves[1] = int(times[-3].split('.')[0])
               month_time_seconds += added_time * (moves[0] + moves[1])

   print(file_name.split(".")[0] + ": " + str(datetime.timedelta(seconds=month_time_seconds)).split('.')[0])
   total_time_seconds += month_time_seconds
   month_time_seconds = 0

print("\nTotal time: " + str(datetime.timedelta(seconds=total_time_seconds)).split('.')[0])