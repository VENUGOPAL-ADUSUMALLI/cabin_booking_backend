#!/usr/bin/env bats

setup() {
  # executed before each test
  echo "setup" >&3
}

teardown() {
  # executed after each test
  echo "teardown" >&3
}

@test "test_name" {
  true
}
