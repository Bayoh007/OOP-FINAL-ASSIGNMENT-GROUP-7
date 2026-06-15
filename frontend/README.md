# Royal Fitness Frontend

A modern, responsive authentication frontend for the Royal Fitness API.

## Features

- ✓ User Registration
- ✓ User Login
- ✓ Dashboard with Token Display
- ✓ Persistent Login (LocalStorage)
- ✓ Form Validation
- ✓ Real-time Feedback Messages
- ✓ Responsive Design
- ✓ Beautiful UI with Gradient Background

## Files

- **index.html** - Main HTML structure with login, registration, and dashboard forms
- **style.css** - Complete CSS styling with animations and responsive design
- **app.js** - JavaScript logic for form handling and API communication

## How to Use

### Option 1: Using LiveServer (VS Code)
1. Install "Live Server" extension in VS Code
2. Right-click on `index.html`
3. Select "Open with Live Server"
4. Browser opens to `http://127.0.0.1:5500/frontend/`

### Option 2: Using Python HTTP Server
```bash
cd frontend
python -m http.server 8080
```
Then open `http://127.0.0.1:8080/`

### Option 3: Using Node.js HTTP Server
```bash
npm install -g http-server
cd frontend
http-server
```

## API Configuration

The frontend connects to the FastAPI backend at:
```
http://127.0.0.1:8000
```

If your backend is running on a different host/port, update the `API_BASE_URL` in `app.js`:
```javascript
const API_BASE_URL = 'http://your-host:your-port';
```

## Features

### Registration
- Enter Full Name, Email, Password
- Passwords must match and be at least 6 characters
- Email must be valid and unique
- Success redirects to login form

### Login
- Enter Email and Password
- Stores JWT token in localStorage
- Shows dashboard with token
- Can logout anytime

### Dashboard
- Shows welcome message with email
- Displays access token
- Logout button to clear session

## Notes

- CORS is already configured in FastAPI (`allow_origins=["*"]`)
- Tokens are stored in browser's localStorage (not production-safe for sensitive data)
- All form validations are performed client-side
- Backend also validates all inputs

## Browser Support

- Chrome/Edge (Latest)
- Firefox (Latest)
- Safari (Latest)
- Mobile browsers

## Security Notes

For production:
- Move API_BASE_URL to environment variables
- Use HTTPS only
- Implement token refresh mechanism
- Add rate limiting
- Use HttpOnly cookies instead of localStorage for tokens
- Implement proper session management
