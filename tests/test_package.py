from importlib.metadata import entry_points
from pathlib import Path


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


def test_demo_workflow_loads():
    from orangecanvas.registry import WidgetRegistry
    from orangecanvas.scheme import Scheme
    from orangecanvas.scheme.readwrite import scheme_load
    from orangewidget.workflow.discovery import WidgetDiscovery

    registry = WidgetRegistry()
    discovery = WidgetDiscovery(registry)
    discovery.run("orange.widgets")
    discovery.run("orangecontrib.robust.widgets")

    scheme = Scheme()
    workflow = (
        Path(__file__).resolve().parents[1]
        / "docs"
        / "examples"
        / "robust-regression-demo.ows"
    )
    with workflow.open("rb") as stream:
        scheme_load(scheme, stream, registry=registry)

    assert [node.title for node in scheme.nodes] == [
        "File",
        "Select Columns",
        "Robust Regression",
        "Test and Score",
        "Coefficients Table",
        "Annotated Data",
    ]
    assert len(scheme.links) == 6
