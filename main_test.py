import pytest


def run_tests():
    # This will run all test files starting with "test_" in the current directory
    pytest_args = [
        "--maxfail=5",  # Stop after 5 failures, can be adjusted as needed
        "--disable-warnings",  # Disable warnings for a cleaner output
        "--capture=no",  # Show print statements in the output
    ]

    # Run pytest on all files or specify individual files if needed
    pytest.main(pytest_args + ["integration_Login_test.py", "All_Features_test.py"])


if __name__ == "__main__":
    run_tests()
