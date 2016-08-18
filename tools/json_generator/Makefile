#Set up EPICODE_ROOT environment variable so that it points to the directory where https://github.com/adnanaziz/epicode is located
#Run `make keep_impl=y` to generate debug versions of JSON that can be directly submitted to the server using `submit.py`
GENERATOR := generator.py
PYTHON    := python3
TMPLT_DIR := templates
GNRTD_DIR := generated
CCSRC_DIR := $(EPICODE_ROOT)/cpp

TEST_OPTION :=
ifdef keep_impl
	TEST_OPTION := -keep-impl
endif
	
all :
TARGETS :=
#params: json filename, cpp test file, cpp dependencies (separated by space, starting with *Test.cc), java dependencies (separated by space, starting with *Test.java)
define add_target
$(addprefix $(GNRTD_DIR)/, $(1)): $(GENERATOR) $(addprefix $(TMPLT_DIR)/, $(1)) $(addprefix $(CCSRC_DIR)/, $(2))
TARGETS += $(addprefix $(GNRTD_DIR)/, $(1))
endef

# Build dependencies.
#anonymous-letter
$(eval $(call add_target, anonymous-letter.json, Anonymous_letterTest.cc Anonymous_letter.cc))
#container-with-most-water
$(eval $(call add_target, container-with-most-water.json, container-with-most-waterTest.cc container-with-most-water.cc))
#convert-base
$(eval $(call add_target, convert-base.json, Convert_baseTest.cc Convert_base.cc))
#first-missing-positive
$(eval $(call add_target, first-missing-positive.json, first-missing-positiveTest.cc first-missing-positive.cc))
#gassing-up
$(eval $(call add_target, gassing-up.json, Gassing_upTest.cc Gassing_up.cc))
#intersect-sorted-arrays
$(eval $(call add_target, intersect-sorted-arrays.json, Intersect_sorted_arrays3Test.cc Intersect_sorted_arrays3.h))
#is-binary-tree-balanced
$(eval $(call add_target, is-binary-tree-balanced.json, Balanced_binary_treeTest.cc Balanced_binary_tree.cc Binary_tree_prototype.h)) 
#matrix-search
$(eval $(call add_target, matrix-search.json, Matrix_searchTest.cc Matrix_search.cc))
#normalized-pathnames
$(eval $(call add_target, normalized-pathnames.json, normalized_pathnamesTest.cc normalized_pathnames.cc))
#number-ways
$(eval $(call add_target, number-ways.json, Number_waysTest.cc Number_ways.cc))
#palindrome-number
$(eval $(call add_target, palindrome-number.json, palindrome-numberTest.cc palindrome-number.cc))
#rpn
$(eval $(call add_target, rpn.json, RPNTest.cc RPN.cc))
#snake-string
$(eval $(call add_target, snake-string.json, snake-stringTest.cc snake-string.cc))
#spreadsheet-encoding
$(eval $(call add_target, spreadsheet-encoding.json, Spreadsheet_encodingTest.cc Spreadsheet_encoding.cc))
#square-root-int
$(eval $(call add_target, square-root-int.json, square-root-intTest.cc square-root-int.cc))
#sudoku-solve
$(eval $(call add_target, sudoku-solve.json, Sudoku_solveTest.cc Sudoku_solve.cc))

# One generic rule for all $(TARGETS)     
$(TARGETS) : % :
#@echo Making $@ from $^
	$(PYTHON) $(GENERATOR) $(TEST_OPTION) --output=$@ --template=$(word 2,$^) --cpp=$(word 3,$^)

all : check-env $(TARGETS)

check-env:
ifndef EPICODE_ROOT
    $(error EPICODE_ROOT is undefined)
endif

clean:
	rm $(TARGETS)

.PHONY: all clean check-env