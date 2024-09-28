from typing import List

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgres_session import get_session
from app.schemas.word_schema import WordCreate, WordDetailResponse
from app.services.word_crud import (
    create_word,
    delete_word,
    get_words,
    select_words_for_quiz,
    word_by_id,
    words_by_tg_user_id,
)

router = APIRouter(prefix="/words", tags=["words"])


@router.get("/{word_id}/", response_model=WordDetailResponse, status_code=status.HTTP_200_OK)
async def word_by_id_route(word_id: int, session: AsyncSession = Depends(get_session)):
    return await word_by_id(word_id=word_id, session=session)


@router.get("/all", response_model=List[WordDetailResponse], status_code=status.HTTP_200_OK)
async def get_all_words_route(
    limit: int = Query(default=3, ge=1),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_session),
):
    return await get_words(limit=limit, offset=offset, session=session)


@router.get("/user/{tg_user_id}/", response_model=List[WordDetailResponse], status_code=status.HTTP_200_OK)
async def words_by_tg_user_id_route(tg_user_id: int, session: AsyncSession = Depends(get_session)):
    return await words_by_tg_user_id(tg_user_id=tg_user_id, session=session)


@router.get("/test/{tg_user_id}", status_code=status.HTTP_200_OK)
async def select_words_for_quiz_route(tg_user_id: int, session: AsyncSession = Depends(get_session)):
    return await select_words_for_quiz(tg_user_id=tg_user_id, session=session)


@router.post("/", response_model=WordDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_word_route(word_create: WordCreate, session: AsyncSession = Depends(get_session)):
    return await create_word(session=session, word=word_create)


@router.delete("/{word_id}", response_model=WordDetailResponse, status_code=status.HTTP_200_OK)
async def delete_word_route(word_id: int, session: AsyncSession = Depends(get_session)):
    return await delete_word(word_id=word_id, session=session)
