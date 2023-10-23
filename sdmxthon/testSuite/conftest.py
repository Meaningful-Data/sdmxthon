import os

from pytest import fixture


@fixture
def data_path(request):
    base_path = request.node.get_closest_marker('input_path').args[0]
    return os.path.join(base_path, "data_sample")


@fixture
def reference_path(request):
    base_path = request.node.get_closest_marker('input_path').args[0]
    return os.path.join(base_path, "reference")


@fixture
def metadata_path(request):
    base_path = request.node.get_closest_marker('input_path').args[0]
    return os.path.join(base_path, "metadata")
