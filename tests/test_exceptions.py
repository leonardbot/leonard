from leonard import exceptions


def test_module_errors_catching():
    # Simulate function with bug
    # by ZeroDivision
    @exceptions.catch_module_errors
    def broken_function():
        return 2 / 0

    # Run broken function
    broken_function()

    # Check, that program didn't exit
    assert True
