#!/bin/bash

file_path=$1

if [ "$(wc -l < "$file_path")" -lt 10000 ]; then
	echo "File has less than 10000 lines."
	exit 2
fi


echo "$(wc -l < "$file_path" | tr -d ' ')"

echo "$(head -n 1 "$file_path")"

echo "$(tail -n 10000 "$file_path" | grep -i "potus" | wc -l | tr -d ' ')"

echo "$(sed -n '100,200p' "$file_path" | grep -i "fake" | wc -l | tr -d ' ')"