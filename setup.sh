#!/bin/bash
# Setup script for e2e testing framework

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print status messages
print_status() {
    echo -e "${GREEN}[✓] $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}[!] $1${NC}"
}

print_error() {
    echo -e "${RED}[✗] $1${NC}"
}

# Detect OS
OS_TYPE="$(uname -s)"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.12 or higher."
    exit 1
fi

# Check Python version
python3 --version | grep -q "Python 3.12" || { echo "Python 3.12 is required"; exit 1; }

# Create virtual environment if it doesn't exist
if [ ! -d "e2e_venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv e2e_venv
else
    print_warning "Virtual environment already exists. Skipping creation."
fi

# Activate virtual environment if sourced
if [[ "${BASH_SOURCE[0]}" != "${0}" ]]; then
    echo "Activating virtual environment..."
    source e2e_venv/bin/activate
elif [[ "$OS_TYPE" =~ MINGW* || "$OS_TYPE" =~ MSYS* || "$OS_TYPE" =~ CYGWIN* ]]; then
    print_warning "On Windows, please activate the virtual environment manually:"
    echo -e "    ${GREEN}./e2e_venv/Scripts/activate${NC} (for Git Bash)"
    echo -e "    ${GREEN}e2e_venv\\Scripts\\activate${NC} (for CMD/PowerShell)"
else
    print_warning "Unknown OS. Please activate the virtual environment manually."
fi

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Install Playwright
echo "Installing Playwright..."
pip install playwright
playwright install

# Create necessary directories
echo "Creating directories..."
mkdir -p test-result/{screenshots,html,allure-results}

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
fi

# Verify installation
echo "Verifying installation..."
python3 -c "import pytest; import playwright; print('Setup completed successfully!')"

# Print next steps
echo "
Next steps:
1. Review and modify .env file if needed
2. Run tests using: python -m pytest
"

if [[ "$OS_TYPE" == "Linux" || "$OS_TYPE" == "Darwin" ]]; then
    echo -e "\nYou are now in the virtual environment. To run tests, use:"
    echo -e "    ${GREEN}python -m pytest${NC}"
    echo -e "    ${GREEN}python -m pytest -v${NC} (for verbose output)"
    echo -e "    ${GREEN}python -m pytest tests/ui/test_parabank_login.py${NC} (for specific test)"
else
    echo -e "\nTo activate the virtual environment, run:"
    echo -e "    ${GREEN}./e2e_venv/Scripts/activate${NC} (for Git Bash)"
    echo -e "    ${GREEN}e2e_venv\\Scripts\\activate${NC} (for CMD/PowerShell)"
    echo -e "\nThen run your tests as above."
fi 