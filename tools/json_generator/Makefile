#Set up EPICODE_ROOT environment variable so that it points to the directory where https://github.com/adnanaziz/epicode is located
#Run `make keep_impl=y` to generate debug a version of JSON that can be directly submitted to the server using `submit.py`
GENERATOR := generator.py
PYTHON    := python3
TMPLT_DIR := templates
GNRTD_DIR := generated
CCSRC_DIR := $(EPICODE_ROOT)/cpp
JVSRC_DIR := $(EPICODE_ROOT)/java/src/main/java/com/epi

TEST_OPTION :=
ifdef keep_impl
	TEST_OPTION := -keep-impl
endif
	
all :
TARGETS :=
#params: json filename, cpp test file, cpp dependencies (separated by space, starting with *Test.cc), java dependencies (separated by space, starting with *Test.java)
define add_target
$(addprefix $(GNRTD_DIR)/, $(1)): $(GENERATOR) $(addprefix $(TMPLT_DIR)/, $(1)) $(addprefix $(CCSRC_DIR)/, $(firstword $(2))) $(addprefix $(JVSRC_DIR)/, $(firstword $(3))) $(addprefix $(CCSRC_DIR)/, $(wordlist 2, $(words $(2)), $(2))) $(addprefix $(JVSRC_DIR)/, $(wordlist 2, $(words $(3)), $(3)))
TARGETS += $(addprefix $(GNRTD_DIR)/, $(1))
endef

# Build dependencies.
#anonymous-letter
$(eval $(call add_target, anonymous-letter.json, Anonymous_letterTest.cc Anonymous_letter.cc, AnonymousLetterTest.java AnonymousLetter.java))
#container-with-most-water
$(eval $(call add_target, container-with-most-water.json, container-with-most-waterTest.cc container-with-most-water.cc, ContainerWithMostWaterTest.java ContainerWithMostWater.java))
#convert-base
$(eval $(call add_target, convert-base.json, Convert_baseTest.cc Convert_base.cc, ConvertBaseTest.java ConvertBase.java))
#first-missing-positive
$(eval $(call add_target, first-missing-positive.json, first-missing-positiveTest.cc first-missing-positive.cc, FirstMissingPositiveTest.java FirstMissingPositive.java))
#gassing-up #FIX
$(eval $(call add_target, gassing-up.json, Gassing_upTest.cc Gassing_up.cc, GassingUpTest.java GassingUp.java))
#intersect-sorted-arrays
$(eval $(call add_target, intersect-sorted-arrays.json, Intersect_sorted_arrays3Test.cc Intersect_sorted_arrays3.h, IntersectSortedArrays3Test.java IntersectSortedArrays3.java))
#is-binary-tree-balanced #FIX
$(eval $(call add_target, is-binary-tree-balanced.json, Balanced_binary_treeTest.cc Balanced_binary_tree.cc Binary_tree_prototype.h, BalancedBinaryTreeTest.java BalancedBinaryTree.java BinaryTreePrototypeTemplate.java)) 
#matrix-search
$(eval $(call add_target, matrix-search.json, Matrix_searchTest.cc Matrix_search.cc, MatrixSearchTest.java MatrixSearch.java))
#normalized-pathnames
$(eval $(call add_target, normalized-pathnames.json, normalized_pathnamesTest.cc normalized_pathnames.cc, NormalizedPathnamesTest.java NormalizedPathnames.java))
#number-ways
$(eval $(call add_target, number-ways.json, Number_waysTest.cc Number_ways.cc, NumberWaysTest.java NumberWays.java))
#palindrome-number
$(eval $(call add_target, palindrome-number.json, palindrome-numberTest.cc palindrome-number.cc, PalindromeNumberTest.java PalindromeNumber.java))
#rpn
$(eval $(call add_target, rpn.json, RPNTest.cc RPN.cc, RPNTest.java RPN.java))
#snake-string
$(eval $(call add_target, snake-string.json, snake-stringTest.cc snake-string.cc, SnakeStringTest.java SnakeString.java))
#spreadsheet-encoding
$(eval $(call add_target, spreadsheet-encoding.json, Spreadsheet_encodingTest.cc Spreadsheet_encoding.cc, SpreadsheetEncodingTest.java SpreadsheetEncoding.java))
#square-root-int
$(eval $(call add_target, square-root-int.json, square-root-intTest.cc square-root-int.cc, SquareRootIntTest.java SquareRootInt.java))
#sudoku-solve
$(eval $(call add_target, sudoku-solve.json, Sudoku_solveTest.cc Sudoku_solve.cc, SudokuSolveTest.java SudokuSolve.java SudokuCheck.java))

# One generic rule for all $(TARGETS)     
$(TARGETS) : % :
#@echo Making $@ from $^
	$(PYTHON) $(GENERATOR) $(TEST_OPTION) --output=$@ --template=$(word 2,$^) --cpp=$(word 3,$^) --java=$(word 4,$^)

all : check-env $(TARGETS)

check-env:
ifndef EPICODE_ROOT
    $(error EPICODE_ROOT is undefined)
endif

clean:
	rm $(TARGETS)

.PHONY: all clean check-env