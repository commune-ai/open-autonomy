#!/usr/bin/env sh

cp ../configure_agents/keys/ethereum_private_key_1.txt ethereum_private_key.txt
aea config set vendor.valory.skills.price_estimation_abci.models.price_api.args.source_id coinmarketcap
aea config set vendor.valory.skills.price_estimation_abci.models.price_api.args.api_key 2142662b-985c-4862-82d7-e91457850c2a
aea config set vendor.valory.skills.price_estimation_abci.models.params.args.consensus.max_participants 4
aea config set vendor.valory.skills.price_estimation_abci.models.params.args.tendermint_url http://node1:26657
aea config set vendor.valory.skills.price_estimation_abci.models.params.args.ethereum_node_url http://hardhat:8545
aea config set vendor.fetchai.connections.ledger.config.ledger_apis.ethereum.address http://hardhat:8545
aea build