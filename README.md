# CS6620_CICD_pt2

### This Python app is a FastAPI application that provides REST endpoints for cryptocurrency data from the CoinGecko API.

### Features:

- **GET /**: Returns a list of all available cryptocurrencies
- **POST /coins/{coin_id}**: Get detailed information for a specific cryptocurrency
- **PUT /coins/{coin_id}**: Mock endpoint that returns a creation confirmation
- **DELETE /coins/{coin_id}**: Mock endpoint that returns a deletion confirmation

### The app includes comprehensive tests and is fully containerized with Docker.

## Local Development Setup

### Prerequisites:

- Git
- Conda
- Python 3.11+

### Installation:

1. Clone the repository:

   ```bash
   git clone git@github.com:pjleclair/CS6620_CICD_pt2.git
   cd CS6620_CICD_pt2
   ```

2. Create and activate the conda environment:

   ```bash
   conda env create -f environment.yml
   conda activate CICD_pt2
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
   docker-compose up --build
   ```

2. Run tests in Docker:
   ```bash
   docker-compose run test
   ```

The containerized app will be available at `http://localhost:8000`

## Testing

Tests verify all endpoints return appropriate status codes and handle both valid and invalid requests. The test suite runs automatically as part of the CI/CD pipeline.
