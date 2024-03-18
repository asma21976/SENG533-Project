import sys
import csv
import matplotlib.pyplot as plt
import numpy as np

def parse_output(output):
  times = []
  response_times = []
  num_successes = 0
  num_requests = 0

  for row in output: 
    if row['success'] == "true":
      num_successes += 1
      times.append(int(row['timeStamp'])/1000)
      response_times.append(int(row['elapsed']))
    num_requests += 1
  
  # Adjust times to start at 0
  times = [time - min(times) for time in times]
  # Sort times and response times to be in chronological order
  times, response_times = zip(*sorted(zip(times, response_times)))
  
  print(f'Error rate: {(1 - num_successes/num_requests) * 100} %')
  print(f'Average response time: {np.average(response_times)} ms')
  print(f'Median response time: {np.median(response_times)} ms')
  print(f'Longest response time: {max(response_times)} ms')
  print(f'Shortest response time: {min(response_times)} ms')

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
    parse_output(csv_reader)

if __name__ == "__main__":
  main()