#!/bin/bash

YELLOW='\033[33m'
RESET='\033[0m'

for test_file in $(find "./test/" -type f -executable -print); do
	echo -e "$YELLOW##>----------- Running [$test_file]$RESET"
	$test_file
	echo
done
