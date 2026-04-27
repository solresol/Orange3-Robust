from importlib.metadata import entry_points


def test_orange_widget_entry_point_is_registered():
    eps = entry_points(group="orange.widgets")
    robust_eps = [ep for ep in eps if ep.name == "Robust"]

    assert robust_eps
    assert robust_eps[0].value == "orangecontrib.robust.widgets"


def test_widget_modules_import():
    import orangecontrib.robust.widgets.owrobustregression  # noqa: F401
    import orangecontrib.robust.widgets.owrobustscale  # noqa: F401


def test_orange_widget_discovery_finds_robust_category():
    from orangecanvas.registry import WidgetRegistry
    from orangewidget.workflow.discovery import WidgetDiscovery

    registry = WidgetRegistry()
    discovery = WidgetDiscovery(registry)
    discovery.run("orange.widgets")

    robust_categories = [cat for cat in registry.categories() if cat.name == "Robust"]

    assert len(robust_categories) == 1
    assert {widget.name for widget in registry.widgets("Robust")} == {
        "Robust Regression",
        "Robust Scale",
    }
