"""Session-oriented HTTP API for anonymous, temporary statement analysis."""

from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from api.dependencies import get_session_manager
from application.errors.application_error import ApplicationError
from application.sessions.session_status import SessionStatus
from application.workflows.analyze_statement import AnalyzeStatementWorkflow
from application.workflows.generate_report import GenerateReportWorkflow
from application.workflows.finalize_session import FinalizeSessionWorkflow

router = APIRouter(prefix="/sessions", tags=["sessions"])
MAX_UPLOAD_BYTES = 10 * 1024 * 1024


@router.post("")
def create_session(manager=Depends(get_session_manager)):
    session = manager.create()
    return _session_dto(session)


@router.post("/{session_id}/preview")
async def preview(session_id: str, file: UploadFile = File(...), manager=Depends(get_session_manager)):
    try:
        session = manager.get(session_id)
        content, filename = await _read_upload(file)
        return session.container.statement_service.preview_statement(content, filename)
    except ApplicationError as error:
        _error(error)


@router.post("/{session_id}/analyze")
async def analyze(session_id: str, file: UploadFile = File(...), manager=Depends(get_session_manager)):
    try:
        session = manager.get(session_id)
        content, filename = await _read_upload(file)
        return AnalyzeStatementWorkflow().analyze(session, content, filename)
    except ApplicationError as error:
        _error(error)
    except ValueError as error:
        raise HTTPException(status_code=422, detail="Analysis input is invalid.") from error


@router.get("/{session_id}/status")
def status(session_id: str, manager=Depends(get_session_manager)):
    try: return _session_dto(manager.get(session_id))
    except ApplicationError as error: _error(error)


@router.get("/{session_id}/analysis")
def analysis(session_id: str, manager=Depends(get_session_manager)):
    try:
        session = manager.get(session_id)
        if session.status not in (SessionStatus.ANALYZED, SessionStatus.REPORT_READY, SessionStatus.FINALIZING):
            raise HTTPException(status_code=409, detail="Analysis is not ready.")
        return session.analysis_result
    except ApplicationError as error: _error(error)


@router.get("/{session_id}/presentation/dashboard")
def presentation_dashboard(session_id: str, manager=Depends(get_session_manager)):
    try:
        session = manager.get(session_id)
        return session.container.presentation_service.dashboard(session)
    except ApplicationError as error: _error(error)


@router.get("/{session_id}/presentation/transactions")
def presentation_transactions(session_id: str, manager=Depends(get_session_manager)):
    try:
        session = manager.get(session_id)
        return session.container.presentation_service.transactions(session)
    except ApplicationError as error: _error(error)


@router.get("/{session_id}/presentation/insights")
def presentation_insights(session_id: str, manager=Depends(get_session_manager)):
    try:
        session = manager.get(session_id)
        return session.container.presentation_service.insights(session)
    except ApplicationError as error: _error(error)


@router.get("/{session_id}/presentation/explanations/{root_id}")
def presentation_explanation(session_id: str, root_id: str, manager=Depends(get_session_manager)):
    try:
        session = manager.get(session_id)
        return session.container.presentation_service.explanation(session, root_id)
    except ApplicationError as error: _error(error)


@router.get("/{session_id}/report")
def report(session_id: str, manager=Depends(get_session_manager)):
    try:
        session = manager.get(session_id)
        path = GenerateReportWorkflow().generate(session)
        return {"report_ready": True, "expires_at": session.expires_at, "filename": path.name}
    except ApplicationError as error: _error(error)
    except ValueError as error: raise HTTPException(status_code=409, detail=str(error)) from error


@router.get("/{session_id}/report.pdf")
def download_report(session_id: str, manager=Depends(get_session_manager)):
    try:
        session = manager.get(session_id)
        if session.report_path is None or not session.report_path.exists():
            GenerateReportWorkflow().generate(session)
        FinalizeSessionWorkflow(manager).finalize(session_id)
        return FileResponse(session.report_path, media_type="application/pdf", filename="smartspend-financial-overview.pdf")
    except ApplicationError as error: _error(error)


@router.delete("/{session_id}")
def delete_session(session_id: str, manager=Depends(get_session_manager)):
    manager.cleanup(session_id)
    return {"deleted": True}


async def _read_upload(file: UploadFile) -> tuple[bytes, str]:
    filename = Path(file.filename or "").name
    if not filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported in this session API.")
    content = await file.read(MAX_UPLOAD_BYTES + 1)
    if not content: raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    if len(content) > MAX_UPLOAD_BYTES: raise HTTPException(status_code=413, detail="Uploaded file exceeds the 10 MB limit.")
    return content, filename


def _session_dto(session) -> dict:
    return {"session_id": session.session_id, "status": session.status.value, "created_at": session.created_at, "expires_at": session.expires_at, "warnings": tuple(session.warnings), "error": session.error}


def _error(error: ApplicationError):
    raise HTTPException(status_code=error.status_code, detail={"code": error.code, "message": str(error)})
