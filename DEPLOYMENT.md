# Vercel Deployment Guide

This guide will help you deploy your Django application to Vercel.

## Prerequisites

1. ✅ **GitHub Connection**: You've already connected your GitHub repository to Vercel
2. ✅ **Vercel Secret Token**: You've already added the secret token

## Files Created for Deployment

The following files have been created/modified for Vercel deployment:

- `vercel.json` - Vercel configuration file
- `build.sh` - Build script for collecting static files and NLTK data
- `.env.example` - Example environment variables
- Updated `requirements.txt` - Vercel-compatible dependencies
- Updated `dennisivy/settings.py` - Vercel-specific configurations

## Environment Variables Required

In your Vercel project dashboard, add these environment variables:

### Required Variables:
```
SECRET_KEY=your-secret-key-here-generate-a-new-one
DEBUG=False
ALLOWED_HOSTS=.vercel.app
DATABASE_URL=sqlite:///db.sqlite3
```

### Optional Variables (for enhanced functionality):
```
# CORS (if you have a frontend)
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com

# Email (if using email features)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

# AWS S3 (if you want to use S3 for media files)
USE_S3=False
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
AWS_S3_REGION_NAME=us-east-1

# Monitoring (optional)
SENTRY_DSN=
```

## Deployment Steps

### 1. Set Environment Variables in Vercel
1. Go to your Vercel project dashboard
2. Navigate to Settings → Environment Variables
3. Add the required environment variables listed above

### 2. Generate a New Secret Key
Generate a new Django secret key for production:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### 3. Deploy
1. Push your code to GitHub
2. Vercel will automatically detect the changes and deploy
3. The deployment process will:
   - Install dependencies from `requirements.txt`
   - Run the `build.sh` script
   - Download NLTK data
   - Collect static files
   - Deploy the application

### 4. Run Database Migrations (First Deployment Only)
After the first successful deployment, you may need to run migrations:
1. Go to your Vercel project dashboard
2. Navigate to the Functions tab
3. Find your Django function and run migrations via Vercel CLI or create a management command

## Important Notes

### Database
- **SQLite**: The app is configured to use SQLite by default on Vercel
- **PostgreSQL**: If you want to use PostgreSQL, set up a database service (like PlanetScale, Supabase, or Railway) and update the `DATABASE_URL` environment variable

### Static Files
- Static files are handled by WhiteNoise middleware
- The `build.sh` script collects static files during deployment
- Static files are served from the `/staticfiles/` directory

### Machine Learning Models
- The pickle files (`feature_extraction.pickle`, `best_svc.pickle`, `X_train.pickle`) are included in the repository
- NLTK data is downloaded during the build process

### File Storage
- For development: Local file storage
- For production: Consider using AWS S3 or similar (set `USE_S3=True` and configure AWS credentials)

### Limitations on Vercel
- **Serverless Functions**: Each request runs in a stateless environment
- **File System**: The file system is read-only except for `/tmp`
- **Execution Time**: Functions have a maximum execution time limit
- **Memory**: Limited memory per function execution

## Troubleshooting

### Common Issues:

1. **Build Fails**: Check the build logs in Vercel dashboard
2. **Import Errors**: Make sure all dependencies are in `requirements.txt`
3. **Static Files Not Loading**: Ensure `whitenoise` is in middleware and `collectstatic` runs
4. **Database Errors**: Check your `DATABASE_URL` environment variable

### Logs
Check the Vercel function logs for any runtime errors:
1. Go to Vercel dashboard
2. Navigate to Functions tab
3. Click on your function to view logs

## Local Development

To test locally with the same configuration:

1. Copy `.env.example` to `.env`
2. Update the values in `.env`
3. Run:
   ```bash
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py collectstatic
   python manage.py runserver
   ```

## Production Checklist

- [ ] All environment variables set in Vercel
- [ ] New secret key generated and added
- [ ] Database migrations applied
- [ ] Static files collecting properly
- [ ] ML models loading correctly
- [ ] API endpoints responding
- [ ] Admin panel accessible (if needed)

## Support

If you encounter issues:
1. Check Vercel deployment logs
2. Verify environment variables
3. Test the application locally first
4. Check Django logs in Vercel function logs