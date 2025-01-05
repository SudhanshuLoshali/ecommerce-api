# E-commerce Platform

A simple e-commerce platform built with FastAPI, featuring product management and order processing.

## Features

- Product management (listing and creation)
- Order placement with stock validation
- Exception handling for common scenarios
- SQLite database with SQLAlchemy ORM
- Docker containerization with data persistence
- Health checks and monitoring
- Test coverage

## Prerequisites

- Python 3.9+
- Docker and Docker Compose
- pip
- curl (for healthchecks)

## Installation & Setup

### Local Development

1. Clone the repository:
```bash
git clone <repository-url>
cd ecommerce-api
```
2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Run the application:
```bash
uvicorn app.main:app --reload
```
The API will be available at ```http://localhost:8000```

### Docker Deployment
1. Using Docker:
```bash
# Build the image
docker build -t ecommerce-api .

# Run the container
docker run -d \
  --name ecommerce-api \
  -p 8000:8000 \
  -v db-data:/app/data \
  ecommerce-api
```

2. Using Docker Compose:
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## Environment Variables

The following environment variables can be configured:

- `PORT`: Application port (default: 8000)
- `HOST`: Application host (default: 0.0.0.0)
- `DATABASE_URL`: Database connection string (sqlite:///./data/ecommerce.db)

## API Documentation

Once the application is running, you can access:
- API documentation: http://localhost:8000/docs
- Alternative API documentation: http://localhost:8000/redoc

## Endpoints

- `GET /products`: Retrieve all products
- `POST /products`: Create a new product
- `POST /orders`: Place a new order


## Data Persistence
The application uses SQLite with data stored in a Docker volume. To manage volumes:
```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect db-data

# Remove volume
docker volume rm db-data
```

## Testing

Run the tests using pytest:
```bash
pytest
```

## Error Handling

| Error | Status Code | Description |
|-------|-------------|-------------|
| ProductNotFoundException | 404 | Product not found |
| InsufficientStockException | 400 | Not enough stock available |
| ValidationError | 422 | Invalid input data |
| DatabaseError | 500 | Database operation failed |

## Health Checks
The application includes Docker health checks that:
- Run every 30 seconds
- Timeout after 30 seconds
- Have 3 retries
- Have a 5-second start period
