# Data Model for Frontend Authentication & Build Configuration Error Resolution

## Error Objects

### Fetch API Error
- **Name**: FetchRedirectError
- **Fields**:
  - errorMessage: string (the error message received)
  - invalidProperty: string ("redirect")
  - invalidValue: boolean (false - invalid value provided)
  - validEnumValues: array of strings (["follow", "error", "manual"])
  - affectedEndpoint: string (the endpoint where fetch is called)
  - affectedFlow: string ("signup" - authentication flow affected)

### Build Warning Object
- **Name**: BuildWarning
- **Fields**:
  - warningMessage: string (the warning text)
  - warningType: string ("lockfiles" or "workspace-root")
  - severity: string ("warning")
  - affectedComponent: string ("Next.js" or "Turbopack")
  - suggestedFix: string (recommended solution)

## Authentication Flow Data

### Signup Request
- **Name**: SignupRequest
- **Fields**:
  - userData: object (user information)
  - fetchConfig: object (configuration for fetch API call)
  - redirectPolicy: string (valid redirect enum value)

## Validation Rules
- fetchConfig.redirect must be one of ["follow", "error", "manual"]
- workspace root must be properly configured for Next.js/Turbopack
- package.json and lockfile must be consistent