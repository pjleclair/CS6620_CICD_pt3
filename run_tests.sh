#!/bin/bash

# Shell script to run tests and exit with appropriate status code

set -e  # Exit on any error

echo "Running FastAPI Cryptocurrency App Tests..."
echo "=========================================="

# Check if conda environment exists and activate it
if conda env list | grep -q "CICD_pt2"; then
    echo "Activating conda environment: CICD_pt2"
    source $(conda info --base)/etc/profile.d/conda.sh
    conda activate CICD_pt2
else
    echo "Warning: CICD_pt2 conda environment not found"
    echo "Make sure to create it with: conda env create -f environment.yml"
    echo "Continuing with current environment..."
fi

# Check if test file exists
if [ ! -f "test_app.py" ]; then
    echo "Error: test_app.py not found in current directory"
    echo "Make sure you're running this script from the project root"
    exit 1
fi

# Run the tests with pytest
echo "Executing pytest..."
if pytest test_app.py -v; then
    echo "=========================================="
    echo "✅ All tests passed successfully!"
    echo "Exiting with status code 0"
    exit 0
else
    echo "=========================================="
    echo "❌ Tests failed!"
    echo "Exiting with non-zero status code"
    exit 1
fi
