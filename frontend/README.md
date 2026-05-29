"""Frontend setup and deployment guide."""
# Frontend Setup Guide

## Prerequisites
- Node.js 18+ and npm installed
- Backend API running on http://localhost:8000

## Local Development

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Configure Environment
Create `.env` file in frontend directory:
```env
REACT_APP_API_URL=http://localhost:8000/api
```

### 3. Start Development Server
```bash
npm start
```

The app will open at `http://localhost:3000`

## Build for Production

```bash
cd frontend
npm run build
```

This creates an optimized production build in the `build/` directory.

## Docker Deployment

### Build Frontend Image
```bash
docker build -f frontend/Dockerfile -t rag-frontend:latest .
```

### Run with Docker Compose
```bash
docker-compose up -d
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api
- Combined (via Nginx): http://localhost

## Features

### Chat Interface
- Real-time message display
- Message animations
- Copy message functionality
- Loading indicators

### Document Upload
- Drag & drop support
- Multiple file upload
- Progress tracking
- Supported formats: PDF, TXT, JPG, PNG, GIF

### Citations
- Expandable citations viewer
- Links to sources
- Citation type display
- Author & year information

### Settings Panel
- Model configuration display
- Supported languages list
- Index statistics
- Application information

### Sidebar
- Document count
- Chat history counter
- Theme toggle (dark/light mode)
- Quick actions (clear history, save index)
- Real-time stats update

## Styling

The application uses:
- CSS3 Flexbox and Grid
- CSS Variables for theming
- Dark/Light mode support
- Responsive design (mobile, tablet, desktop)
- Smooth transitions and animations

### Theme Variables
```css
--primary: #3b82f6
--secondary: #8b5cf6
--success: #10b981
--danger: #ef4444
```

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Troubleshooting

### Backend not connecting
- Ensure backend is running on http://localhost:8000
- Check REACT_APP_API_URL in .env
- Check browser console for CORS errors

### Build fails
- Delete node_modules and package-lock.json
- Run `npm ci` to reinstall dependencies
- Check Node version (requires 18+)

### Styles not loading
- Clear browser cache (Ctrl+Shift+Delete)
- Restart development server
- Check if CSS files are present in src/styles/

## Performance Tips

1. **Image Optimization**: Use modern image formats
2. **Code Splitting**: Components are already optimized
3. **Lazy Loading**: Implement for large documents
4. **Caching**: Browser caches API responses

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| REACT_APP_API_URL | http://localhost:8000/api | Backend API URL |
| NODE_ENV | development | Build environment |

## See Also
- [Backend API Documentation](../backend/README.md)
- [Main README](../README.md)
