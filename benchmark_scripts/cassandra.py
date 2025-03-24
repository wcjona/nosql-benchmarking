#!/usr/bin/env python3
import time
import random
import string
import argparse
import uuid
from cassandra.cluster import Cluster

def random_string(length):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def setup_keyspace_and_table(session):
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS benchmark_keyspace
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 1};
    """)
    session.execute("USE benchmark_keyspace;")
    session.execute("""
        CREATE TABLE IF NOT EXISTS test_table (
            id uuid PRIMARY KEY,
            name text,
            value int
        );
    """)

def prepopulate_data(session, count, data_size):
    inserted_ids = []
    insert_query = session.prepare("INSERT INTO test_table (id, name, value) VALUES (?, ?, ?)")
    for _ in range(count):
        record_id = uuid.uuid4()
        session.execute(insert_query, (record_id, random_string(data_size), random.randint(1, 1000)))
        inserted_ids.append(record_id)
    return inserted_ids

def benchmark_cassandra_workload(session, workload, num_ops, data_size, id_list):
    if workload == "write-heavy":
        weights = [0.8, 0.2]
    elif workload == "read-heavy":
        weights = [0.2, 0.8]
    else:
        weights = [0.5, 0.5]

    operations = ['write', 'read']
    write_count = 0
    read_count = 0

    insert_query = session.prepare("INSERT INTO test_table (id, name, value) VALUES (?, ?, ?)")
    start_time = time.time()
    for _ in range(num_ops):
        op = random.choices(operations, weights)[0]
        if op == 'write':
            new_id = uuid.uuid4()
            session.execute(insert_query, (new_id, random_string(data_size), random.randint(1, 1000)))
            id_list.append(new_id)
            write_count += 1
        else:
            if id_list:
                random_id = random.choice(id_list)
                session.execute("SELECT * FROM test_table WHERE id = %s", (random_id,))
            read_count += 1
    elapsed = time.time() - start_time
    print(f"Cassandra Workload '{workload}' with data size {data_size}: Executed {num_ops} operations ({write_count} writes, {read_count} reads) in {elapsed:.4f} seconds.")

def main():
    parser = argparse.ArgumentParser(description="Cassandra Benchmarking Script with Workload and Data Size Options")
    parser.add_argument("--workload", choices=["read-heavy", "write-heavy", "mixed"], default="mixed",
                        help="Type of workload to run")
    parser.add_argument("--num_ops", type=int, default=1000,
                        help="Number of operations to perform")
    parser.add_argument("--data_size", type=int, default=10,
                        help="Size of the random string data in each record")
    args = parser.parse_args()

    cluster = Cluster(['127.0.0.1'])  # Adjust contact points as needed.
    session = cluster.connect()
    setup_keyspace_and_table(session)

    # Prepopulate data and store the inserted ids.
    id_list = prepopulate_data(session, count=100, data_size=args.data_size)
    benchmark_cassandra_workload(session, args.workload, args.num_ops, args.data_size, id_list)

    session.shutdown()
    cluster.shutdown()

if __name__ == "__main__":
    main()
