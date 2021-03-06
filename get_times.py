#!/usr/bin/env python3

import datetime
import sys
import os

if (len(sys.argv) != 2):
   print('Pass name of the directory with pgn files generated with \'get_archives.py\' script')
   exit(0)

remaining_times = ['','']
moves = [0, 0]
month_time_seconds = [0,0,0] # bullet, blitz, rapid
total_time_seconds = [0,0,0] # bullet, blitz, rapid
added_time = 0
games_played = [0,0,0]       # bullet, blitz, rapid

dir_name = sys.argv[1]
files = os.listdir(dir_name)

def sec_to_date(seconds):
   return str(datetime.timedelta(seconds=seconds)).split('.')[0]

for file_name in files:
   with open(dir_name + "/" + file_name, encoding = 'utf-8') as f:
      for line in f:
         if (line.find('TimeControl') != -1):
            time_control_str = line.split("\"")[1]
            if (time_control_str.find('1/') != -1):
               time_control = -1
            elif (time_control_str.find('+') != -1):
               time_control = int(time_control_str.split('+')[0])
            else:
               time_control = int(time_control_str)

         if (line[0] == '1'):
            times = line.split("]}")
            if (len(times) >= 3):
               remaining_times[0] = (times[-2].split(" ")[-1])
               remaining_times[1] = (times[-3].split(" ")[-1])

               h,m,s = remaining_times[0].split(':')
               remaining_times[0] = float(datetime.timedelta(hours=int(h),minutes=int(m),seconds=float(s)).total_seconds())

               h,m,s = remaining_times[1].split(':')
               remaining_times[1] = float(datetime.timedelta(hours=int(h),minutes=int(m),seconds=float(s)).total_seconds())

               time_seconds = 2*time_control - remaining_times[0] - remaining_times[1]

               if (added_time != 0):
                  moves[0] = int(times[-2].split('.')[0])
                  moves[1] = int(times[-3].split('.')[0])
                  time_seconds += added_time * (moves[0] + moves[1])

               if (time_control > 0):
                  if (time_control < 180):
                     games_played[0] += 1
                     month_time_seconds[0] += time_seconds
                  elif (time_control < 600):
                     games_played[1] += 1
                     month_time_seconds[1] += time_seconds
                  else:
                     games_played[2] += 1
                     month_time_seconds[2] += time_seconds

   print(file_name.split(".")[0] + ": " + str(datetime.timedelta(seconds=sum(month_time_seconds))).split('.')[0])
   for i in range(3):
      total_time_seconds[i] += month_time_seconds[i]
   month_time_seconds = [0,0,0]

print("\nGames played: " + str(sum(games_played)))
print("\nBullet: " + str(games_played[0]) + " games, " + str(datetime.timedelta(seconds=total_time_seconds[0])).split('.')[0])
print("Blitz: " + str(games_played[1]) + " games, " + sec_to_date(total_time_seconds[1]))
print("Rapid: " + str(games_played[2]) + " games, " + sec_to_date(total_time_seconds[2]))
print("\nTotal time: " + sec_to_date(sum(total_time_seconds)))