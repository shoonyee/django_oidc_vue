# Full Stack Application with Django + Vue.js

A modern full-stack web application featuring a Django backend with OIDC authentication via U-M Shibboleth and a Vue 3 frontend with Vuetify.

## Features

- **Backend**: Django REST API with OIDC authentication
- **Frontend**: Vue 3 + Vuetify with responsive design
- **Authentication**: OIDC integration with University of Michigan Shibboleth
- **Models**: Two sample models (Model1, Model2) with CRUD operations
- **Contact Form**: Public contact form (no authentication required)
- **Responsive Design**: Mobile-friendly interface

## Project Structure

```
├── backend/                 # Django backend application
│   ├── backend/            # Django project settings
│   ├── api/                # API app with models and views
│   ├── manage.py           # Django management script
│   └── requirements.txt    # Python dependencies
├── frontend/               # Vue.js frontend application
│   ├── src/                # Source code
│   │   ├── views/          # Vue components
│   │   ├── stores/         # Pinia state management
│   │   └── router/         # Vue Router configuration
│   ├── package.json        # Node.js dependencies
│   └── vite.config.js      # Vite configuration
└── README.md               # This file
```

## Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn
- Access to U-M Shibboleth (for OIDC authentication)

## Quick Start

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your U-M OIDC configuration
   ```

5. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start Django server:**
   ```bash
   python manage.py runserver
   ```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:3000`

## API Endpoints

### Public Endpoints (No Authentication Required)
- `GET /api/public/health_check/` - Health check
- `GET /api/public/public_info/` - Application information
- `POST /api/contact/` - Submit contact form

### Protected Endpoints (Authentication Required)
- `GET /api/model1/` - List Model1 entries
- `POST /api/model1/` - Create Model1 entry
- `PUT /api/model1/{id}/` - Update Model1 entry
- `DELETE /api/model1/{id}/` - Delete Model1 entry
- `GET /api/model2/` - List Model2 entries
- `POST /api/model2/` - Create Model2 entry
- `PUT /api/model2/{id}/` - Update Model2 entry
- `DELETE /api/model2/{id}/` - Delete Model2 entry
- `POST /api/model2/{id}/toggle_active/` - Toggle Model2 active status

### Authentication Endpoints
- `GET /api/auth/user/` - Get current user information
- `GET /oidc/authenticate/` - Redirect to U-M OIDC login
- `GET /oidc/logout/` - Redirect to U-M OIDC logout

## Authentication

The application uses OIDC (OpenID Connect) authentication with U-M Shibboleth. **There is no custom login interface** - users are automatically redirected to U-M's official login page when authentication is required.

### How It Works

1. **No Custom Login**: The frontend has no login forms or custom authentication
2. **Automatic Redirects**: When accessing protected routes, users are automatically sent to U-M Shibboleth
3. **Seamless Integration**: After successful U-M authentication, users are redirected back to the app
4. **Session Management**: Django handles OIDC sessions automatically

### U-M Shibboleth OIDC Configuration

The application is configured to work with U-M's official OIDC endpoints from [https://shibboleth.umich.edu/.well-known/openid-configuration](https://shibboleth.umich.edu/.well-known/openid-configuration):

- **Issuer**: `https://shibboleth.umich.edu`
- **Authorization Endpoint**: `https://shibboleth.umich.edu/idp/profile/oidc/authorize`
- **Token Endpoint**: `https://shibboleth.umich.edu/idp/profile/oidc/token`
- **User Info Endpoint**: `https://shibboleth.umich.edu/idp/profile/oidc/userinfo`
- **JWKS Endpoint**: `https://shibboleth.umich.edu/oidc/keyset.jwk`

### Supported Scopes and Claims

Based on U-M's OIDC configuration, the application supports:
- **Scopes**: `openid`, `email`, `profile`, `eduperson`, `edumember`
- **Claims**: Standard OIDC claims plus U-M specific attributes like `eduperson_principal_name`, `eduperson_affiliation`, `edumember_is_member_of`

### Configuration

Update the following environment variables in `backend/.env`:

```bash
OIDC_CLIENT_ID=your-app-client-id
OIDC_CLIENT_SECRET=your-app-client-secret
OIDC_AUTHORIZATION_ENDPOINT=https://shibboleth.umich.edu/idp/profile/oidc/authorize
OIDC_TOKEN_ENDPOINT=https://shibboleth.umich.edu/idp/profile/oidc/token
OIDC_USER_ENDPOINT=https://shibboleth.umich.edu/idp/profile/oidc/userinfo
OIDC_JWKS_ENDPOINT=https://shibboleth.umich.edu/oidc/keyset.jwk
```

**Note**: You'll need to register your application with U-M IT to obtain the client ID and secret.

## Development

### Backend Development

- The Django backend uses Django REST Framework for API endpoints
- Models are defined in `backend/api/models.py`
- Views and serializers are in `backend/api/views.py` and `backend/api/serializers.py`
- Admin interface is available at `/admin/` for data management
- OIDC authentication is handled by `mozilla-django-oidc`

### Frontend Development

- Built with Vue 3 Composition API
- Uses Vuetify 3 for Material Design components
- State management with Pinia
- Routing with Vue Router 4
- HTTP requests with Axios
- Automatic OIDC redirects for authentication

## Deployment

### Backend Deployment

1. Set `DEBUG=False` in production
2. Use a production database (PostgreSQL recommended)
3. Configure static files with WhiteNoise
4. Set up proper CORS settings for production domains
5. Ensure HTTPS is enabled for OIDC security

### Frontend Deployment

1. Build the production version:
   ```bash
   npm run build
   ```
2. Deploy the `dist/` folder to your web server
3. Configure API proxy settings for production

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For questions or support, please contact the development team or submit an issue through the project repository.

## U-M Shibboleth Integration Notes

- **Security**: Uses RS256 signing algorithm as supported by U-M
- **Scopes**: Includes U-M specific scopes for enhanced user information
- **Claims**: Handles both standard OIDC and U-M specific user attributes
- **Compliance**: Follows U-M's OIDC implementation standards
