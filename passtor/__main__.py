from .store import Storage
from .get import get_password, store_password
from .encrypt import generate_cert, decrypt_cert
import argparse
import shlex
import getpass


def do_action(args, cert=None):
    storage = Storage(args.storage)

    if not args.password:
        args.password = getpass.getpass("password: ")

    if not cert and not args.generate_cert:
        with open(args.cert, "rb") as f:
            encrypted = f.read()

        cert = decrypt_cert(encrypted, args.password)

    if not args.key and not args.generate_cert:
        args.key = input("key: ")

    if args.get:
        print(get_password(storage, args.key, cert, args.duration))

    elif args.store:
        if not args.data:
            args.data = input("data: ")

        store_password(storage, args.key, cert, args.data)

    elif args.generate_cert:
        cert = generate_cert(args.password)
        with open(args.cert, "wb") as f:
            f.write(cert)

    return cert


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-k", "--key", help="key for stored data", action="store", required=False
    )
    parser.add_argument(
        "-p",
        "--password",
        help="password for stored data",
        action="store",
        required=False,
    )
    parser.add_argument(
        "-d", "--data", help="data to be stored", action="store", required=False
    )
    parser.add_argument(
        "--storage",
        help="storage file",
        action="store",
        required=False,
        default="data.json",
    )
    parser.add_argument(
        "--duration",
        help="duration of copied password",
        action="store",
        required=False,
        type=int,
    )
    parser.add_argument(
        "-c", "--cert", help="certificate file", action="store", default="key.key"
    )

    group = parser.add_mutually_exclusive_group()

    group.add_argument("-g", "--get", help="get stored data", action="store_true")
    group.add_argument("-s", "--store", help="store new data", action="store_true")
    group.add_argument(
        "--generate-cert", help="generate new key for storing data", action="store_true"
    )

    args = parser.parse_args()

    if any((args.store, args.get, args.generate_cert)):
        do_action(args)
    else:
        cert = None
        while True:
            in_ = input()
            input_arguments = shlex.split(in_)
            args = parser.parse_args(input_arguments)
            try:
                cert = do_action(args, cert)
            except Exception as e:
                print(e)
