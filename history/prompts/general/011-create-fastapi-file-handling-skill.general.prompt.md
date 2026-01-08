---
id: 011
title: Create FastAPI File Handling Skill
stage: general
date: 2026-01-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: Fozia
command: skill creation
labels: ["fastapi", "file-handling", "skill-creation", "uploads", "downloads", "s3", "image-processing"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .claude/skills/fastapi-file-handling.md
tests:
  - none (documentation work)
---

## Prompt

Continue (implicit: continue building FastAPI skills ecosystem)

## Response snapshot

Created comprehensive FastAPI File Handling skill documentation (27K) at `.claude/skills/fastapi-file-handling.md`.

The skill covers:

**1. File Uploads**
- Basic single file upload with UploadFile
- Multiple file uploads
- File upload with form data (metadata)
- File upload with validation (extension, size, MIME type)

**2. File Storage**
- Local file storage with unique filenames (UUID)
- AWS S3 storage with boto3
- Presigned URLs for direct S3 uploads (client-side)
- Storage strategy patterns

**3. File Downloads**
- Basic file download with FileResponse
- Download with custom headers
- Streaming large files efficiently with async generators
- Download from S3 with streaming

**4. Image Processing**
- Image upload with resizing using PIL/Pillow
- Thumbnail generation
- Image format conversion and optimization
- Quality and compression settings

**5. CSV and Excel Handling**
- CSV upload and processing with csv module
- Excel upload with pandas
- CSV export with streaming
- Excel export with openpyxl

**6. PDF Generation**
- PDF generation with ReportLab
- HTML to PDF conversion with WeasyPrint
- Dynamic PDF content

**7. File Access Control**
- Secure file access with authentication
- Ownership verification
- Temporary download links with JWT tokens
- Token expiration and validation

**8. File Metadata Management**
- FileMetadata SQLModel for database storage
- Upload with metadata tracking
- File organization and tagging
- Public/private file flags

**Best Practices**:
- File validation (types, sizes, MIME detection, sanitization)
- Storage strategy (unique filenames, organization, cloud storage, cleanup, CDN)
- Security (authentication, access controls, presigned URLs, malware scanning, filename sanitization)
- Performance (streaming, async operations, caching, background processing, chunked uploads)
- Error handling (not found, storage errors, integrity validation, retry logic, logging)

The skill completes the file operations layer for FastAPI applications, enabling secure file uploads, downloads, processing, and storage.

## Outcome

- ✅ Impact: Created production-ready FastAPI file handling skill with comprehensive patterns for uploads, downloads, storage (local/S3), image processing, CSV/Excel/PDF handling, and secure access controls
- 🧪 Tests: No tests required (documentation work)
- 📁 Files: Created .claude/skills/fastapi-file-handling.md (27K)
- 🔁 Next prompts: User may request additional FastAPI skills (WebSockets, caching, rate limiting, middleware, GraphQL) or begin implementing a FastAPI application with full file handling capabilities
- 🧠 Reflection: This skill adds critical file operations capabilities to the FastAPI ecosystem. Combined with existing skills (routing, validation, security, configuration, testing, database, migrations, background tasks), developers can now build APIs that handle file uploads, downloads, processing, and storage with proper validation, security, and performance optimization for production environments.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A (documentation work)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
