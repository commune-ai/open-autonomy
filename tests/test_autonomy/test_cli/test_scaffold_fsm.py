# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2022 Valory AG
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

"""Test 'scaffold fsm' subcommand."""

import importlib.util
import os
import shutil
from importlib.machinery import ModuleSpec
from pathlib import Path
from unittest import mock

import click.testing
import pytest
from aea.configurations.constants import PACKAGES
from aea.test_tools.test_cases import AEATestCaseEmpty

# trigger population of autonomy commands
import autonomy.cli.core  # noqa

from packages.valory import skills

from tests.conftest import ROOT_DIR


VALORY_SKILLS_PATH = Path(os.path.join(*skills.__package__.split("."))).absolute()
fsm_specifications = list(VALORY_SKILLS_PATH.glob("**/fsm_specification.yaml"))


class BaseScaffoldFSMTest(AEATestCaseEmpty):
    """Test `scaffold fsm` subcommand."""

    @classmethod
    def setup_class(cls) -> None:
        """Set up the test."""
        super().setup_class()
        cls.agent_name = "default_author"
        cls.set_agent_context(os.path.join("packages", cls.agent_name))
        cls.create_agents(cls.agent_name, is_local=cls.IS_LOCAL, is_empty=cls.IS_EMPTY)
        shutil.move(str(cls.t / cls.agent_name), str(cls.t / "packages"))

    def scaffold_fsm(self, fsm_spec_file: Path) -> click.testing.Result:
        """Scaffold FSM."""

        path_to_spec_file = Path(ROOT_DIR) / fsm_spec_file
        packages_path = str(Path(ROOT_DIR) / Path(PACKAGES))
        my_skill = f"test_skill_{fsm_spec_file.parts[-2]}"
        scaffold_args = ["scaffold", "fsm", my_skill, "--local", "--spec"]
        args = ["--registry-path", packages_path, *scaffold_args, path_to_spec_file]
        return self.run_cli_command(*args, cwd=self._get_cwd())


class TestScaffoldFSM(BaseScaffoldFSMTest):
    """Test `scaffold fsm` subcommand."""

    @pytest.mark.parametrize("fsm_spec_file", fsm_specifications)
    def test_scaffold_fsm(self, fsm_spec_file: Path) -> None:
        """Test scaffold fsm."""

        result = self.scaffold_fsm(fsm_spec_file)
        assert result.exit_code == 0


class TestScaffoldFSMImports(BaseScaffoldFSMTest):
    """Test `scaffold fsm` subcommand."""

    @pytest.mark.parametrize("fsm_spec_file", fsm_specifications)
    def test_imports(
        self, fsm_spec_file: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test imports of scaffolded modules"""

        self.scaffold_fsm(fsm_spec_file)
        monkeypatch.syspath_prepend(self.t)
        path = self.t / self.agent_name
        for file in path.rglob("**/*.py"):
            module_spec = importlib.util.spec_from_file_location("name", file)
            assert isinstance(module_spec, ModuleSpec)
            module_type = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(module_type)  # type: ignore


class TestScaffoldFSMAutonomyTests(BaseScaffoldFSMTest):
    """Test `scaffold fsm` subcommand."""

    @pytest.mark.parametrize("fsm_spec_file", fsm_specifications)
    def test_autonomy_test(self, fsm_spec_file: Path) -> None:
        """Run autonomy test on the scaffolded skill"""

        with mock.patch("aea.cli.utils.decorators._validate_config_consistency"):
            self.scaffold_fsm(fsm_spec_file)
            prefix = self.t / "packages" / self.agent_name / "skills"
            path = prefix / f"test_skill_{fsm_spec_file.parts[-2]}"
            packages_dir = str(Path(self._get_cwd()).parent)
            args = ["test", "by-path", str(path)]
            result = self.run_cli_command(*args, cwd=packages_dir)
            assert result.exit_code == 0
