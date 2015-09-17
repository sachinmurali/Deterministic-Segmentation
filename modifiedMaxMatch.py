import time, itertools, argparse

globalLeft = []
globalRight = []

#Function that converts hashtags into a list of words using maxMatch
def hashTags(hashtagTrain, ngramsFile):

	global globalRight
	global globalLeft

	dList = createDictionary(ngramsFile)
	
	with open(hashtagTrain) as hFile:								# Open the raw hashtags file
		for line in hFile:
			if line.startswith("#"):

				line = line.strip('#').lower().rstrip()				# Remove hashtags at the beginning and newline character at the end

				finalList = optimizedMaxMatch(line, dList)			# A funct				

				localLeft = globalLeft
				localRight = globalRight

				globalRight = []
				globalLeft = []

				localRight.reverse()

				localLeft.extend(localRight)

				finalList = localLeft

				splitTokens(finalList)	 							# Call splitTokens to write the list containing the words into a file

def createDictionary(dictionaryFile):

	myDictionary = {}
	
	with open(dictionaryFile) as myFile:							# Open the google derived list of words
		for line in myFile:											# Read only the first 75000 words
			line = line.rstrip().split()
			myDictionary[line[0]] = line[0]							# The key and value for the dictionary are the words itself
	return myDictionary

def optimizedMaxMatch(sentence, dictionary):

	if sentence == "":
		return []

	leftword = leftLongestWord(sentence,dictionary)
	leftremainder = sentence[len(leftword):]

	rightword = rightLongestWord(sentence, dictionary)
	rightremainder = sentence[:len(sentence) - len(rightword)]
	
	if len(leftword) > len(rightword):
		globalLeft.append(leftword)
		optimizedMaxMatch(leftremainder, dictionary)
	else:
		globalRight.append(rightword)
		optimizedMaxMatch(rightremainder, dictionary)

def leftLongestWord(sentence, dictionary):
	
	for i in xrange(len(sentence), 0, -1):

		word = sentence[:i]

		if i == 1:
			return sentence[0]
		elif dictionary.get(word) != None:
			return word	

def rightLongestWord(sentence, dictionary):

	for i in xrange(0, len(sentence)):

		word = sentence[i:]

		if i == len(sentence) - 1:
			return sentence[i]
		elif dictionary.get(word) != None:
			return word

#Function to write all the tokens onto a file
def splitTokens(tokenList):

	with open("output.txt", "a") as hFile:							
		hFile.write(" ".join(tokenList))							
		hFile.write("\n")	

def compareTokens(file1, file2):
   
   total_error_rate, hashtagCount = 0, 0

   with open(file1) as source, open(file2) as destination:
      for lineA, lineB in zip(source, destination):

         hashtagCount += 1

         first_file, second_file = lineA.split(), lineB.split()            # Split the line into a list of words

         total_edit_distance = minEditDist(first_file, second_file)        # val - hold the value of the total edit distance between
                                                                           #       all the words 
         error_rate = total_edit_distance / float(len(second_file))
                                                                           #word error rates
         total_error_rate += error_rate

   final_error_rate = total_error_rate / float(hashtagCount)

   print "Individual word error rate: %s, Total Hashtags: %s, Final word error rate: %s" %(total_error_rate, hashtagCount, final_error_rate)

# Function that calculates the minimum edit distance between two words
def minEditDist(source, target):

   n = len(source)
   m = len(target)

   D = [[0 for j in range(m+1)] for i in range(n+1)]                       	# Creates a 2d matrix with i rows and j columns

   D[0][0] = 0                                                             	# Assign the 1st element in the matrix as 0

   for i in range(1, n+1):
   	D[i][0] = D[i-1][0] + 1                                              	# Fill the rows initially with elements

   for j in range(1, m+1):                                                 	# Fill the columns initially with elements
      D[0][j] = D[0][j-1] + 1

   for i in range(1,n+1):
      for j in range(1,m+1):
         D[i][j] = min(D[i-1][j] + 1, D[i-1][j-1] + costFunction(source[i-1], target[j-1]), D[i][j-1] + 1)

   return D[n][m]

# Function to determine the cost of the substitution
def costFunction(val1, val2):

   if val1 != val2:
   	return 1
   else:
   	return 0
   	   

if __name__=="__main__":

	start_time = time.time()

	parser = argparse.ArgumentParser()

	parser.add_argument("hashtagTrain", help = "This file contains the hashtags")
	parser.add_argument("ngramsFile", help = "This file contains my dictionary")
	parser.add_argument("outputFile", help = "Contains my MaxMatch answers")
	parser.add_argument("referenceFile", help = "Contains reference segmentation")

	args = parser.parse_args()

	hashtagTrain = args.hashtagTrain
	ngramsFile = args.ngramsFile

	hashTags(hashtagTrain, ngramsFile)

	file1 = args.outputFile
   	file2 = args.referenceFile

   	compareTokens(file1, file2)

	print "Execution time: %s" %(time.time() - start_time)