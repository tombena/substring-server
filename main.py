# Sources:
#     - [CSV python library](https://docs.python.org/2/library/csv.html)
#     - [Sorting results](https://stackoverflow.com/questions/3121979/how-to-sort-list-tuple-of-lists-tuples)
#     - [Flask](http://flask.pocoo.org/docs/0.12/quickstart/)

# Get top 10 for string s by opening http://localhost:5000/s

# For a query string s, we want to find all names of the
# form s or _s (s can contain "_").
# A name is of the form str1_str2_str3....
# therefore we have a match in the following cases:
#   - str1_str2_str3 starts by s
#   - str2_str3 starts by s
#   _ str3 starts by s
# My solution is to make an array of these cut-out names.
# This array is then sorted alphabetically.
# The search consists in doing a divide and conquer approach
# to find a name starting by s.
# If one is found, then all the possible matches are in the same area
# because of alphabetical ordering.
# We add the corresponding full names to our results (of max capacity 10)
# If results has reached capacity, we replace the smallest element
# in terms of score.

import csv
import re
from operator import itemgetter
from flask import Flask, jsonify

app = Flask(__name__)

class Parser(object):
    def __init__(self, file_path):
        # store tuples of type (name, full_name, score)
        # name corresponds to substrings of full_name
        # example:
        #     full name = str1_str2_str3 corresponds to the following names:
        #     str1_str2, str2_str3 and str3
        self.data = []

        with open(file_path) as f:
            csv_reader = csv.reader(f, delimiter=',')

            for row in csv_reader:
                name = row[0]
                score = int(row[1])
                full_name = name
                self.data.append((name, full_name, score))

                chunk_name = name.split('_')
                curr_name = ""

                # append chunks to each others
                # example:
                # full name = str1_str2_str3 corresponds to the following names:
                # str1_str2, str2_str3 and str3
                for i in range(1, len(chunk_name)):
                    curr_name += chunk_name[i]
                    self.data.append((curr_name, full_name, score))
                    curr_name += "_"

            # sort [name, full_name, score] by "name" alphabetically
            self.data.sort(key=lambda tup: tup[0])

    # browse array in direction delta (-1 for left, 1 for right)
    # starting from position
    # add elements while they start with substring
    # return modifed scores and results
    def browse_candidates(self, position, delta, scores, results, substring):
        i = position

        while substring == self.data[i][0][:len(substring)]:
            full_name = self.data[i][1]
            score = self.data[i][2]

            # don't add duplicate "full_name"
            if full_name not in results:
                # if results is full, replace smallest element
                if len(results) == 10:
                    ind_min = scores.index(min(scores))
                    scores[ind_min] = score
                    results[ind_min] = full_name
                # simply add
                else:
                    results.append(full_name)
                    scores.append(score)
            i += delta

            # if edge of array has been reached, stop
            if i == -1 or i == len(self.data):
                break

        return scores, results

    def return_top_10(self, substring):

        start = 0
        end = len(self.data) - 1
        # fullnames and corresponding scores
        results = []
        scores = []

        # search for a name starting by substring using divide and conquer -> O(log(N))
        # if found, add matching surrounding elements
        while True:
            middle = int((start + end)/2)

            # used for break condition
            t_start = start
            t_end = end

            # shorten current name to be the length of substring (or smaller)
            curr_name = self.data[middle][0]
            short_name = curr_name[:len(substring)]

            # if current name starts with substring
            if substring == short_name:                
                # examine left candidates from middle
                scores, results = self.browse_candidates(middle, -1, scores, results, substring)

                if middle + 1 == len(self.data):
                    break

                # examine right candidates from middle + 1
                scores, results = self.browse_candidates(middle + 1, 1, scores, results, substring)

                break
            # if substring is (alphabetically) smaller than current name
            # substring = abc < bbc -> we need to go left
            elif (substring < curr_name):
                end = middle
            # if bigger, go right
            else:
                start = middle

            # if we haven't moved, stop
            if t_start == start and t_end == end:
                break

        # sort results by score
        # return 10 highest results
        return sorted(zip(results, scores),
                      key=itemgetter(1),
                      reverse=True)


@app.route('/<substring>')
def return_top_10(substring):

    # ignore favicon request
    if substring == "favicon.ico":
        return

    return jsonify(result=p.return_top_10(substring))


if __name__ == '__main__':
    p = Parser('./data.csv')
    app.run(port=5000, 
            debug=False)

