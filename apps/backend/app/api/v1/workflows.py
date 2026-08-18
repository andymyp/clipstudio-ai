"""Workflow monitoring endpoints."""

from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.models import Workflow
from ...dependencies.api import (
    UserContext,
    get_db_session,
    get_user_context,
    get_workflow_manager,
)
from ...repositories.workflows import WorkflowRepository
from ...schemas.api import JobResponse, Page, WorkflowResponse
from ...schemas.common import ApiResponse
from ...services.workflow.manager import (
    WorkflowManager,
    WorkflowNotFoundError,
    WorkflowOperationError,
)

router = APIRouter(prefix="/workflows", tags=["workflows"])


def _response(workflow: Workflow) -> WorkflowResponse:
    """Map workflow state to a public status contract."""
    duration = None
    if workflow.started_at:
        end = workflow.completed_at or datetime.now(UTC)
        duration = max(0.0, (end - workflow.started_at).total_seconds())
    return WorkflowResponse(
        id=workflow.id,
        agent_id=workflow.agent_id,
        current_step=workflow.current_step,
        status=workflow.status,
        progress=workflow.progress,
        started_at=workflow.started_at,
        completed_at=workflow.completed_at,
        created_at=workflow.created_at,
        updated_at=workflow.updated_at,
        errors=list(workflow.errors_json or []),
        duration_seconds=duration,
    )


@router.get("", response_model=ApiResponse[Page[WorkflowResponse]])
async def list_workflows(
    status_filter: str | None = Query(default=None, alias="status"),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_db_session),
    _: UserContext = Depends(get_user_context),
) -> ApiResponse[Page[WorkflowResponse]]:
    """List workflow status records."""
    items = await WorkflowRepository(session).list_filtered(
        status=status_filter, limit=limit, offset=offset
    )
    page = Page(
        items=[_response(item) for item in items],
        limit=limit,
        offset=offset,
        returned=len(items),
    )
    return ApiResponse(success=True, data=page)


@router.get("/{workflow_id}", response_model=ApiResponse[WorkflowResponse])
async def get_workflow(
    workflow_id: str,
    session: AsyncSession = Depends(get_db_session),
    _: UserContext = Depends(get_user_context),
) -> ApiResponse[WorkflowResponse]:
    """Get a workflow status record."""
    workflow = await WorkflowRepository(session).get(workflow_id)
    if workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found.")
    return ApiResponse(success=True, data=_response(workflow))


@router.post("/{workflow_id}/cancel", response_model=ApiResponse[WorkflowResponse])
async def cancel_workflow(
    workflow_id: str,
    session: AsyncSession = Depends(get_db_session),
    manager: WorkflowManager = Depends(get_workflow_manager),
    _: UserContext = Depends(get_user_context),
) -> ApiResponse[WorkflowResponse]:
    """Mark a workflow cancelled; execution is owned by a later engine phase."""
    try:
        workflow = await manager.cancel(workflow_id)
    except WorkflowNotFoundError:
        raise HTTPException(status_code=404, detail="Workflow not found.") from None
    return ApiResponse(success=True, data=_response(workflow))


@router.post("/{workflow_id}/pause", response_model=ApiResponse[WorkflowResponse])
async def pause_workflow(
    workflow_id: str,
    manager: WorkflowManager = Depends(get_workflow_manager),
    _: UserContext = Depends(get_user_context),
) -> ApiResponse[WorkflowResponse]:
    """Pause a queued or running workflow."""
    try:
        workflow = await manager.pause(workflow_id)
    except WorkflowNotFoundError:
        raise HTTPException(status_code=404, detail="Workflow not found.") from None
    except WorkflowOperationError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return ApiResponse(success=True, data=_response(workflow))


@router.post(
    "/{workflow_id}/resume",
    response_model=ApiResponse[JobResponse],
    status_code=202,
)
async def resume_workflow(
    workflow_id: str,
    manager: WorkflowManager = Depends(get_workflow_manager),
    _: UserContext = Depends(get_user_context),
) -> ApiResponse[JobResponse]:
    """Resume a paused workflow through the queue."""
    try:
        job = await manager.resume(workflow_id)
    except WorkflowNotFoundError:
        raise HTTPException(status_code=404, detail="Workflow not found.") from None
    except WorkflowOperationError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return ApiResponse(success=True, data=JobResponse(job_id=job.job_id))
