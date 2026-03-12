import os
import argparse

from .cli.status import STATUS_ARGS
from .cli.cleanup import CLEANUP_ARGS

from . import connect
from .exceptions import CommandError

from dotenv import load_dotenv


# Global arguments for all commands
load_dotenv()
GLOBAL_ARGS = {
    ("-u", "--url"): {
        "help": "the url for the admin API of your Envoy node",
        "default": os.environ.get("ENVOY_URL", None),
        "type": str,
        "metavar": "URL",
    },
    ("-c", "--client-id"): {
        "help": "the client id of the API key to use for authentication",
        "default": os.environ.get("ENVOY_CLIENT_ID", None),
        "type": str,
        "metavar": "ID",
    },
    ("-s", "--secret"): {
        "help": "the client secret of the API key to use for authentication",
        "default": os.environ.get("ENVOY_CLIENT_SECRET", None),
        "type": str,
        "metavar": "SECRET",
    },
    ("-t", "--timeout"): {
        "help": "the number of seconds to wait for a response before timing out",
        "default": 10.0,
        "type": float,
        "metavar": "SEC",
    },
}


# Define the CLI commands and arguments
COMMANDS = {
    "status": STATUS_ARGS,
    "cleanup": CLEANUP_ARGS,
}


def main():
    parser = argparse.ArgumentParser(
        prog="envoy",
        description="API client for TRISA Envoy nodes and common commands",
        epilog="Report bugs to https://github.com/trisacrypto/pyenvoy/issues",
    )

    # Add global arguments to the parser
    for pargs, kwargs in GLOBAL_ARGS.items():
        if isinstance(pargs, str):
            pargs = (pargs,)
        parser.add_argument(*pargs, **kwargs)

    # Add subparsers for each command
    subparsers = parser.add_subparsers(title="commands", required=True)
    for cmd, cargs in COMMANDS.items():
        subparser = subparsers.add_parser(cmd, description=cargs["description"])
        for pargs, kwargs in cargs.get("args", {}).items():
            if isinstance(pargs, str):
                pargs = (pargs,)
            subparser.add_argument(*pargs, **kwargs)
        subparser.set_defaults(func=cargs["func"])

    try:
        args = parser.parse_args()
        if args.url is None or args.client_id is None or args.secret is None:
            parser.error(
                "missing required client configuration: url, client id, and/or secret"
            )

        client = connect(
            url=args.url,
            client_id=args.client_id,
            client_secret=args.secret,
            timeout=args.timeout,
        )

        args.func(client, args)
    except CommandError as e:
        parser.error(str(e))


if __name__ == "__main__":
    main()
