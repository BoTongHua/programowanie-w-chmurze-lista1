import argparse

from Domain.Consumers.consumer2 import run_consumer2

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Type2 Event Consumer')
    parser.add_argument('--connection-string', type=str,
                        default="amqps://username:password@hostname/vhost",
                        help='CloudAMQP connection string')

    args = parser.parse_args()
    run_consumer2(args.connection_string)
    