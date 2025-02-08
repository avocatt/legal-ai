# Domain Layer

This directory contains the core business logic and domain models of the application.

## Structure

```
domain/
├── models/          # Domain models and entities
├── services/        # Domain services
├── repositories/    # Repository interfaces
└── exceptions/      # Domain-specific exceptions
```

## Guidelines

1. **Domain Models**

   - Should be independent of infrastructure
   - Use value objects where appropriate
   - Implement rich domain models
   - Include validation logic

2. **Domain Services**

   - Handle complex business operations
   - Coordinate between multiple entities
   - Implement business rules
   - Remain persistence-agnostic

3. **Best Practices**
   - Follow DDD principles
   - Use type hints
   - Write comprehensive tests
   - Document business rules
