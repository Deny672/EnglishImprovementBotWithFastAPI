import random

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.models import Word
from app.schemas.word_schema import WordCreate, WordDetailResponse


async def word_by_id(word_id: int, session: AsyncSession):
    result = await session.execute(select(Word).filter(Word.id == word_id))
    word = result.scalars().first()
    if word is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Word not found")
    return WordDetailResponse.model_validate(word)


async def get_words(limit: int, offset: int, session: AsyncSession):
    result = await session.execute(select(Word).order_by(Word.id).offset(offset).limit(limit))
    words = result.scalars().all()
    if not words:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Words do not exist")
    words_for_return = [WordDetailResponse.model_validate(word) for word in words]
    return words_for_return


async def words_by_tg_user_id(tg_user_id: int, session: AsyncSession):
    result = await session.execute(select(Word).filter(Word.tg_user_id == tg_user_id))
    words = result.scalars().all()
    if not words:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This user's words were not found")
    words_for_return = [WordDetailResponse.model_validate(word) for word in words]
    return words_for_return


async def select_words_for_quiz(tg_user_id: int, session: AsyncSession):
    result = await session.execute(select(Word).filter(Word.tg_user_id == tg_user_id))
    words = result.scalars().all()
    if not words:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This user's words were not found")

    if len(words) < 4:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not enough unique words for the quiz"
        )

    selected_word = random.choice(words)
    correct_translation = selected_word.translation

    words.remove(selected_word)

    wrong_translations_set = set()

    for word in words:
        if len(wrong_translations_set) < 3 and word.translation != correct_translation:
            wrong_translations_set.add(word.translation)

    if len(wrong_translations_set) < 3:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not enough unique wrong translations available"
        )

    wrong_translations = list(wrong_translations_set)

    quiz = {
        "word_for_translate": selected_word.word,
        "correct_translations": correct_translation,
        "incorrect_translate_list": wrong_translations,
    }

    return quiz


async def create_word(session: AsyncSession, word: WordCreate) -> Word:

    word_exist = await session.execute(
        select(Word).filter(
            Word.tg_user_id == word.tg_user_id, Word.word == word.word, Word.translation == word.translation
        )
    )
    if word_exist.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The specified word with the specified translation already exists",
        )
    word_data = Word()
    word_data.word = word.word
    word_data.translation = word.translation
    word_data.tg_user_id = word.tg_user_id
    session.add(word_data)
    await session.commit()
    await session.refresh(word_data)
    return WordDetailResponse.model_validate(word_data)


async def delete_word(word_id: int, session: AsyncSession):
    result = await session.execute(select(Word).filter(Word.id == word_id))
    word = result.scalars().first()

    if word is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Word not found")

    await session.delete(word)
    await session.commit()
    return word
