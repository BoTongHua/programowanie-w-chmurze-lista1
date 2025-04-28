import argparse

from Domain.Publishers.publisher1 import run_publisher1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Type1 Event Publisher')
    parser.add_argument('--instance-id', type=str, default="1", help='Instance ID for this publisher')
    parser.add_argument('--connection-string', type=str,
                        default="amqps://username:password@hostname/vhost",
                        help='CloudAMQP connection string')

    args = parser.parse_args()
    run_publisher1(args.instance_id, args.connection_string)