// This is a placeholder function that will be implemented properly
// when we set up the actual authentication integration
export async function getJWTToken(): Promise<string> {
  // In a real implementation, this would fetch the JWT token from the backend
  // For now, we'll return a mock token for development
  const mockToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
  return mockToken
}