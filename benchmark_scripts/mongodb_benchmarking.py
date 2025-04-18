#!/usr/bin/env python3
import time
import random
import string
import argparse
from pymongo import MongoClient

def random_string(length):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def prepopulate_collection(collection, count, data_size):
    docs = [{"name": random_string(data_size), "value": random.randint(1, 1000)} for _ in range(count)]
    collection.insert_many(docs)

def benchmark_mongodb_workload(collection, workload, num_ops, data_size):
    if workload == "write":
        weights = [1, 0]
    elif workload == "read":
        weights = [0, 1]
    else:  # mixed
        weights = [0.5, 0.5]

    operations = ['write', 'read']
    write_count = 0
    read_count = 0

    start_time = time.time()
    for _ in range(num_ops):
        op = random.choices(operations, weights)[0]
        if op == 'write':
            doc = {"name": random_string(data_size), "value": random.randint(1, 1000)}
            collection.insert_one(doc)
            write_count += 1
        else:
            # Read: randomly sample one document.
            list(collection.aggregate([{"$sample": {"size": 1}}]))
            read_count += 1
    elapsed = time.time() - start_time
    print(f"MongoDB Workload '{workload}' with data size {data_size}: Executed {num_ops} operations ({write_count} writes, {read_count} reads) in {elapsed:.4f} seconds.")

def main():
    parser = argparse.ArgumentParser(description="MongoDB Benchmarking Script with Workload and Data Size Options")
    parser.add_argument("--workload", choices=["read", "write", "mixed"], default="mixed",
                        help="Type of workload to run")
    parser.add_argument("--num_ops", type=int, default=1000,
                        help="Number of operations to perform")
    parser.add_argument("--data_size", type=int, default=10,
                        help="Size of the random string data in each document")
    args = parser.parse_args()

    client = MongoClient("mongodb://192.168.219.129:27017/")
    db = client["benchmark_db"]
    collection = db["test_collection"]
    # Clear previous test data.
    collection.delete_many({})

    # Prepopulate baseline data.
    prepopulate_collection(collection, count=100, data_size=args.data_size)
    benchmark_mongodb_workload(collection, args.workload, args.num_ops, args.data_size)

if __name__ == "__main__":
    main()
