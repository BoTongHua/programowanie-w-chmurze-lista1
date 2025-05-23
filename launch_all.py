import multiprocessing
import argparse

from Domain.Consumers.consumer1 import run_consumer1
from Domain.Consumers.consumer2 import run_consumer2
from Domain.Consumers.consumer3 import run_consumer3
from Domain.Consumers.consumer4 import run_consumer4
from Domain.Publishers.publisher1 import run_publisher1
from Domain.Publishers.publisher2 import run_publisher2
from Domain.Publishers.publisher3 import run_publisher3


def launch_all_components(connection_string):
    """Launch all components of the message broker system"""
    processes = []

    # Launch Type1 Publishers (3 instances)
    for i in range(1, 4):
        p = multiprocessing.Process(
            target=run_publisher1,
            args=(str(i), connection_string)
        )
        p.start()
        processes.append(p)

    # Launch Type2 publisher
    p = multiprocessing.Process(
        target=run_publisher2,
        args=(connection_string,)
    )
    p.start()
    processes.append(p)

    # Launch Type3 publisher
    p = multiprocessing.Process(
        target=run_publisher3,
        args=(connection_string,)
    )
    p.start()
    processes.append(p)

    # Launch Type1 Consumers (2 instances)
    for i in range(1, 3):
        p = multiprocessing.Process(
            target=run_consumer1,
            args=(str(i), connection_string)
        )
        p.start()
        processes.append(p)

    # Launch Type2 consumer
    p = multiprocessing.Process(
        target=run_consumer2,
        args=(connection_string,)
    )
    p.start()
    processes.append(p)

    # Launch Type3 consumer
    p = multiprocessing.Process(
        target=run_consumer3,
        args=(connection_string,)
    )
    p.start()
    processes.append(p)

    # Launch Type4 consumer
    p = multiprocessing.Process(
        target=run_consumer4,
        args=(connection_string,)
    )
    p.start()
    processes.append(p)

    # Wait for all processes to finish
    try:
        for p in processes:
            p.join()
    except KeyboardInterrupt:
        print("Stopping all components...")
        for p in processes:
            p.terminate()
            p.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Launch all message broker system components')
    parser.add_argument('--connection-string', type=str,
                        default="amqps://username:password@hostname/vhost",
                        help='CloudAMQP connection string')

    args = parser.parse_args()
    launch_all_components(args.connection_string)