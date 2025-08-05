#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Download NLTK data (required for the ML service)
python -c "
import nltk
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
"

# Collect static files
python manage.py collectstatic --noinput

echo "Build completed successfully!"