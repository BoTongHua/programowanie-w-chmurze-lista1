import argparse

from Domain.Consumers.consumer3 import run_consumer3

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Type3 Event Consumer')
    parser.add_argument('--connection-string', type=str,
                        default="amqps://username:password@hostname/vhost",
                        help='CloudAMQP connection string')

    args = parser.parse_args()
    run_consumer3(args.connection_string)