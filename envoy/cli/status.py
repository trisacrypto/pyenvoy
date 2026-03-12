"""
This module implements the `status` command for the `envoy` CLI.
"""

import json


def status(client, args):
    status = client.status()

    if args.output == "json":
        print(json.dumps(status, indent=2))
    elif args.output == "text":
        print(f"Status:  {status['status']}")
        print(f"Uptime:  {status['uptime']}")
        print(f"Version: {status['version']}")
    else:
        print(status["status"])


STATUS_ARGS = {
    "description": "reports the status of your Envoy node",
    "func": status,
    "args": {
        ("-o", "--output"): {
            "help": "the output format to use",
            "default": "json",
            "type": str,
            "choices": ["json", "text"],
        },
    },
}
