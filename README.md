# PyEnvoy

**A Python API client for [TRISA Envoy](https://trisa.dev/envoy/index.html) nodes**.

Envoy is a secure messaging tool designed for travel rule data exchanges, ensuring compliance using the [TRISA](https://trisa.io) (Travel Rule Information Sharing Architecture) and [TRP](https://www.openvasp.org/trp) (Travel Rule Protocol) protocols.

Virtual Asset Service Providers (VASPs) can deploy an Envoy node in order to interact with the compliance network using peer-to-peer messaging. The `pyenvoy` package allows VASPs to interact with their Envoy node programatically in Python so that they can:

- Manage users and API keys
- Manage customer accounts and counterparty information
- Create, view, and manage travel rule transactions
- Send and receive secure envelopes with counterparties
- Manage public keys on the node
- Manage the configuration of the node

The API allows users to treat Envoy as their boundary node to compliance networks, and integrate travel rule data exchanges with their transaction processing systems or internal compliance tools.

## Version note

Envoy uses semantic versioning like `major.minor.micro` (for full release versions). API-compatibility between the Envoy server and `pyenvoy` client will be based on the `major.minor` version, however the `micro` version may differ between the two.

## Getting Started

You will need to deploy or host an Envoy node at a URL accessible by the client, then generate an API key and save the client ID and secret for the keys.

You can install PyEnvoy as follows:

```
$ pip install -U pyenvoy
```

Set the following environment variables:

1. `$ENVOY_URL`: the url of your Envoy API, e.g. `"https://myenvoy.tr-envoy.com/"`
2. `$ENVOY_CLIENT_ID`: the client ID of your API keys
3. `$ENVOY_CLIENT_SECRET`: the client secret for your API keys

If you're using the `connect()` function, you can also store these variables in a `.env` file in your current working directory (see [.env.template](./.env.template)).

Create an envoy client:

```python
from envoy import connect

envoy = connect()
```

This will create the client and load the environment variables. You can test your connection to the server:

```python
>>> envoy.status()
{'status': 'ok', 'uptime': '71h33m42.068692289s', 'version': '0.24.0-beta.28 (019fd7e)'}
```

Which should return the status, uptime, and version of your envoy node. Note that the `status` endpoint does not require authentication, so this will not check if your credentials are correct.

## REST Usage

The Envoy API is implemented as a [RESTful](https://en.wikipedia.org/wiki/REST) architecture. To that end, each resource in the API can generally be accessed with `list`, `create`, `detail`, `update`, and `delete` methods and may have other associated actions such as `send` for transactions. For example, to get a list of counterparties from the server you would use:

```python
envoy.counterparties.list()
```

Or to create a customer account you would:

```python
account_data = {...}
envoy.accounts.create(account_data)
```

All resources are named on the `envoy.Client` and are accessed as properties of the client; each of their methods can then be used to interact with the resource.

For advanced usage, note that the client also has `get`, `post`, `put`, and `delete` methods, in which you can directly make requests to the Envoy node.

## Error Handling

Envoy specific errors will be a subclass of `EnvoyError`. An `ServerError` is raised when the Envoy node returns a 500 status code, and a `ClientError` is raised when the node returns a 400 status code. `AuthenticationError` is returned when no api key credentials are specified or the Server returns a 401 or 403 status code.

Note that all API keys have a set of permissions that defines what actions they can take, if your API keys do not have the required permissions for an action, an `AuthenticationError` will be raised.
