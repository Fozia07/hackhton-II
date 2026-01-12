# Data Model: JWT-Based User Authentication

## Entity: SignupRequest

### Attributes
- **username** (String)
  - Type: String
  - Constraints: Required, min length 3, max length 150, unique
  - Required: Yes
  - Description: Unique username for the user account

- **email** (String)
  - Type: String
  - Constraints: Required, valid email format, unique
  - Required: Yes
  - Description: Email address associated with the user account

- **password** (String)
  - Type: String
  - Constraints: Required, min length 8, validated for strength
  - Required: Yes
  - Description: Password for the user account (will be hashed)

### Validation Rules
- Username must be between 3 and 150 characters
- Email must follow standard email format
- Password must be at least 8 characters
- Username and email must be unique across all users

## Entity: SigninRequest

### Attributes
- **username** (String)
  - Type: String
  - Constraints: Required, can be username or email
  - Required: Yes
  - Description: Username or email for authentication

- **password** (String)
  - Type: String
  - Constraints: Required
  - Required: Yes
  - Description: Password for authentication

### Validation Rules
- Username/email and password must match existing user
- Credentials must be valid for authentication

## Entity: AuthResponse

### Attributes
- **access_token** (String)
  - Type: String
  - Constraints: Required, JWT format
  - Required: Yes
  - Description: JWT access token for authentication

- **token_type** (String)
  - Type: String
  - Constraints: Required, default "bearer"
  - Required: Yes
  - Description: Type of authentication token

- **user_id** (Integer)
  - Type: Integer
  - Constraints: Required, matches user ID
  - Required: Yes
  - Description: Identifier of the authenticated user

- **username** (String)
  - Type: String
  - Constraints: Required
  - Required: Yes
  - Description: Username of the authenticated user

### Validation Rules
- Token must be properly formatted JWT
- Token must not be expired
- User information must match authenticated user

## Entity: JWT Token

### Attributes
- **sub** (String)
  - Type: String
  - Description: Subject (user identifier) of the token

- **exp** (Integer)
  - Type: Integer
  - Description: Expiration timestamp of the token

- **iat** (Integer)
  - Type: Integer
  - Description: Issued at timestamp of the token

- **user_id** (Integer)
  - Type: Integer
  - Description: User identifier included in the token

### Validation Rules
- Token must have valid signature
- Token must not be expired at time of validation
- Subject must match authenticated user

## Entity: User (Enhanced)

### Additional Attributes for Authentication
- **hashed_password** (String)
  - Type: String
  - Constraints: Required, stored as hash
  - Required: Yes
  - Description: Hashed password for authentication

### Relationships
- Related to authentication sessions (potential future enhancement)
- Related to user permissions (potential future enhancement)