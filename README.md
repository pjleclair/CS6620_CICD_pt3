# CS6620_CICD_pt3

### This Python app is a FastAPI application that provides REST endpoints for item management with DynamoDB and S3 storage.

### Features:

- **GET /items**: Returns a list of all items
- **GET /items/{item_id}**: Get detailed information for a specific item
- **POST /items**: Create a new item (stores in DynamoDB and S3)
- **PUT /items/{item_id}**: Update an existing item
- **DELETE /items/{item_id}**: Delete an item from both DynamoDB and S3

### The app includes comprehensive tests and is fully containerized with Docker, using LocalStack for AWS service mocking.

## Local Development Setup

### Prerequisites:

- Git
- Conda
- Python 3.11+

### Installation:

1. Clone the repository:

   ```bash
   git clone git@github.com:pjleclair/CS6620_CICD_pt3.git
   cd CS6620_CICD_pt3
   ```

2. Create and activate the conda environment:

   ```bash
   conda env create -f environment.yml
   conda activate CICD_pt3
   ```

3. Run the application locally:

   ```bash
   fastapi dev main.py
   ```

4. Run tests locally:
   ```bash
   pytest test_app.py
   ```

The app will be available at `http://localhost:8000`

## Docker Setup

### Prerequisites:

- Docker
- Docker Compose

### Running with Docker:

1. Build and start the application:

   ```bash
   ./run_api.sh
   ```

2. Run tests in Docker:
   ```bash
   ./run_tests.sh
   ```

The containerized app will be available at `http://localhost:8000`

## Testing

Tests verify all endpoints return appropriate status codes and handle both valid and invalid requests. The test suite runs automatically as part of the CI/CD pipeline.

## Disclaimer

Used Claude for assistance implementing AWS services integration (DynamoDB, S3) with LocalStack
