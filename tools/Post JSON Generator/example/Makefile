generate: 
	python3 ../generator.py  -keep-impl --template=is-binary-tree-balanced-template.json --cpp=Balanced_binary_treeTest.cc --output example.json

submit:
	python3 ../judgetest.py --json=example.json -cpp
	
clean:
	rm example.json
