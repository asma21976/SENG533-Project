import sys
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def parse_output(output, filename):
  times = []
  response_times = []
  num_successes = 0
  num_requests = 0

  print("start")
  for row in output: 
    if row['success'] == "true":
      num_successes += 1
      times.append(int(row['timeStamp'])/1000)
      response_times.append(int(row['elapsed']))
    num_requests += 1
  print("end reading")

  # Adjust times to start at 0
  times = [time - min(times) for time in times]
  print("end adjusting time")

  # Sort times and response times to be in chronological order
  times, response_times = zip(*sorted(zip(times, response_times)))

  print(f'Error rate: {(1 - num_successes/num_requests) * 100} %')
  print(f'Average response time: {np.average(response_times)} ms')
  print(f'Median response time: {np.median(response_times)} ms')
  print(f'Longest response time: {max(response_times)} ms')
  print(f'Shortest response time: {min(response_times)} ms')

  # Create or load the DataFrame
  try:
      df = pd.read_csv("combined_response_times.csv")
  except FileNotFoundError:
      df = pd.DataFrame()

  # NEED to pad the columns in case of different # of samples captured over 10 minutes
  max_length = max(len(response_times), len(df))
  new_df = pd.DataFrame()

  # Pad existing columns with -1 values
  for column in df.columns:
    if column != filename:
      padding_length = max_length - len(df[column].tolist())
      padding_values = [-1] * padding_length
      new_df[column] = df[column].tolist() + padding_values

  new_df[filename] = list(response_times) + [-1] * (max_length - len(response_times))

  # Save the new df to the old CSV
  new_df.to_csv("results/combined_response_times.csv", index=False)

  plt.title("Response times of requests over duration of test")
  plt.xlabel("Time (seconds)")
  plt.ylabel("Response time (milliseconds)")
  plt.plot(times, response_times)
  plt.show()

def main():
  if len(sys.argv) < 2:
    print("Error: Log file name must be supplied as a command-line argument.")
    exit(1)
  with open(sys.argv[1]) as csv_file:
    csv_reader = csv.DictReader(csv_file)
    parse_output(csv_reader, sys.argv[1])

if __name__ == "__main__":
  main()