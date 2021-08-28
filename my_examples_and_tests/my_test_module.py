# The module can also be stored in "site-packages" directory of the current virtual environment ('venv'):
# ~/PycharmProjects/PythonNetEng/venv/lib/python3.8/site-packages/my_test_module.py
# See paths where python looks for modules: ipmort sys + sys.path

def my_function():
    print("Here my_function() does some work inside and returns result.")


# To hide execution of this code when this script is imported as module in another script.
if __name__ == '__main__':
    print("Here I'm running my_function() inside the module for test!")
    my_function()
    print("Results: my_function() ... done!")