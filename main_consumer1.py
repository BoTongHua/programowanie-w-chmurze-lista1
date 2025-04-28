import argparse

from consumers.consumer1 import run_consumer1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Type1 Event Consumer')
    parser.add_argument('--instance-id', type=str, default="1", help='Instance ID for this consumer')
    parser.add_argument('--connection-string', type=str,
                        default="amqps://username:password@hostname/vhost",
                        help='CloudAMQP connection string')

    args = parser.parse_args()
    run_consumer1(args.instance_id, args.connection_string)
