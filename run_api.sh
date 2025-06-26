#!/bin/bash

# Shell script to run the FastAPI REST API until manually stopped

set -e  # Exit on any error

echo "Starting FastAPI Cryptocurrency REST API..."
echo "The API will run until manually stopped (Ctrl+C)"
echo "API will be available at http://localhost:8000"
echo "================================"

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

# Check if main.py exists
if [ ! -f "main.py" ]; then
    echo "Error: main.py not found in current directory"
    echo "Make sure you're running this script from the project root"
    exit 1
fi

# Run the FastAPI application
echo "Starting FastAPI development server..."
fastapi dev main.py

echo "API server stopped."
