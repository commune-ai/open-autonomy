#!/usr/bin/env sh

cp ../configure_agents/keys/ethereum_private_key_3.txt ethereum_private_key.txt
aea config set vendor.valory.skills.price_estimation_abci.models.price_api.args.source_id binance
aea config set vendor.valory.skills.price_estimation_abci.models.params.args.consensus.max_participants 4
aea config set vendor.valory.skills.price_estimation_abci.models.params.args.tendermint_url http://node3:26657
aea config set vendor.valory.skills.price_estimation_abci.models.params.args.convert_id USDT
aea config set vendor.valory.skills.price_estimation_abci.models.params.args.ethereum_node_url http://hardhat:8545
aea build

