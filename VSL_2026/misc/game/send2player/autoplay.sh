#!/bin/bash
{
  sleep 1
  echo "14.225.212.104"
  sleep 0.5
  echo "9999"
  sleep 1
  for i in {1..20}; do
    echo "1"
    sleep 0.3
  done
} | ./client.exe 2>&1 | tee full_output.txt
