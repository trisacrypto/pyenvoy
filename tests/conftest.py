import pytest
import random


@pytest.fixture(scope="module")
def transactions():
    return [
        {
            "id": "1617520d-8d27-422e-ba59-b36a5701ede6",
            "source": "local",
            "status": "pending",
            "counterparty": "CharlieVASP",
            "counterparty_id": "01HTQXPSY42TS08TYMH2R4K37K",
            "originator": "Mary Tilcott",
            "originator_address": "mjJ9xufmdSfZLRUXV6Ac3r64M6bbrxCu48",
            "beneficiary": "Ada Lovelace",
            "beneficiary_address": "mhqBatgwaUHFouZz8X7xchx6ePKppitqzU",
            "virtual_asset": "BTC",
            "amount": 3.54e-05,
            "last_update": "2024-07-29T15:34:52.303915438Z",
            "envelope_count": 2,
            "created": "2024-07-29T15:34:51.983925487Z",
            "modified": "2024-07-29T15:34:52.305623673Z",
        },
        {
            "id": "82d3aa97-44a3-4445-8b7d-da87bc93a699",
            "source": "local",
            "status": "rejected",
            "counterparty": "CharlieVASP",
            "counterparty_id": "01HTQXPSY42TS08TYMH2R4K37K",
            "originator": "Mary Tilcott",
            "originator_address": "mjJ9xufmdSfZLRUXV6Ac3r64M6bbrxCu48",
            "beneficiary": "Ada Lovelace",
            "beneficiary_address": "mkBxBRNTciK5AD3w36jQjeeeJRrBRf4WC8",
            "virtual_asset": "BTC",
            "amount": 0.000612664,
            "last_update": "2024-07-29T14:41:36.588745182Z",
            "envelope_count": 4,
            "created": "2024-07-29T14:40:16.339663621Z",
            "modified": "2024-07-29T14:41:36.589290283Z",
        },
        {
            "id": "7effc231-3045-42f5-a073-90c650c3fc49",
            "source": "local",
            "status": "review",
            "counterparty": "CharlieVASP",
            "counterparty_id": "01HTQXPSY42TS08TYMH2R4K37K",
            "originator": "Mary Tilcott",
            "originator_address": "0x64FFD67A858C013E0EBED36B9ECD0E77C376AF26",
            "beneficiary": "Ada Lovelace",
            "beneficiary_address": " 0x3D9BBF05D7615C4478A8C249A21383C459D4D24E",
            "virtual_asset": "ETH (GAS)",
            "amount": 23.0,
            "last_update": "2024-07-29T14:36:54.472447717Z",
            "envelope_count": 4,
            "created": "2024-07-29T14:36:03.874913572Z",
            "modified": "2024-07-29T14:36:54.472926185Z",
        },
        {
            "id": "36af060d-147b-477f-99f5-ed739c3b5260",
            "source": "local",
            "status": "review",
            "counterparty": "CharlieVASP",
            "counterparty_id": "01HTQXPSY42TS08TYMH2R4K37K",
            "originator": "Mary Tilcott",
            "originator_address": "mjJ9xufmdSfZLRUXV6Ac3r64M6bbrxCu48",
            "beneficiary": "Ada Lovelace",
            "beneficiary_address": "mkBxBRNTciK5AD3w36jQjeeeJRrBRf4WC8",
            "virtual_asset": "BTC",
            "amount": 1e-06,
            "last_update": "2024-07-29T14:29:38.813674438Z",
            "envelope_count": 4,
            "created": "2024-07-29T14:21:40.863640707Z",
            "modified": "2024-07-29T14:29:38.817746836Z",
        },
    ]


@pytest.fixture(scope="module")
def transaction(transactions):
    i = random.randint(0, len(transactions) - 1)
    return transactions[i]


@pytest.fixture(scope="module")
def accounts():
    [
        {
            "id": "01HV6RV08YNR2GH8MEEFCV4NKN",
            "customer_id": "27166869",
            "first_name": "Mary",
            "last_name": "Tilcott",
            "travel_address": "ta4n7VX9D53cuj5Z7PhzV3VQZDJTvwTAfoFe9Lebqxc1yrhdSA9DqxYsNuHzmZLzVHQTs9SoYo6rqVZgeKu8GpejqnixkEogrFzABjboQJa4j",  # noqa
            "crypto_addresses": [],
            "created": "2024-04-11T14:26:26.718450843Z",
            "modified": "2024-06-18T17:21:26.320856455Z",
        },
        {
            "id": "01HVS53MS4ACHY8TH9HQP3KC07",
            "customer_id": "007999999",
            "first_name": "James",
            "last_name": "Bond",
            "travel_address": "ta4n7VX9D53cuj5Z7PhzV3VQZDJTvwTAfoFe9Lebqxc1yrhdSA9Dr4tJShZPXN9RLdk7mrQm5FuGEuX3YR5epeGfMUwXrwrYHpSxk6w5WcqwB",  # noqa
            "crypto_addresses": [],
            "created": "2024-04-18T17:47:12.548765548Z",
            "modified": "2024-06-18T17:21:26.359994646Z",
        },
        {
            "id": "01HZJ0BTNDXVE2MKTZBNF93MNZ",
            "customer_id": "39910432",
            "first_name": "Twilda",
            "last_name": "Swansong",
            "travel_address": "ta4n7VX9D53cuj5Z7PhzV3VQZDJTvwTAfoFe9Lebqxc1yrhdSA9DuuUrLqtdDxjAjWuiDuSqAXabEn89Y9yKoMHZTjtM3Noj5p5VubQdp3BUu",  # noqa
            "crypto_addresses": [],
            "created": "2024-06-04T16:12:24.109734714Z",
            "modified": "2024-06-18T17:21:26.401280348Z",
        },
        {
            "id": "01J2EM41FHVZAKCX2V22R5ZEB5",
            "customer_id": "87878787877",
            "first_name": "Homer",
            "last_name": "Simpson",
            "travel_address": "ta4n7VX9D53cuj5Z7PhzV3VQZDJTvwTAfoFe9Lebqxc1yrhdSA9Mnn7CEdsPgcvY1Nx6JR1XYMwfyD8uKDjNdYVaymQMdGa9ApH85UZDkuw1b",  # noqa
            "crypto_addresses": [],
            "created": "2024-07-10T15:27:48.209902771Z",
            "modified": "2024-07-10T15:27:48.209902771Z",
        },
        {
            "id": "01J30GCY7QESHGHR19GZ8EAWVR",
            "customer_id": "764306082",
            "first_name": "Roni",
            "last_name": "Gifford",
            "travel_address": "ta4n7VX9D53cuj5Z7PhzV3VQZDJTvwTAfoFe9Lebqxc1yrhdSA9Mofe6ewNndxTdTAwaeHo9KmeyM3Xdsaz6wwWL3AqmBJEjET9rg8FDG3jYs",  # noqa
            "crypto_addresses": [],
            "created": "2024-07-17T14:09:05.271319559Z",
            "modified": "2024-07-17T14:09:05.271319559Z",
        },
    ]
