import argparse

from Domain.Publishers.publisher2 import run_publisher2

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Type2 Event Publisher')
    parser.add_argument('--connection-string', type=str,
                        default="amqps://username:password@hostname/vhost",
                        help='CloudAMQP connection string')

    args = parser.parse_args()
    run_publisher2(args.connection_string)
    