import os
import re
import sys
import matplotlib.pyplot as plt
import numpy as np

"""
Recursively traverses from a root directory and returns a dictionary of counts.
@param rootDir: The root directory to start the searches
@param pattern: A compiled, valid regular expression pattern
@return: A dictionary of key=directory value=count of files that match the regex pattern
"""
def traverse_directories(rootDir, pattern):
	result = dict()
	for root, directories , filenames in os.walk(rootDir):
	    for filename in filenames: 
	    	path = os.path.join(root, filename)
	    	# Only check files and not directories
	    	if (os.path.isfile(path)):
		    	if pattern.match(filename):
		    		if (root in result):
		    			result[root]+=1
		    		else:
		    			result[root]=1
	print result
	return result

"""
Plots a bar graph, given a dictionary. X-Axis=Directory, Y-Axis=Count of Files that match RegEx

@param dictionary: A dictionary containing key=directory, value=counts as integers
@return: The axes object of the graph
"""
def plot_bar_graph(dictionary, ax=None):
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)

    counts = dictionary.values()
    directories = dictionary.keys()

    plt.xlabel('Directories')
    plt.ylabel('Counts')

    x_coordinates = np.arange(len(dictionary))
    ax.bar(x_coordinates, counts, align='center')

    ax.xaxis.set_major_locator(plt.FixedLocator(x_coordinates))
    ax.xaxis.set_major_formatter(plt.FixedFormatter(directories))

    return ax

args = sys.argv[1:]
print args
if len(args) < 2:
	print "Please provide a Root Directory and Filename RegEx as arguments"
elif len(args) > 3:
	print "The script only supports 3 arguments. Please check your inputs and ensure there are not any spaces"
else:
	if not os.path.exists(args[0]):
		print "This is not a valid directory name"
	else:
		try:
			# Compiling a regular expression dramatically increases speed of regex match
			pattern = re.compile(args[1])
			result = traverse_directories(args[0], pattern)

			if (len(args) == 3 and args[2].lower() == 'true'):
				if (len(result) == 0):
					print "No Data to plot!"
				elif (len(result) <= 20):
					plot_bar_graph(result)
					plt.show()
				else:
					# If there is too much data to display, the x index of the graph will not display properly
					print "Data will not be plotted for searches containing more than 20 subdirectories"
		except re.error:
			print "Your Filename RegEx is invalid!"

# Tests (Dependent on Environment, therefore it is appended here as to what to test for)
# Ideally, the environment would have a test script that generates all the test files before running the below checks

# Test 1 (No Arguments)
# Execution: "python countFiles.py"
# Expect: "Please provide a Root Directory and Filename RegEx as arguments"

# Test 2 (1 Argument)
# Execution: "python countFiles.py test"
# Expect: "Please provide a Root Directory and Filename RegEx as arguments"

# Test 3 (2 Invalid Arguments)
# Execution: "python countFiles.py <invalid> <invalid>"
# Expect: "This is not a valid directory name"

# Test 4 (2 Arguments, Directory argument invalid)
# Execution: "python countFiles.py <invalid> <valid>"
# Expect: "This is not a valid directory name"

# Test 5 (2 Arguments, Directory Valid, RegEx Invalid)
# Execution: "python countFiles.py <valid> <invalid>"
# Expect: "Your Filename RegEx is invalid!

# Test 6 (2 Arguments, Both Valid, No result)
# Execution: "python countFiles.py <valid> <valid>"
# Expect: {}

# Test 7 (2 Arguments, Both Valid, Result in topmost directory)
# Execution: "python countFiles.py <valid> <valid>"
# Expect: {'<first level dir>': <count>}

# Test 8 (2 Arguments, Both Valid, Result in all directories)
# Execution: "python countFiles.py <valid> <valid>"
# Expect: {'<first level dir>': <count>, <2nd level dir>': <count>, <3rd level dir>': <count>.....}

# Test 9 (3 Arguments, 3rd argument is not anything that says 'true')
# Execution: "python countFiles.py <valid> <valid> 'hello'"
# Expect: {} and no graph plot coming up

# Test 10 (3 Arguments, 3rd argument = True, No Result)
# Execution: "python countFiles.py <valid> <valid> 'True'"
# Expect: {} "No Data to plot!"

# Test 11 (3 Arguments, 3rd argument = True, Results found)
# Execution: "python countFiles.py <valid> <valid> 'True'"
# Expect: {} , a Graph chart coming up that plots the data, with xlabel = "Directories", ylabel= "Counts"

# Test 12 (2 Arguments, Windows path on Linux)
# Execution: "python countFiles.py <windows path> <valid>"
# Expect: "This is not a valid directory name"

# Test 13 (2 Arguments, Linux path on Windows)
# Execution: "python countFiles.py <linux path> <valid>"
# Expect: "This is not a valid directory name"

# Test 14 (Providing a path with spaces)
# Execution: "python countFiles.py /matthewfung test/test / test"
# Expect: "The script only supports 3 arguments. Please check your inputs and ensure there are not any spaces"

# Test 15 (2 arguments, Providing a path with spaces, but in quotation marks)
# Execution: "python countFiles.py '/matthewfung test/test / test' test"
# Expect: Python should pick up that as a valid path, and return results if results found, or "This is not a valid directory name" if the directory is not valid