import argparse

from Domain.Publishers.publisher3 import run_publisher3

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Type3 Event Publisher')
    parser.add_argument('--connection-string', type=str,
                        default="amqps://username:password@hostname/vhost",
                        help='CloudAMQP connection string')

    args = parser.parse_args()
    run_publisher3(args.connection_string)
