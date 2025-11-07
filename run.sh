#!/bin/bash
# Simple script to run the domain search web application

echo "Starting Domain Search Web Application..."
echo "Access the application at: http://localhost:8000"
echo ""

cd domain_search
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
