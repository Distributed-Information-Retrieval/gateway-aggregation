import inspect

import gateway_aggregation


def test_smoke() -> None:
    assert inspect.ismodule(gateway_aggregation)
