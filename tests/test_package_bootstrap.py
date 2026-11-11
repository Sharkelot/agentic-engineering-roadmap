from importlib.util import find_spec


def test_agent_eval_lab_package_is_discoverable() -> None:
    assert find_spec("agent_eval_lab") is not None
