#!/usr/bin/env python3
import time
import random
import string
import argparse
import redis

def random_string(length):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def prepopulate_keys(r, count, data_size):
    keys = []
    for i in range(count):
        key = f"key:{i}"
        r.set(key, random_string(data_size))
        keys.append(key)
    return keys

def benchmark_redis_workload(r, workload, num_ops, data_size, key_list):
    if workload == "write-heavy":
        weights = [0.8, 0.2]
    elif workload == "read-heavy":
        weights = [0.2, 0.8]
    else:
        weights = [0.5, 0.5]

    operations = ['write', 'read']
    write_count = 0
    read_count = 0
    key_counter = len(key_list)

    start_time = time.time()
    for _ in range(num_ops):
        op = random.choices(operations, weights)[0]
        if op == 'write':
            key = f"key:{key_counter}"
            r.set(key, random_string(data_size))
            key_list.append(key)
            key_counter += 1
            write_count += 1
        else:
            if key_list:
                random_key = random.choice(key_list)
                r.get(random_key)
            read_count += 1
    elapsed = time.time() - start_time
    print(f"Redis Workload '{workload}' with data size {data_size}: Executed {num_ops} operations ({write_count} writes, {read_count} reads) in {elapsed:.4f} seconds.")

def main():
    parser = argparse.ArgumentParser(description="Redis Benchmarking Script with Workload and Data Size Options")
    parser.add_argument("--workload", choices=["read-heavy", "write-heavy", "mixed"], default="mixed",
                        help="Type of workload to run")
    parser.add_argument("--num_ops", type=int, default=1000,
                        help="Number of operations to perform")
    parser.add_argument("--data_size", type=int, default=10,
                        help="Size of the random string data for each key")
    args = parser.parse_args()

    r = redis.Redis(host='localhost', port=6379, db=0)

    # Prepopulate keys for read operations.
    key_list = prepopulate_keys(r, count=100, data_size=args.data_size)
    benchmark_redis_workload(r, args.workload, args.num_ops, args.data_size, key_list)

if __name__ == "__main__":
    main()
