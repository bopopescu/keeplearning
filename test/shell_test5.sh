#!/bin/bash
echo "program name:" $0
echo "program pid:" $$
echo "the frist arg:" $1
echo "the second arg:" $2
echo "the third arg:" $3
echo "the number of the args:" $#
echo "the args is:" "$@"
echo "the args is:" "$*"
echo "the last arg of the pre-program:" "$_"
