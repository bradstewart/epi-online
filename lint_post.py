import json

files = [ "convert-base-with-harness.json", "rpn-with-harness.json", "square-root-int-with-harness.json", "sudoku-solve-with-harness.json"] 

for filename in files:
    print("\nChecking " + filename)
    src = open(filename).read().strip()
    problem = json.loads(src)
    for key in problem:
        print(key + ":\t" + problem[key])
