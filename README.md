# Modern Django Portfolio Website

A modern, feature-rich portfolio website built with Django 5.1, featuring machine learning integration, REST API, and responsive design.

![Portfolio Screenshot](static/images/portfolio-preview.jpg)

## 🚀 Features

- **Modern Django 5.1** with latest best practices
- **Machine Learning Integration** - Spam classification service
- **REST API** with Django REST Framework
- **Interactive Frontend** with Bootstrap 5 and modern JavaScript
- **Responsive Design** with dark/light theme support
- **Portfolio Management** - Projects, skills, experience, and personal info
- **Contact System** with email notifications
- **Admin Interface** for content management
- **API Documentation** with Swagger/OpenAPI
- **Production Ready** with Docker, Nginx, and Gunicorn
- **Security Focused** with rate limiting and CSRF protection
- **Comprehensive Testing** with pytest and coverage
- **Performance Optimized** with caching and static file compression

## 🛠️ Technology Stack

### Backend
- **Django 5.1** - Web framework
- **Django REST Framework** - API development
- **PostgreSQL** - Database (SQLite for development)
- **Redis** - Caching and sessions
- **Celery** - Async task processing (optional)

### Frontend
- **Bootstrap 5** - CSS framework
- **Modern JavaScript** - ES6+ features
- **AOS** - Animations on scroll
- **Bootstrap Icons** - Icon library

### Machine Learning
- **scikit-learn** - ML models
- **NLTK** - Natural language processing
- **Pandas & NumPy** - Data processing

### DevOps & Deployment
- **Docker** - Containerization
- **Nginx** - Reverse proxy and static files
- **Gunicorn** - WSGI server
- **Supervisor** - Process management

### Development Tools
- **pytest** - Testing framework
- **Black** - Code formatting
- **Flake8** - Code linting
- **isort** - Import sorting

## 📋 Prerequisites

- Python 3.11+
- Docker and Docker Compose (for containerized deployment)
- Git

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd django-portfolio-website
```

### 2. Environment Setup

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database
DATABASE_URL=sqlite:///db.sqlite3

# Email
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Redis (optional for development)
REDIS_URL=redis://localhost:6379/0
```

### 3. Local Development

#### Option A: Traditional Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run development server
python manage.py runserver
```

#### Option B: Docker Development

```bash
# Start development environment
docker-compose up --build

# Create superuser (in another terminal)
docker-compose exec web python manage.py createsuperuser
```

### 4. Access the Application

- **Website**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin/
- **API Documentation**: http://localhost:8000/api/docs/
- **API Root**: http://localhost:8000/api/

## 📁 Project Structure

```
django-portfolio-website/
├── apps/                          # Django applications
│   ├── core/                      # Core functionality
│   ├── portfolio/                 # Portfolio management
│   └── ml_service/               # Machine learning service
├── dennisivy/                     # Django project settings
├── templates/                     # HTML templates
├── static/                        # Static files (CSS, JS, images)
├── media/                         # User uploaded files
├── docker/                        # Docker configuration
├── logs/                         # Application logs
├── tests/                        # Test files
├── requirements.txt              # Python dependencies
├── pytest.ini                   # Testing configuration
├── Dockerfile                    # Production container
├── Dockerfile.dev               # Development container
├── docker-compose.yml           # Multi-container setup
└── README.md                     # This file
```

## 🎯 Core Applications

### Core App (`apps.core`)
- Homepage with portfolio overview
- Contact form handling
- Base models and utilities

### Portfolio App (`apps.portfolio`)
- Personal information management
- Project showcase
- Skills and technologies
- Work experience and education
- REST API endpoints

### ML Service App (`apps.ml_service`)
- Spam classification using machine learning
- Model management and predictions
- API endpoints for ML services
- Classification history tracking

## 🔧 Configuration

### Environment Variables

Key environment variables in `.env`:

```env
# Django Core
SECRET_KEY=your-secret-key
DEBUG=True/False
ALLOWED_HOSTS=comma,separated,hosts

# Database
DATABASE_URL=postgresql://user:pass@host:port/db

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# AWS S3 (Optional)
USE_S3=True/False
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket

# Security
CORS_ALLOWED_ORIGINS=http://localhost:3000
SENTRY_DSN=your-sentry-dsn

# Caching
REDIS_URL=redis://localhost:6379/0
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apps --cov-report=html

# Run specific test categories
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m "not slow"    # Exclude slow tests
```

## 📊 API Documentation

The project includes comprehensive API documentation:

- **Swagger UI**: `/api/docs/` - Interactive API documentation
- **ReDoc**: `/api/redoc/` - Alternative API documentation
- **Schema**: `/api/schema/` - OpenAPI schema

### API Endpoints

#### Portfolio API (`/api/portfolio/`)
- `GET /skills/` - List all skills
- `GET /projects/` - List all projects
- `GET /projects/{slug}/` - Project details
- `GET /experience/` - List experience
- `GET /personal-info/` - Personal information

#### ML Service API (`/api/ml/`)
- `POST /classify/` - Classify text for spam
- `GET /history/` - Classification history
- `GET /health/` - Service health check

#### Core API
- `POST /contact/` - Send contact message

## 🚀 Production Deployment

### Docker Production Setup

1. **Build and run with Docker Compose:**

```bash
# Update environment variables in docker-compose.yml
# Build and start services
docker-compose up -d --build

# Check service status
docker-compose ps

# View logs
docker-compose logs -f web
```

2. **Manual Docker Build:**

```bash
# Build production image
docker build -t portfolio-app .

# Run with environment variables
docker run -d \
  --name portfolio \
  -p 80:80 \
  -e SECRET_KEY=your-secret-key \
  -e DEBUG=False \
  -e DATABASE_URL=postgresql://user:pass@host/db \
  portfolio-app
```

### Environment-specific Settings

Create separate environment files:
- `.env.development`
- `.env.staging`
- `.env.production`

### Health Checks

The application includes health check endpoints:
- `/api/ml/health/` - ML service health
- Built-in Docker health checks

### Monitoring and Logging

- Application logs: `/app/logs/`
- Nginx logs: `/var/log/nginx/`
- Supervisor logs: `/var/log/supervisor/`
- Sentry integration for error monitoring

## 🔒 Security Features

- **CSRF Protection** - Built-in Django CSRF
- **Rate Limiting** - API endpoint rate limiting
- **Security Headers** - Comprehensive security headers
- **Input Validation** - Strict input validation
- **SQL Injection Protection** - Django ORM protection
- **XSS Prevention** - Template auto-escaping
- **HTTPS Ready** - SSL/TLS configuration ready

## 🎨 Customization

### Adding New Portfolio Items

1. **Skills**: Use Django admin to add new skills
2. **Projects**: Create projects with detailed descriptions
3. **Experience**: Add work experience and education
4. **Personal Info**: Update personal information and social links

### Customizing Themes

The frontend supports light/dark themes. Customize in:
- `static/css/style.css`
- `static/js/main.js`

### Adding New ML Models

1. Add model files to project root
2. Update `apps/ml_service/services.py`
3. Create new API endpoints in `apps/ml_service/views.py`

## 🔧 Development Workflow

### Code Quality

```bash
# Format code
black .

# Check code quality
flake8

# Sort imports
isort .

# Run all quality checks
black . && isort . && flake8
```

### Database Operations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset database (development only)
python manage.py flush

# Load sample data
python manage.py loaddata fixtures/sample_data.json
```

### Static Files

```bash
# Collect static files
python manage.py collectstatic

# Clear cache
python manage.py clear_cache
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests: `pytest`
5. Commit changes: `git commit -am 'Add feature'`
6. Push to branch: `git push origin feature-name`
7. Submit a pull request

### Development Guidelines

- Follow PEP 8 style guide
- Write tests for new features
- Update documentation
- Use meaningful commit messages
- Keep dependencies minimal

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Issues](../../issues) section
2. Review the documentation
3. Check logs for error details
4. Create a new issue with detailed information

## 🙏 Acknowledgments

- Django community for the excellent framework
- Bootstrap team for the responsive framework
- scikit-learn team for machine learning tools
- All contributors and maintainers

---

**Built with ❤️ using Django 5.1 and modern web technologies**
