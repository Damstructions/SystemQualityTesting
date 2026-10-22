#!/bin/bash
if command -v npm >/dev/null 2>&1; then
  echo "npm already installed: $(npm --version)"
  exit 0
fi

echo "npm not found. Installing Node.js..."

if command -v apt-get >/dev/null 2>&1; then
  sudo apt-get update
  sudo apt-get install -y nodejs npm
elif command -v dnf >/dev/null 2>&1; then
  sudo dnf install -y nodejs npm
elif command -v yum >/dev/null 2>&1; then
  sudo yum install -y nodejs npm
elif command -v pacman >/dev/null 2>&1; then
  sudo pacman -S --noconfirm nodejs npm
else
  echo "Unsupported package manager."
  exit 1
fi

echo "Installed: $(npm --version 2>/dev/null || echo 'Please open a new shell')"