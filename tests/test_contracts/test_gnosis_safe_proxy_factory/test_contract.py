# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2021 Valory AG
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""Tests for valory/gnosis contract."""

from pathlib import Path

from packages.valory.contracts.gnosis_safe.contract import SAFE_CONTRACT
from packages.valory.contracts.gnosis_safe_proxy_factory.contract import (
    PROXY_FACTORY_CONTRACT,
)

from tests.conftest import ROOT_DIR
from tests.test_contracts.base import BaseGanacheContractTest


class TestGnosisSafeProxyFactory(BaseGanacheContractTest):
    """Test deployment of the proxy to Ganache."""

    directory = Path(
        ROOT_DIR, "packages", "valory", "contracts", "gnosis_safe_proxy_factory"
    )
    deployment_kwargs = dict(gas=10000000, gasPrice=10000000)

    def test_deploy(self):
        """Test deployment results."""
        assert (
            self.contract_address != PROXY_FACTORY_CONTRACT
        ), "Contract addresses should differ as we don't use deterministic deployment here."

    def test_build_tx_deploy_proxy_contract_with_nonce(self):
        """Test build_tx_deploy_proxy_contract_with_nonce method."""
        result = self.contract.build_tx_deploy_proxy_contract_with_nonce(
            self.ledger_api,
            self.contract_address,
            SAFE_CONTRACT,
            self.deployer_crypto.address,
            b"",
            1,
            gas=1000,
            gas_price=1000,
            nonce=1,
        )
        assert len(result) == 2
        assert len(result[0]) == 8
        assert all(
            [
                key
                in [
                    "value",
                    "gas",
                    "gasPrice",
                    "chainId",
                    "from",
                    "to",
                    "data",
                    "nonce",
                ]
                for key in result[0].keys()
            ]
        )
