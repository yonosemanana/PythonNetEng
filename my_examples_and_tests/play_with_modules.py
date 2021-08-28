from my_test_module import my_function # When you import a module or only a funcion from it, all module's code is executed!
# The code is executed already at the import!


# Calling my_function() function from other module.

print()
print('Here I am in another script and calling my_function().')
my_function()
print('I expect to print only results of my call of my_function().')