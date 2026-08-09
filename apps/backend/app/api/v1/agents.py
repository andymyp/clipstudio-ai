"""Agent management endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...dependencies.api import (
    UserContext,
    get_agent_manager,
    get_db_session,
    get_user_context,
)
from ...repositories.agents import AgentRepository
from ...schemas.api import AgentResponse, AgentUpdate, JobResponse, Page
from ...schemas.common import ApiResponse
from ...schemas.entities import AgentCreate
from ...services.agents.manager import (
    AgentManager,
    AgentNotFoundError,
    AgentOperationError,
)

router = APIRouter(prefix="/agents", tags=["agents"])


@router.get("", response_model=ApiResponse[Page[AgentResponse]], summary="List agents")
async def list_agents(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_db_session),
    _: UserContext = Depends(get_user_context),
) -> ApiResponse[Page[AgentResponse]]:
    """List persisted agents with bounded pagination."""
    items = await AgentRepository(session).list(limit=limit, offset=offset)
    page = Page(
        items=[AgentResponse.model_validate(item) for item in items],
        limit=limit,
        offset=offset,
        returned=len(items),
    )
    return ApiResponse(success=True, data=page)


@router.post(
    "", response_model=ApiResponse[AgentResponse], status_code=status.HTTP_201_CREATED
)
async def create_agent(
    payload: AgentCreate,
    session: AsyncSession = Depends(get_db_session),
    manager: AgentManager = Depends(get_agent_manager),
    _: UserContext = Depends(get_user_context),
) -> ApiResponse[AgentResponse]:
    """Create an inactive agent definition."""
    agent = await manager.create(payload)
    return ApiResponse(success=True, data=AgentResponse.model_validate(agent))


@router.get("/{agent_id}", response_model=ApiResponse[AgentResponse])
async def get_agent(
    agent_id: str,
    session: AsyncSession = Depends(get_db_session),
    _: UserContext = Depends(get_user_context),
) -> ApiResponse[AgentResponse]:
    """Get an agent by id."""
    agent = await AgentRepository(session).get(agent_id)
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found.") from None
    return ApiResponse(success=True, data=AgentResponse.model_validate(agent))


@router.put("/{agent_id}", response_model=ApiResponse[AgentResponse])
async def update_agent(
    agent_id: str,
    payload: AgentUpdate,
    session: AsyncSession = Depends(get_db_session),
    _: UserContext = Depends(get_user_context),
) -> ApiResponse[AgentResponse]:
    """Update mutable agent definition fields."""
    repository = AgentRepository(session)
    agent = await repository.get(agent_id)
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found.") from None
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(agent, field, value)
    await repository.update(agent)
    return ApiResponse(success=True, data=AgentResponse.model_validate(agent))


@router.delete("/{agent_id}", response_model=ApiResponse[dict[str, bool]])
async def delete_agent(
    agent_id: str,
    session: AsyncSession = Depends(get_db_session),
    manager: AgentManager = Depends(get_agent_manager),
    _: UserContext = Depends(get_user_context),
) -> ApiResponse[dict[str, bool]]:
    """Delete an agent definition."""
    try:
        await manager.delete(agent_id)
    except AgentNotFoundError:
        raise HTTPException(status_code=404, detail="Agent not found.") from None
    return ApiResponse(success=True, data={"deleted": True})


async def _set_agent_status(
    agent_id: str, new_status: str, session: AsyncSession
) -> ApiResponse[AgentResponse]:
    repository = AgentRepository(session)
    agent = await repository.get(agent_id)
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found.") from None
    agent.status = new_status
    await repository.update(agent)
    return ApiResponse(success=True, data=AgentResponse.model_validate(agent))


@router.post("/{agent_id}/activate", response_model=ApiResponse[AgentResponse])
async def activate_agent(
    agent_id: str,
    session: AsyncSession = Depends(get_db_session),
    manager: AgentManager = Depends(get_agent_manager),
    _: UserContext = Depends(get_user_context),
) -> ApiResponse[AgentResponse]:
    """Activate an agent without starting execution."""
    try:
        agent = await manager.activate(agent_id)
    except AgentNotFoundError:
        raise HTTPException(status_code=404, detail="Agent not found.") from None
    except AgentOperationError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return ApiResponse(success=True, data=AgentResponse.model_validate(agent))


@router.post("/{agent_id}/pause", response_model=ApiResponse[AgentResponse])
async def pause_agent(
    agent_id: str,
    session: AsyncSession = Depends(get_db_session),
    manager: AgentManager = Depends(get_agent_manager),
    _: UserContext = Depends(get_user_context),
) -> ApiResponse[AgentResponse]:
    """Pause an agent without cancelling persisted work."""
    try:
        agent = await manager.pause(agent_id)
    except AgentNotFoundError:
        raise HTTPException(status_code=404, detail="Agent not found.") from None
    except AgentOperationError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return ApiResponse(success=True, data=AgentResponse.model_validate(agent))


@router.post(
    "/{agent_id}/run", response_model=ApiResponse[JobResponse], status_code=202
)
async def run_agent(
    agent_id: str,
    session: AsyncSession = Depends(get_db_session),
    manager: AgentManager = Depends(get_agent_manager),
    _: UserContext = Depends(get_user_context),
) -> ApiResponse[JobResponse]:
    """Queue an agent run placeholder for the future workflow engine."""
    try:
        job_id = await manager.enqueue(agent_id)
    except AgentNotFoundError:
        raise HTTPException(status_code=404, detail="Agent not found.") from None
    except AgentOperationError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return ApiResponse(success=True, data=JobResponse(job_id=job_id))
