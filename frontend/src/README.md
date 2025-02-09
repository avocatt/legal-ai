# Frontend Architecture

This directory contains the frontend application source code.

## Directory Structure

```
src/
├── components/      # React components
│   ├── common/     # Shared components
│   ├── layout/     # Layout components
│   └── forms/      # Form components
├── hooks/          # Custom React hooks
├── services/       # API and external services
├── store/          # State management
├── utils/          # Utility functions
├── i18n/           # Internationalization
└── types/          # TypeScript type definitions
```

## Guidelines

1. **Components**

   - Use functional components
   - Implement proper prop types
   - Keep components focused
   - Write unit tests

2. **State Management**

   - Use React Query for server state
   - Use Zustand for client state
   - Keep state minimal
   - Document state shape

3. **Code Organization**

   - Follow component-driven development
   - Use TypeScript
   - Document public APIs
   - Write comprehensive tests

4. **Best Practices**
   - Follow React best practices
   - Use proper error boundaries
   - Implement proper loading states
   - Handle edge cases
