"""
This module implements the `cleanup` command for the `envoy` CLI.
"""
import re

from .prompt import confirm
from ..exceptions import CommandError, NotFound


def is_ulid(value: str) -> bool:
    return re.match(r'^[0-9A-HJ-NP-TV-Z]{26}$', value) is not None


def cleanup(client, args):
    # Get Counterparty ID and Confirm Counterparty Selection
    counterparty_id = None
    if is_ulid(args.counterparty):
        try:
            counterparty = client.counterparties.detail(args.counterparty)
            counterparty_id = counterparty["id"]
        except NotFound:
            raise CommandError(f"counterparty '{args.counterparty}' not found")
    else:
        counterparty = client.counterparties.search(args.counterparty)
        if len(counterparty) == 0:
            raise CommandError(f"counterparty '{args.counterparty}' not found")
        else:
            counterparty = counterparty[0]
            counterparty_id = counterparty["id"]

        if not args.yes and not confirm(f"continue with {counterparty['name']} ({counterparty_id})?"):
            raise CommandError("could not identify counterparty")

        counterparty_id = counterparty["id"]

    # Get transactions and confirm transaction selection
    # TODO: use `/v1/counterparties/{counterparty_id}/transfers` when implemented
    # TODO: handle pagination when implemented
    transactions = client.transactions.list(
        params={
            "status": args.status,
        }
    )

    # Filter transactions by counterparty and status
    transactions = [
        tx for tx in transactions
        if tx["counterparty_id"] == counterparty_id and tx["status"] == args.status
    ]

    # Confirm moving forward with the operation
    method = "archive" if not args.delete else "delete"
    if not args.yes and not confirm(f"{method} {len(transactions)} {args.status} transactions for {counterparty['name']} ({counterparty_id})?"):
        raise CommandError(f"{method} operation cancelled")

    for tx in transactions:
        if args.dry_run:
            print(" ".join([
                f"dry run: {method} transfer {tx['id']} (status {tx['status']})",
                f"with {tx['counterparty']}: {tx['amount']} {tx['virtual_asset']}",
                f"from {tx['originator_address']} to {tx['beneficiary_address']}"
            ]))
        elif args.delete:
            client.transactions.delete(tx["id"])
        else:
            tx = client.transactions.detail(tx["id"])
            tx.archive()


CLEANUP_ARGS = {
    "description": "batch archive or delete transactions by counterparty and status",
    "func": cleanup,
    "args": {
        ("-s", "--status"): {
            "help": "the status of the transactions to cleanup",
            "default": "review",
            "type": str,
            "choices": [
                "draft", "pending", "repair", "review",
                "rejected", "accepted", "completed"
            ],
        },
        ("-c", "--counterparty"): {
            "help": "the counterparty name or ID of the transactions to cleanup",
            "type": str,
            "required": True,
        },
        ("-D", "--delete"): {
            "help": "delete the transactions instead of archiving them",
            "action": "store_true",
            "default": False,
        },
        ("-d", "--dry-run"): {
            "help": "do not perform the operation, print the affected transactions",
            "action": "store_true",
            "default": False,
        },
        ("-y", "--yes"): {
            "help": "answer yes to all confirmation prompts",
            "action": "store_true",
            "default": False,
        },
    },
}
