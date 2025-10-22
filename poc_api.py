"""
POC Agent API endpoints.

This module provides FastAPI endpoints for interacting with the POC Agent,
including document uploads, chat conversations, and POC generation.
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
import os
import shutil
from datetime import datetime

from database import get_db, Document, POC, POCConversation, POCPhase
from agents.poc_agent import POCAgent
from auth import get_current_user, User

router = APIRouter(prefix="/api/poc", tags=["poc"])

# Pydantic models for requests/responses

class ChatRequest(BaseModel):
    prompt: str
    document_ids: Optional[List[int]] = None
    conversation_history: Optional[dict] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    agent_state: dict
    next_action: str

class GenerateRequest(BaseModel):
    requirements: dict

class POCResponse(BaseModel):
    poc_id: str
    poc_name: str
    directory: str
    files: List[str]

# Initialize POC Agent (lazy initialization)
_poc_agent = None

def get_poc_agent():
    """Lazy initialization of POC Agent"""
    global _poc_agent
    if _poc_agent is None:
        _poc_agent = POCAgent()
    return _poc_agent


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload a document (PDF, TXT, MD, PNG, JPG) for POC context.
    
    The document will be stored and processed for RAG.
    """
    # Validate file type
    allowed_types = ["pdf", "txt", "md", "png", "jpg", "jpeg"]
    file_ext = file.filename.split(".")[-1].lower()
    
    if file_ext not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: {', '.join(allowed_types)}"
        )
    
    # Create upload directory
    upload_dir = f"uploads/{current_user.id}"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Save file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(upload_dir, filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Load and process document
    try:
        agent = get_poc_agent()
        docs = agent.load_document(file_path, file_ext)
        agent.create_vector_store(docs, str(current_user.id))
        
        # Extract content for database
        content_text = "\n".join([doc.page_content for doc in docs])
        
    except Exception as e:
        # Clean up file if processing fails
        os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Document processing failed: {str(e)}")
    
    # Save to database
    db_document = Document(
        user_id=current_user.id,
        filename=file.filename,
        file_path=file_path,
        content_text=content_text[:10000],  # Limit to 10k chars
        file_type=file_ext
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    
    return {
        "id": db_document.id,
        "filename": db_document.filename,
        "file_type": db_document.file_type,
        "created_at": db_document.created_at
    }


@router.get("/documents")
def list_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all documents uploaded by current user."""
    documents = db.query(Document).filter(Document.user_id == current_user.id).all()
    
    return [
        {
            "id": doc.id,
            "filename": doc.filename,
            "file_type": doc.file_type,
            "created_at": doc.created_at
        }
        for doc in documents
    ]


@router.delete("/documents/{doc_id}")
def delete_document(
    doc_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a document."""
    document = db.query(Document).filter(
        Document.id == doc_id,
        Document.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Delete file
    if os.path.exists(document.file_path):
        os.remove(document.file_path)
    
    # Delete from database
    db.delete(document)
    db.commit()
    
    return {"message": "Document deleted"}


@router.post("/chat", response_model=ChatResponse)
def chat_with_agent(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Chat with POC Agent.
    
    Processes user message and returns agent response with conversation tracking.
    """
    try:
        agent = get_poc_agent()
        result = agent.process_request(
            prompt=request.prompt,
            user_id=str(current_user.id),
            document_ids=request.document_ids,
            conversation_history=request.conversation_history
        )
        
        # Update requirements from conversation after each message
        agent.update_requirements_from_conversation()
        
        # Save conversation to database
        if agent.conversation_id:
            # Check if conversation exists
            conv = db.query(POCConversation).filter(
                POCConversation.user_id == current_user.id
            ).order_by(POCConversation.created_at.desc()).first()
            
            if not conv:
                # Create new conversation
                conv = POCConversation(
                    user_id=current_user.id,
                    conversation_history=agent.save_conversation()
                )
                db.add(conv)
            else:
                # Update existing conversation
                conv.conversation_history = agent.save_conversation()
            
            db.commit()
        
        return ChatResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")


@router.post("/generate", response_model=POCResponse)
def generate_poc(
    request: GenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate POC structure with all documentation files.
    
    Creates directory structure and markdown files for implementation.
    """
    try:
        agent = get_poc_agent()
        result = agent.generate_poc(
            requirements=request.requirements,
            user_id=str(current_user.id)
        )
        
        # Save to database
        db_poc = POC(
            user_id=current_user.id,
            poc_id=result["poc_id"],
            poc_name=result["poc_name"],
            description=request.requirements.get("goal", ""),
            requirements=request.requirements,
            directory=result["directory"]
        )
        db.add(db_poc)
        db.commit()
        db.refresh(db_poc)
        
        # Create phase records
        phases = [
            ("phase_1_frontend", "Frontend"),
            ("phase_2_backend", "Backend"),
            ("phase_3_database", "Database")
        ]
        
        for i, (file_key, name) in enumerate(phases, 1):
            db_phase = POCPhase(
                poc_id=db_poc.id,
                phase_number=i,
                phase_name=name,
                instructions_file=os.path.join(result["directory"], f"{file_key}.md"),
                status="pending"
            )
            db.add(db_phase)
        
        db.commit()
        
        return POCResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"POC generation failed: {str(e)}")


class PRDResponse(BaseModel):
    prd_name: str
    file_path: str
    feature_name: str
    description: str


@router.post("/generate-prd", response_model=PRDResponse)
def generate_prd(
    request: GenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate PRD markdown file for Cursor implementation.
    
    Saves to /prd/ folder with comprehensive implementation instructions.
    """
    try:
        agent = get_poc_agent()
        
        # Use provided requirements or extract from agent state
        requirements = request.requirements
        if not requirements or not requirements.get("goal"):
            # Try to extract from agent's current state
            requirements = agent.requirements if hasattr(agent, 'requirements') and agent.requirements else request.requirements
        
        # If still no requirements, try extracting from latest conversation
        if not requirements or not requirements.get("goal"):
            # Get latest conversation for this user
            latest_conv = db.query(POCConversation).filter(
                POCConversation.user_id == current_user.id
            ).order_by(POCConversation.created_at.desc()).first()
            
            if latest_conv and latest_conv.conversation_history:
                # Try to extract from stored conversation
                conv_data = latest_conv.conversation_history
                if isinstance(conv_data, dict) and conv_data.get("requirements"):
                    requirements = conv_data["requirements"]
        
        # Ensure we have at least basic requirements
        if not requirements or not requirements.get("goal"):
            raise HTTPException(
                status_code=400,
                detail="Requirements not complete. Please have a conversation about what you want to build first."
            )
        
        result = agent.generate_prd(
            requirements=requirements,
            user_id=str(current_user.id)
        )
        
        # Save conversation with PRD reference
        if hasattr(agent, 'conversation_id') and agent.conversation_id:
            conv = db.query(POCConversation).filter(
                POCConversation.user_id == current_user.id
            ).order_by(POCConversation.created_at.desc()).first()
            
            if not conv:
                conv = POCConversation(
                    user_id=current_user.id,
                    conversation_history=agent.save_conversation()
                )
                db.add(conv)
            else:
                conv.conversation_history = agent.save_conversation()
            
            db.commit()
        
        return PRDResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PRD generation failed: {str(e)}")


@router.get("/list-prds")
def list_prds():
    """List all PRD files in /prd/ folder."""
    prd_dir = "prd"
    
    if not os.path.exists(prd_dir):
        return []
    
    prds = []
    for filename in os.listdir(prd_dir):
        if filename.endswith("-prd.md"):
            file_path = os.path.join(prd_dir, filename)
            stat = os.stat(file_path)
            
            # Extract feature name from filename (format: feature_name-timestamp-prd.md)
            feature_name = filename.replace("-prd.md", "").rsplit("-", 1)[0]
            
            prds.append({
                "prd_name": filename,
                "file_path": file_path,
                "feature_name": feature_name,
                "created_at": datetime.fromtimestamp(stat.st_mtime).isoformat()
            })
    
    # Sort by creation time (newest first)
    prds.sort(key=lambda x: x["created_at"], reverse=True)
    
    return prds


@router.get("/prd/{prd_name}")
def get_prd_content(prd_name: str):
    """Get PRD file content."""
    prd_path = os.path.join("prd", prd_name)
    
    if not os.path.exists(prd_path):
        raise HTTPException(status_code=404, detail="PRD not found")
    
    try:
        with open(prd_path, "r") as f:
            content = f.read()
        
        return {
            "prd_name": prd_name,
            "content": content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read PRD: {str(e)}")


@router.get("/list")
def list_pocs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all POCs created by current user."""
    pocs = db.query(POC).filter(POC.user_id == current_user.id).all()
    
    return [
        {
            "id": poc.id,
            "poc_id": poc.poc_id,
            "poc_name": poc.poc_name,
            "description": poc.description,
            "created_at": poc.created_at
        }
        for poc in pocs
    ]


@router.get("/{poc_id}/files")
def get_poc_files(
    poc_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get file tree for a POC."""
    poc = db.query(POC).filter(
        POC.poc_id == poc_id,
        POC.user_id == current_user.id
    ).first()
    
    if not poc:
        raise HTTPException(status_code=404, detail="POC not found")
    
    # Get all files in POC directory
    files = []
    poc_dir = poc.directory
    
    if os.path.exists(poc_dir):
        for root, dirs, filenames in os.walk(poc_dir):
            for filename in filenames:
                full_path = os.path.join(root, filename)
                rel_path = os.path.relpath(full_path, poc_dir)
                files.append(rel_path)
    
    return {
        "poc_id": poc.poc_id,
        "directory": poc.directory,
        "files": files
    }


@router.get("/{poc_id}/download")
def download_poc(
    poc_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Download POC as ZIP file."""
    poc = db.query(POC).filter(
        POC.poc_id == poc_id,
        POC.user_id == current_user.id
    ).first()
    
    if not poc:
        raise HTTPException(status_code=404, detail="POC not found")
    
    # Create ZIP file
    import zipfile
    zip_filename = f"{poc.poc_id}.zip"
    zip_path = f"/tmp/{zip_filename}"
    
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(poc.directory):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, os.path.dirname(poc.directory))
                zipf.write(file_path, arcname)
    
    return FileResponse(
        zip_path,
        media_type="application/zip",
        filename=zip_filename
    )


@router.put("/{poc_id}/update")
def update_poc(
    poc_id: str,
    request: GenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update POC requirements and regenerate phase files."""
    poc = db.query(POC).filter(
        POC.poc_id == poc_id,
        POC.user_id == current_user.id
    ).first()
    
    if not poc:
        raise HTTPException(status_code=404, detail="POC not found")
    
    # Update requirements
    poc.requirements = request.requirements
    poc.description = request.requirements.get("goal", poc.description)
    
    # Regenerate phase files
    try:
        agent = get_poc_agent()
        result = agent.generate_poc(
            requirements=request.requirements,
            user_id=str(current_user.id)
        )
        
        db.commit()
        
        return {"message": "POC updated", "directory": result["directory"]}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"POC update failed: {str(e)}")

