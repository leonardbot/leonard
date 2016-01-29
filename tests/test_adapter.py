from leonard import adapter


def test_importing_adapter():
    result = adapter.import_adapter('adapters.console')
    assert result is not None


def test_loading_adapter():
    result = adapter.load_adapter('console')

    assert result is not None
    assert type(result) == adapter.Adapter
    assert hasattr(result, 'name')
    assert hasattr(result, 'module')
    assert hasattr(result, 'config')
