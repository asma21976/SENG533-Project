import docker
import time
import threading
import matplotlib.pyplot as plt

def measure_container_stats(client, container_id, results, i, stop):
    stats = client.api.stats(container_id, decode=True, stream=True)
    results[i]['time'] = []
    results[i]['cpu_usage'] = []
    results[i]['mem_usage'] = []
    results[i]['disk_reads'] = []
    results[i]['disk_writes'] = []
    for stat in stats:
        if stop():
            break

        cpu_stats = stat['cpu_stats']
        memory_stats = stat['memory_stats']
        blkio_stats = stat['blkio_stats']

        # Current time
        results[i]['time'].append(time.time())

        # CPU usage
        cpu_percent = calculate_cpu_percent(cpu_stats)
        results[i]['cpu_usage'].append(cpu_percent)

        # Memory usage
        memory_usage = memory_stats['usage']
        memory_limit = memory_stats['limit']
        memory_usage_percent = memory_usage/memory_limit*100.0
        results[i]['mem_usage'].append(memory_usage_percent)

        # Disk I/O stats
        disk_stats = calculate_disk_stats(blkio_stats)
        results[i]['disk_reads'].append(disk_stats['reads'])
        results[i]['disk_writes'].append(disk_stats['writes'])

def calculate_cpu_percent(cpu_stats):
    cpu_usage = cpu_stats['cpu_usage']['total_usage']
    system_cpu_usage = cpu_stats['system_cpu_usage']
    online_cpus = len(cpu_stats['cpu_usage']['percpu_usage'])

    if 'precpu_stats' in cpu_stats:
        precpu_usage = cpu_stats['precpu_stats']['total_usage']
        precpu_system = cpu_stats['precpu_stats']['system_cpu_usage']
    else:
        precpu_usage = 0
        precpu_system = 0

    cpu_delta = cpu_usage - precpu_usage
    system_delta = system_cpu_usage - precpu_system

    if system_delta > 0 and cpu_delta > 0:
        cpu_percent = (cpu_delta / system_delta) * online_cpus * 100.0
    else:
        cpu_percent = 0.0

    return cpu_percent

def calculate_disk_stats(blkio_stats):
    disk_stats = {'reads': 0, 'writes': 0}

    for bio_entry in blkio_stats['io_service_bytes_recursive']:
        if 'Read' in bio_entry['op']:
            disk_stats['reads'] += bio_entry['value']
        elif 'Write' in bio_entry['op']:
            disk_stats['writes'] += bio_entry['value']

    return disk_stats

def plot_statistics(result_set, container_name, start_time):
    times = [time - start_time for time in result_set['time']]
    plt.plot(times, result_set['cpu_usage'], label="CPU Usage (%)")
    plt.plot(times, result_set['mem_usage'], label="Memory Usage (%)")
    plt.plot(times, result_set['disk_reads'], label="Disk reads")
    plt.plot(times, result_set['disk_writes'], label="Disk writes")
    plt.title(f'Usage stats for {container_name} container')
    plt.legend()
    plt.show()

def main():
    client = docker.from_env()
    container_ids = [container.id for container in client.containers.list()]
    container_names = [container.name for container in client.containers.list()]
    results = []
    for i in range(len(container_ids)):
        results.append({})
    threads = [None]*len(container_ids)

    stop_threads = False

    print("Starting measurement for 30 seconds...")
    start_time = int(time.time())
    
    for i in range(len(threads)):
        threads[i] = threading.Thread(target=measure_container_stats, args=(client, container_ids[i], results, i, lambda: stop_threads))
        threads[i].start()

    try:
        time.sleep(30)
    except KeyboardInterrupt:
        pass
    
    print("Stopping measurement")

    stop_threads = True;

    for thread in threads:
        thread.join()

    for i in range(len(results)):
        plot_statistics(results[i], container_names[i], start_time)


if __name__ == "__main__":
    main()