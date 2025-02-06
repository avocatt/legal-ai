# Frontend Application

## Architecture

The frontend is a modern React application built with TypeScript and Material-UI, providing a clean and intuitive interface for the Turkish Legal AI system.

### Project Structure

```
frontend/
├── src/
│   ├── components/        # Reusable UI components
│   ├── services/         # API integration services
│   ├── types/           # TypeScript type definitions
│   ├── hooks/           # Custom React hooks
│   ├── utils/           # Utility functions
│   └── App.tsx          # Main application component
├── public/              # Static assets
└── vite.config.ts       # Vite configuration
```

## Features

### User Interface
- Clean, modern Material-UI design
- Responsive layout for all devices
- Dark/light theme support
- Loading states and error handling

### Question-Answer Interface
- Real-time question input
- Markdown-rendered responses
- Source citation display
- Confidence score indicators

### API Integration
- Axios-based API client
- Request/response type safety
- Error handling middleware
- Loading state management

## Setup

1. Install dependencies:
```bash
npm install
```

2. Set up environment:
```bash
cp .env.example .env
# Edit .env with your API URL
```

3. Start development server:
```bash
npm run dev
```

4. Build for production:
```bash
npm run build
```

## Development

### Code Style
- Follow TypeScript best practices
- Use ESLint and Prettier
- Follow component composition patterns
- Implement proper error boundaries

### Component Guidelines
1. Keep components focused and small
2. Use TypeScript interfaces
3. Implement proper prop validation
4. Document component usage
5. Include unit tests

### State Management
- React Query for API state
- Context for theme/global state
- Local state for component-specific data

## Testing

```bash
# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific test file
npm test -- src/components/QuestionInput.test.tsx
```

## Building and Deployment

### Development
```bash
npm run dev
```

### Production Build
```bash
npm run build
npm run preview
```

### Docker Build
```bash
docker build -t legal-ai-frontend .
docker run -p 80:80 legal-ai-frontend
```

## Performance

### Optimization Techniques
- Code splitting
- Lazy loading
- Image optimization
- Caching strategies

### Monitoring
- Performance metrics
- Error tracking
- User analytics

## Accessibility

### Guidelines
- ARIA labels
- Keyboard navigation
- Screen reader support
- Color contrast compliance

## Browser Support
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
