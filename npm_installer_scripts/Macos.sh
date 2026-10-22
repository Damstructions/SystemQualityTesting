#!/bin/bash
if command -v npm >/dev/null 2>&1; then
  echo "npm already installed: $(npm --version)"
  exit 0
fi

echo "npm not found. Installing Node.js..."

if command -v brew >/dev/null 2>&1; then
  brew install node
else
  # Fallback: nvm (user-level, no sudo required)
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
  export NVM_DIR="$HOME/.nvm"
  [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
  nvm install --lts
fi

# Refresh current shell if possible
if command -v npm >/dev/null 2>&1; then
  echo "Installed: $(npm --version)"
else
  echo "Please open a new terminal and run: npm --version"
fi