import pyspark

# This code will run only in pyspark console

file = sc.textFile("Tweet 3000.json")
splitWords = text_file.flatMap(lambda line: line.split(" ")) 
mapWords = splitWords.map(lambda word: (word, 1))
finalCount = mapWords.reduceByKey(lambda a, b: a + b)

counts.coalesce(1).saveAsTextFile("FrequencyOfWords.txt")