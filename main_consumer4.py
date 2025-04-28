import argparse

from consumers.consumer4 import run_consumer4

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Type4 Event Consumer')
    parser.add_argument('--connection-string', type=str,
                        default="amqps://username:password@hostname/vhost",
                        help='CloudAMQP connection string')

    args = parser.parse_args()
    run_consumer4(args.connection_string)