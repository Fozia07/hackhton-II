# Data Model: Database Integration with Neon PostgreSQL using SQLModel

## Entity: User

### Attributes
- **id** (Integer)
  - Type: Integer
  - Constraints: Primary Key, Auto-increment
  - Required: Yes
  - Description: Unique identifier for the user

- **username** (String)
  - Type: String(150)
  - Constraints: Unique, Not Null
  - Required: Yes
  - Description: Unique username for the user account

- **email** (String)
  - Type: String(255)
  - Constraints: Unique, Not Null
  - Required: Yes
  - Description: Email address associated with the user account

- **hashed_password** (String)
  - Type: String(255)
  - Constraints: Not Null
  - Required: Yes
  - Description: Hashed password for authentication

- **created_at** (DateTime)
  - Type: DateTime
  - Constraints: Default to current timestamp
  - Required: No (auto-generated)
  - Description: Timestamp when the user account was created

- **updated_at** (DateTime)
  - Type: DateTime
  - Constraints: Default to current timestamp, updates on modification
  - Required: No (auto-generated)
  - Description: Timestamp when the user account was last updated

- **is_active** (Boolean)
  - Type: Boolean
  - Constraints: Default to True
  - Required: No (default value)
  - Description: Flag indicating if the user account is active

### Validation Rules
- Username must be between 3 and 150 characters
- Email must follow standard email format
- Email and username must be unique across all users
- Password must be properly hashed before storage

### Relationships
- Potential future relationships with other entities (e.g., user sessions, user preferences)

## Entity: Database Session

### Attributes
- **session** (SQLModel Session)
  - Type: SQLModel Session object
  - Description: Database session instance for database operations

### Lifecycle Management
- Created per request through FastAPI dependency injection
- Automatically closed after request completion
- Managed through FastAPI's dependency system