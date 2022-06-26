# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2021-2022 Valory AG
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

"""End2end tests for the valory/simple_abci skill."""
import pytest

from tests.test_agents.base import BaseTestEnd2EndNormalExecution, RoundChecks


# round check log messages of the happy path
HAPPY_PATH = (
    RoundChecks("registration"),
    RoundChecks("randomness_startup", n_periods=3),
    RoundChecks("select_keeper_at_startup", n_periods=2),
    RoundChecks("reset_and_pause", n_periods=2),
)

# strict check log messages of the happy path
STRICT_CHECK_STRINGS = ("Period end",)


@pytest.mark.parametrize("nb_nodes", (1,))
class TestSimpleABCISingleAgent(
    BaseTestEnd2EndNormalExecution,
):
    """Test the ABCI simple_abci skill with only one agent."""

    agent_package = "valory/simple_abci:0.1.0"
    skill_package = "valory/simple_abci:0.1.0"
    wait_to_finish = 80
    happy_path = HAPPY_PATH
    strict_check_strings = STRICT_CHECK_STRINGS
    use_benchmarks = True


@pytest.mark.parametrize("nb_nodes", (2,))
class TestSimpleABCITwoAgents(
    BaseTestEnd2EndNormalExecution,
):
    """Test the ABCI simple_abci skill with two agents."""

    agent_package = "valory/simple_abci:0.1.0"
    skill_package = "valory/simple_abci:0.1.0"
    wait_to_finish = 120
    happy_path = HAPPY_PATH
    strict_check_strings = STRICT_CHECK_STRINGS


@pytest.mark.parametrize("nb_nodes", (4,))
class TestSimpleABCIFourAgents(
    BaseTestEnd2EndNormalExecution,
):
    """Test the ABCI simple_abci skill with four agents."""

    agent_package = "valory/simple_abci:0.1.0"
    skill_package = "valory/simple_abci:0.1.0"
    wait_to_finish = 120
    happy_path = HAPPY_PATH
    strict_check_strings = STRICT_CHECK_STRINGS
