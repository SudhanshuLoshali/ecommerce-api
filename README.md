# E-commerce-Platform

A simple e-commerce platform built with FastAPI.

## Features

- Product management (listing and creation)
- Order placement with stock validation
- Exception handling
- Test coverage
- Dockerized deployment

## Prerequisites

- Python 3.9+
- Docker
- pip

## Local Development

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

## Docker Deployment

### Using Docker

1. Build the image:
```bash
docker build -t ecommerce-api .
```

2. Run the container:
```bash
docker run -d \
  --name ecommerce-api \
  -p 8000:8000 \
  -e DATABASE_URL=sqlite:///./data/ecommerce.db \
  -e PORT=8000 \
  ecommerce-api
```

### Using Docker Compose

1. Start the services:
```bash
docker-compose up -d
```

2. View logs:
```bash
docker-compose logs -f
```

### Environment Variables

The following environment variables can be configured:

- `PORT`: Application port (default: 8000)
- `HOST`: Application host (default: 0.0.0.0)
- `DATABASE_URL`: Database connection string (default: sqlite:///./ecommerce.db)

## API Documentation

Once the application is running, you can access:
- API documentation: http://localhost:8000/docs
- Alternative API documentation: http://localhost:8000/redoc

### Endpoints

- `GET /products`: Retrieve all products
- `POST /products`: Create a new product
- `POST /orders`: Place a new order

## Testing

Run the tests using pytest:
```bash
pytest
```

## Error Handling

The API implements comprehensive error handling for:
- Insufficient stock
- Product not found
- Invalid input data
- Database errors