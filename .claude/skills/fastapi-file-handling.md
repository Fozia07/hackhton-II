# FastAPI File Handling

## Expertise
Expert skill for handling file operations in FastAPI applications. Specializes in file uploads, downloads, streaming, validation, storage strategies (local, S3, cloud), image processing, and secure file handling for production environments.

## Purpose
This skill handles file operations, enabling you to:
- Accept file uploads with validation
- Stream large files efficiently
- Download files with proper headers
- Store files locally or in cloud storage (S3, GCS, Azure)
- Process images (resize, compress, format conversion)
- Handle CSV, Excel, and PDF files
- Implement secure file access controls
- Manage file metadata and organization
- Handle multipart form data

## When to Use
Use this skill when you need to:
- Accept file uploads from users
- Serve files for download
- Stream large files without memory issues
- Process uploaded images or documents
- Generate and serve PDFs or reports
- Import/export data via CSV or Excel
- Store files in cloud storage
- Implement file access controls
- Handle profile pictures or attachments

## Core Concepts

### 1. File Uploads

**Basic File Upload**:
```python
from fastapi import FastAPI, File, UploadFile
from typing import List

app = FastAPI()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a single file.

    UploadFile provides:
    - filename: Original filename
    - content_type: MIME type
    - file: SpooledTemporaryFile object
    """
    contents = await file.read()

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(contents)
    }
```

**Multiple File Upload**:
```python
@app.post("/upload-multiple/")
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    """Upload multiple files."""
    results = []

    for file in files:
        contents = await file.read()
        results.append({
            "filename": file.filename,
            "size": len(contents)
        })

    return {"files": results}
```

**File Upload with Form Data**:
```python
from fastapi import Form

@app.post("/upload-with-metadata/")
async def upload_with_metadata(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: str = Form(None)
):
    """Upload file with additional metadata."""
    contents = await file.read()

    return {
        "filename": file.filename,
        "title": title,
        "description": description,
        "size": len(contents)
    }
```

**File Upload with Validation**:
```python
from fastapi import HTTPException
import magic  # python-magic for MIME type detection

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".pdf"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

async def validate_file(file: UploadFile) -> None:
    """
    Validate uploaded file.

    Checks:
    - File extension
    - File size
    - MIME type
    """
    # Check extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {ALLOWED_EXTENSIONS}"
        )

    # Check file size
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {MAX_FILE_SIZE / 1024 / 1024} MB"
        )

    # Reset file pointer
    await file.seek(0)

    # Verify MIME type (optional, requires python-magic)
    mime = magic.from_buffer(contents, mime=True)
    allowed_mimes = {"image/jpeg", "image/png", "image/gif", "application/pdf"}
    if mime not in allowed_mimes:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Detected: {mime}"
        )

    # Reset file pointer again
    await file.seek(0)

@app.post("/upload-validated/")
async def upload_validated_file(file: UploadFile = File(...)):
    """Upload file with validation."""
    await validate_file(file)

    # Save file
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        contents = await file.read()
        f.write(contents)

    return {"filename": file.filename, "path": file_path}
```

### 2. File Storage

**Local File Storage**:
```python
import os
import uuid
from pathlib import Path

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

async def save_file_locally(file: UploadFile) -> str:
    """
    Save file to local storage with unique filename.

    Returns:
        File path
    """
    # Generate unique filename
    file_ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = UPLOAD_DIR / unique_filename

    # Save file
    with open(file_path, "wb") as f:
        contents = await file.read()
        f.write(contents)

    return str(file_path)

@app.post("/upload-local/")
async def upload_to_local(file: UploadFile = File(...)):
    """Upload file to local storage."""
    file_path = await save_file_locally(file)

    return {
        "filename": file.filename,
        "path": file_path,
        "url": f"/files/{os.path.basename(file_path)}"
    }
```

**AWS S3 Storage**:
```python
import boto3
from botocore.exceptions import ClientError
from core.config import get_settings

settings = get_settings()

s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
    region_name=settings.aws_region
)

async def upload_to_s3(
    file: UploadFile,
    bucket: str,
    key: str = None
) -> str:
    """
    Upload file to AWS S3.

    Args:
        file: File to upload
        bucket: S3 bucket name
        key: S3 object key (optional, generates if not provided)

    Returns:
        S3 URL
    """
    if key is None:
        file_ext = os.path.splitext(file.filename)[1]
        key = f"{uuid.uuid4()}{file_ext}"

    try:
        # Upload file
        contents = await file.read()
        s3_client.put_object(
            Bucket=bucket,
            Key=key,
            Body=contents,
            ContentType=file.content_type
        )

        # Generate URL
        url = f"https://{bucket}.s3.{settings.aws_region}.amazonaws.com/{key}"
        return url

    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"S3 upload failed: {e}")

@app.post("/upload-s3/")
async def upload_to_s3_endpoint(file: UploadFile = File(...)):
    """Upload file to S3."""
    url = await upload_to_s3(
        file,
        bucket=settings.s3_bucket,
        key=f"uploads/{uuid.uuid4()}{os.path.splitext(file.filename)[1]}"
    )

    return {
        "filename": file.filename,
        "url": url
    }
```

**Presigned URL for Direct S3 Upload**:
```python
@app.post("/upload-url/")
async def generate_upload_url(
    filename: str,
    content_type: str
):
    """
    Generate presigned URL for direct S3 upload.
    Client uploads directly to S3 using this URL.
    """
    key = f"uploads/{uuid.uuid4()}{os.path.splitext(filename)[1]}"

    try:
        presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': settings.s3_bucket,
                'Key': key,
                'ContentType': content_type
            },
            ExpiresIn=3600  # 1 hour
        )

        return {
            "upload_url": presigned_url,
            "key": key,
            "expires_in": 3600
        }

    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate URL: {e}")
```

### 3. File Downloads

**Basic File Download**:
```python
from fastapi.responses import FileResponse

@app.get("/download/{filename}")
async def download_file(filename: str):
    """Download file from local storage."""
    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream"
    )
```

**Download with Custom Headers**:
```python
from fastapi import Response

@app.get("/download-custom/{filename}")
async def download_with_headers(filename: str):
    """Download file with custom headers."""
    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
            "Cache-Control": "no-cache"
        }
    )
```

**Streaming Large Files**:
```python
from fastapi.responses import StreamingResponse
import aiofiles

async def file_iterator(file_path: str, chunk_size: int = 8192):
    """
    Async generator to stream file in chunks.
    Efficient for large files.
    """
    async with aiofiles.open(file_path, 'rb') as f:
        while chunk := await f.read(chunk_size):
            yield chunk

@app.get("/stream/{filename}")
async def stream_file(filename: str):
    """Stream large file efficiently."""
    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return StreamingResponse(
        file_iterator(str(file_path)),
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )
```

**Download from S3**:
```python
@app.get("/download-s3/{key:path}")
async def download_from_s3(key: str):
    """Download file from S3."""
    try:
        # Get object from S3
        response = s3_client.get_object(
            Bucket=settings.s3_bucket,
            Key=key
        )

        # Stream response
        return StreamingResponse(
            response['Body'],
            media_type=response['ContentType'],
            headers={
                "Content-Disposition": f"attachment; filename={os.path.basename(key)}"
            }
        )

    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            raise HTTPException(status_code=404, detail="File not found")
        raise HTTPException(status_code=500, detail=f"S3 download failed: {e}")
```

### 4. Image Processing

**Image Upload with Resizing**:
```python
from PIL import Image
import io

async def process_image(
    file: UploadFile,
    max_width: int = 1920,
    max_height: int = 1080,
    quality: int = 85
) -> bytes:
    """
    Process and resize image.

    Args:
        file: Uploaded image file
        max_width: Maximum width
        max_height: Maximum height
        quality: JPEG quality (1-100)

    Returns:
        Processed image bytes
    """
    # Read image
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))

    # Convert RGBA to RGB if necessary
    if image.mode == 'RGBA':
        image = image.convert('RGB')

    # Resize if needed
    if image.width > max_width or image.height > max_height:
        image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

    # Save to bytes
    output = io.BytesIO()
    image.save(output, format='JPEG', quality=quality, optimize=True)
    output.seek(0)

    return output.getvalue()

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    """Upload and process image."""
    # Validate image
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")

    # Process image
    processed_image = await process_image(file)

    # Save processed image
    filename = f"{uuid.uuid4()}.jpg"
    file_path = UPLOAD_DIR / filename

    with open(file_path, "wb") as f:
        f.write(processed_image)

    return {
        "filename": filename,
        "size": len(processed_image),
        "url": f"/files/{filename}"
    }
```

**Generate Thumbnails**:
```python
async def create_thumbnail(
    image_path: str,
    thumbnail_size: tuple = (200, 200)
) -> str:
    """
    Create thumbnail from image.

    Args:
        image_path: Path to original image
        thumbnail_size: Thumbnail dimensions

    Returns:
        Thumbnail path
    """
    image = Image.open(image_path)
    image.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)

    # Generate thumbnail filename
    base, ext = os.path.splitext(image_path)
    thumbnail_path = f"{base}_thumb{ext}"

    image.save(thumbnail_path, quality=85, optimize=True)
    return thumbnail_path

@app.post("/upload-with-thumbnail/")
async def upload_with_thumbnail(file: UploadFile = File(...)):
    """Upload image and generate thumbnail."""
    # Save original
    file_path = await save_file_locally(file)

    # Create thumbnail
    thumbnail_path = await create_thumbnail(file_path)

    return {
        "original": f"/files/{os.path.basename(file_path)}",
        "thumbnail": f"/files/{os.path.basename(thumbnail_path)}"
    }
```

### 5. CSV and Excel Handling

**CSV Upload and Processing**:
```python
import csv
import io

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    """Upload and process CSV file."""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be CSV")

    # Read CSV
    contents = await file.read()
    csv_data = contents.decode('utf-8')

    # Parse CSV
    reader = csv.DictReader(io.StringIO(csv_data))
    rows = list(reader)

    return {
        "filename": file.filename,
        "rows": len(rows),
        "columns": list(rows[0].keys()) if rows else [],
        "sample": rows[:5]  # First 5 rows
    }
```

**Excel Upload with pandas**:
```python
import pandas as pd

@app.post("/upload-excel/")
async def upload_excel(file: UploadFile = File(...)):
    """Upload and process Excel file."""
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="File must be Excel")

    # Read Excel
    contents = await file.read()
    df = pd.read_excel(io.BytesIO(contents))

    return {
        "filename": file.filename,
        "rows": len(df),
        "columns": df.columns.tolist(),
        "sample": df.head().to_dict('records')
    }
```

**CSV Export**:
```python
from fastapi.responses import StreamingResponse

@app.get("/export-csv/")
async def export_csv(db: Session = Depends(get_db)):
    """Export data to CSV."""
    # Get data
    users = db.execute(select(User)).scalars().all()

    # Create CSV
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=['id', 'email', 'username'])
    writer.writeheader()

    for user in users:
        writer.writerow({
            'id': user.id,
            'email': user.email,
            'username': user.username
        })

    output.seek(0)

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=users.csv"
        }
    )
```

**Excel Export with pandas**:
```python
@app.get("/export-excel/")
async def export_excel(db: Session = Depends(get_db)):
    """Export data to Excel."""
    # Get data
    users = db.execute(select(User)).scalars().all()

    # Create DataFrame
    data = [{
        'ID': user.id,
        'Email': user.email,
        'Username': user.username
    } for user in users]
    df = pd.DataFrame(data)

    # Create Excel file
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Users')

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=users.xlsx"
        }
    )
```

### 6. PDF Generation

**Generate PDF with ReportLab**:
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

@app.get("/generate-pdf/")
async def generate_pdf(title: str, content: str):
    """Generate PDF document."""
    # Create PDF
    output = io.BytesIO()
    c = canvas.Canvas(output, pagesize=letter)

    # Add content
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, title)

    c.setFont("Helvetica", 12)
    c.drawString(100, 700, content)

    c.save()
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=document.pdf"
        }
    )
```

**HTML to PDF with WeasyPrint**:
```python
from weasyprint import HTML

@app.post("/html-to-pdf/")
async def html_to_pdf(html_content: str):
    """Convert HTML to PDF."""
    # Generate PDF from HTML
    pdf_bytes = HTML(string=html_content).write_pdf()

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=document.pdf"
        }
    )
```

### 7. File Access Control

**Secure File Access with Authentication**:
```python
from core.dependencies import get_current_user

@app.get("/secure-files/{filename}")
async def get_secure_file(
    filename: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Download file with authentication.
    Only file owner can download.
    """
    # Get file metadata
    file_record = db.execute(
        select(FileMetadata).where(FileMetadata.filename == filename)
    ).scalar_one_or_none()

    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")

    # Check ownership
    if file_record.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    # Serve file
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found on disk")

    return FileResponse(path=file_path, filename=filename)
```

**Temporary Download Links**:
```python
from datetime import datetime, timedelta
import jwt

def generate_download_token(
    filename: str,
    expires_in: int = 3600
) -> str:
    """
    Generate temporary download token.

    Args:
        filename: File to download
        expires_in: Token expiration in seconds

    Returns:
        JWT token
    """
    payload = {
        "filename": filename,
        "exp": datetime.utcnow() + timedelta(seconds=expires_in)
    }
    token = jwt.encode(payload, settings.secret_key, algorithm="HS256")
    return token

@app.get("/download-link/{filename}")
async def get_download_link(
    filename: str,
    current_user: User = Depends(get_current_user)
):
    """Generate temporary download link."""
    token = generate_download_token(filename)

    return {
        "download_url": f"/download-with-token?token={token}",
        "expires_in": 3600
    }

@app.get("/download-with-token")
async def download_with_token(token: str):
    """Download file using temporary token."""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        filename = payload["filename"]

        file_path = UPLOAD_DIR / filename
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")

        return FileResponse(path=file_path, filename=filename)

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Download link expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid download link")
```

### 8. File Metadata Management

**File Metadata Model**:
```python
from sqlmodel import SQLModel, Field
from datetime import datetime

class FileMetadata(SQLModel, table=True):
    """File metadata stored in database."""
    id: int = Field(default=None, primary_key=True)
    filename: str = Field(index=True)
    original_filename: str
    content_type: str
    size: int
    storage_path: str
    user_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Optional fields
    description: str = None
    tags: str = None  # JSON string of tags
    is_public: bool = False
```

**Upload with Metadata**:
```python
@app.post("/upload-with-db/")
async def upload_with_database(
    file: UploadFile = File(...),
    description: str = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload file and store metadata in database."""
    # Save file
    file_path = await save_file_locally(file)

    # Create metadata record
    file_metadata = FileMetadata(
        filename=os.path.basename(file_path),
        original_filename=file.filename,
        content_type=file.content_type,
        size=os.path.getsize(file_path),
        storage_path=file_path,
        user_id=current_user.id,
        description=description
    )

    db.add(file_metadata)
    db.commit()
    db.refresh(file_metadata)

    return {
        "id": file_metadata.id,
        "filename": file_metadata.filename,
        "url": f"/files/{file_metadata.filename}"
    }
```

## Best Practices

### 1. File Validation
- Always validate file types and sizes
- Use MIME type detection, not just extensions
- Set reasonable file size limits
- Sanitize filenames to prevent path traversal
- Validate file content, not just headers

### 2. Storage Strategy
- Use unique filenames (UUID) to prevent collisions
- Organize files in directories (by date, user, type)
- Use cloud storage (S3) for production
- Implement file cleanup for temporary files
- Consider CDN for public files

### 3. Security
- Authenticate file access when needed
- Implement access controls (ownership, permissions)
- Use presigned URLs for direct uploads
- Scan uploaded files for malware
- Never trust user-provided filenames

### 4. Performance
- Stream large files instead of loading into memory
- Use async file operations (aiofiles)
- Implement caching for frequently accessed files
- Use background tasks for file processing
- Consider chunked uploads for large files

### 5. Error Handling
- Handle file not found errors
- Catch storage errors (disk full, S3 errors)
- Validate file integrity after upload
- Implement retry logic for cloud uploads
- Log all file operations

## Summary

This skill provides comprehensive guidance for file handling in FastAPI applications with:
- File uploads with validation
- Multiple storage strategies (local, S3, presigned URLs)
- File downloads and streaming
- Image processing and thumbnails
- CSV and Excel handling
- PDF generation
- Secure file access controls
- File metadata management
- Best practices for security and performance

Use this skill to implement robust file handling capabilities in your FastAPI applications with proper validation, storage, and access controls for production environments.
