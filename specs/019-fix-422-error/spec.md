# Specification: Fix 422 Error When Toggling Todo Completion

## Feature Description
Resolve the persistent 422 (Unprocessable Content) error that occurs when users click the checkbox to mark a todo as complete/incomplete. The error manifests as "Error: [object Object]" in the browser and shows red indicators in the IDE for the TodoItem.tsx component.

## Problem Statement
When a user attempts to toggle the completion status of a todo item by clicking the checkbox, the following issues occur:
- Browser displays "Error: [object Object]"
- Network tab shows 422 (Unprocessable Content) error for PUT requests to `/todos/{id}`
- IDE shows red error indicators in TodoItem.tsx component
- The todo completion status does not update properly

## User Scenarios & Testing
### Primary Scenario
1. User is authenticated and on the dashboard page
2. User sees a list of todos with checkboxes
3. User clicks the checkbox next to a todo to mark it as complete/incomplete
4. The checkbox should visually update and the todo's completion status should be saved to the backend
5. The UI should reflect the change without errors

### Error Scenario
1. User clicks the checkbox next to a todo
2. Browser displays "Error: [object Object]"
3. Network request to update todo returns 422 status
4. Todo completion status is not updated

## Functional Requirements
1. **Checkbox Toggle Functionality**: The checkbox should properly toggle the todo's completion status when clicked
2. **Backend Communication**: PUT requests to update todo completion should succeed with 200 status
3. **Error Handling**: Proper error messages should be displayed to the user instead of "[object Object]"
4. **State Synchronization**: The frontend state should properly reflect the updated completion status
5. **Validation Compatibility**: The update request should pass backend validation without 422 errors

## Non-Functional Requirements
1. **Response Time**: Todo completion updates should complete within 2 seconds
2. **User Experience**: The checkbox should provide immediate visual feedback
3. **Data Consistency**: The todo's completion status should be consistent between frontend and backend

## Success Criteria
- Users can successfully toggle todo completion status without errors
- PUT requests to `/todos/{id}` return 200 status when updating completion
- No 422 errors occur during completion toggling
- Error messages are properly formatted instead of showing "[object Object]"
- Todo items visually update immediately upon completion toggle

## Key Entities
- TodoItem component (frontend)
- TodoContext and TodoProvider (frontend state management)
- TodoService updateTodo method (frontend API calls)
- Backend todo update endpoint (PUT /todos/{id})
- TodoUpdate model validation (backend)

## Assumptions
- The backend is running and accessible at the configured API URL
- User is properly authenticated with valid JWT token
- The TodoItem component is properly integrated with TodoContext
- Other todo operations (create, delete) are working correctly

## Dependencies
- Authentication system for proper JWT token handling
- Backend API endpoints for todo operations
- TodoContext for state management