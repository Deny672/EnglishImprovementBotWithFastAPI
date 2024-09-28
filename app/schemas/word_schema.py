from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class WordSchema(BaseModel):
    id: int
    word: str = Field(max_length=50)
    translation: str = Field(max_length=50)
    tg_user_id: int
    created_at: str = datetime

    model_config = ConfigDict(from_attributes=True)


class WordDetailResponse(BaseModel):
    id: int
    word: str = Field(max_length=50)
    translation: str = Field(max_length=50)
    tg_user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WordCreate(BaseModel):
    word: str = Field(max_length=50)
    translation: str = Field(max_length=50)
    tg_user_id: int
