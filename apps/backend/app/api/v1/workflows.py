"""Workflow monitoring endpoints."""

from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.models import Workflow
from ...dependencies.api import UserContext, get_db_session, get_user_context
from ...repositories.workflows import WorkflowRepository
from ...schemas.api import Page, WorkflowResponse
from ...schemas.common import ApiResponse

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
    _: UserContext = Depends(get_user_context),
) -> ApiResponse[WorkflowResponse]:
    """Mark a workflow cancelled; execution is owned by a later engine phase."""
    repository = WorkflowRepository(session)
    workflow = await repository.get(workflow_id)
    if workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found.")
    if workflow.status not in {"completed", "failed", "cancelled"}:
        workflow.status = "cancelled"
        workflow.completed_at = datetime.now(UTC)
        await repository.update(workflow)
    return ApiResponse(success=True, data=_response(workflow))
