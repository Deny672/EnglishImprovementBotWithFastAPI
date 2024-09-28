import pytest

from tests import constant


@pytest.mark.asyncio
async def test_get_word_by_id_success(inserted_words_in_test_db, word_test_data, client):
    for i in range(len(word_test_data)):
        response = await client.get(f"/words/{i+1}/")
        assert response.json()["word"] == word_test_data[i]["word"]
        assert response.json()["translation"] == word_test_data[i]["translation"]
        assert response.json()["tg_user_id"] == word_test_data[i]["tg_user_id"]


@pytest.mark.asyncio
async def test_get_word_by_id_not_found_404(client):
    response = await client.get("/words/123141/")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_all_words_success(inserted_words_in_test_db, word_test_data, client):
    response = await client.get("/words/all")
    assert response.status_code == 200
    for i, data in enumerate(response.json()):
        assert data["word"] == word_test_data[i]["word"]
        assert data["translation"] == word_test_data[i]["translation"]
        assert data["tg_user_id"] == word_test_data[i]["tg_user_id"]


@pytest.mark.asyncio
async def test_get_all_words_not_found_404(client):
    response = await client.get("/words/all")
    assert response.status_code == 404
    assert response.json() == {"detail": "Words do not exist"}


@pytest.mark.asyncio
async def test_get_words_pagination_success(inserted_words_in_test_db, word_test_data, client):
    response = await client.get(f"/words/all?limit={constant.LIMIT}&offset={constant.OFFSET}")
    assert response.status_code == 200
    for i, data in enumerate(response.json()):
        assert data["word"] == word_test_data[i + constant.OFFSET]["word"]
        assert data["translation"] == word_test_data[i + constant.OFFSET]["translation"]
        assert data["tg_user_id"] == word_test_data[i + constant.OFFSET]["tg_user_id"]


@pytest.mark.asyncio
async def test_get_words_pagination_not_found_404(client):
    response = await client.get(f"/words/all?limit={constant.LIMIT}&offset={constant.OFFSET}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Words do not exist"}


@pytest.mark.asyncio
async def test_get_words_by_user_success(inserted_user_specific_words, user_word_test_data, client):
    response = await client.get(f"/words/user/{user_word_test_data[0]['tg_user_id']}/")
    print(response.json())
    assert response.status_code == 200
    assert response.json()[0]["word"] == user_word_test_data[0]["word"]
    assert response.json()[0]["translation"] == user_word_test_data[0]["translation"]
    assert response.json()[0]["tg_user_id"] == user_word_test_data[0]["tg_user_id"]
    assert response.json()[0]["tg_user_id"] != user_word_test_data[1]["tg_user_id"]


@pytest.mark.asyncio
async def test_get_words_by_user_not_found_404(client):
    response = await client.get(f"/words/user/{1}/")
    assert response.status_code == 404
    assert response.json() == {"detail": "This user's words were not found"}


@pytest.mark.asyncio
async def test_quiz_word_selection_user_not_found_returns_404(
    inserted_user_specific_words, user_word_test_data, client
):
    response = await client.get(f"/words/test/{52}")
    assert response.status_code == 404
    assert response.json() == {"detail": "This user's words were not found"}


@pytest.mark.asyncio
async def test_quiz_word_selection_insufficient_unique_words_returns_404(
    inserted_user_specific_words, user_word_test_data, client
):
    response = await client.get(f"/words/test/{user_word_test_data[1]['tg_user_id']}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not enough unique words for the quiz"}


@pytest.mark.asyncio
async def test_quiz_word_selection_insufficient_wrong_translations_returns_404(
    inserted_user_specific_words, user_word_test_data, client
):
    response = await client.get(f"/words/test/{user_word_test_data[7]['tg_user_id']}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not enough unique wrong translations available"}


@pytest.mark.asyncio
async def test_quiz_word_selection_success_returns_200(
    inserted_user_specific_words, user_word_test_data, client
):
    response = await client.get(f"/words/test/{user_word_test_data[2]['tg_user_id']}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_word_success_returns_201(client):
    data = {"word": "Удобный", "translation": "Convenient", "tg_user_id": 121444}
    response = await client.post("/words/", json=data)
    assert response.status_code == 201
    assert response.json()["word"] == data["word"]
    assert response.json()["translation"] == data["translation"]
    assert response.json()["tg_user_id"] == data["tg_user_id"]


@pytest.mark.asyncio
async def test_create_word_already_exists_returns_404(
    inserted_user_specific_words, user_word_test_data, client
):
    data = {
        "word": user_word_test_data[1]["word"],
        "translation": user_word_test_data[1]["translation"],
        "tg_user_id": user_word_test_data[1]["tg_user_id"],
    }
    response = await client.post("/words/", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": "The specified word with the specified translation already exists"}


@pytest.mark.asyncio
async def test_delete_word_success_returns_200(inserted_user_specific_words, user_word_test_data, client):
    response = await client.delete(f"/words/{1}")
    assert response.status_code == 200
    assert response.json()["word"] == user_word_test_data[0]["word"]
    assert response.json()["translation"] == user_word_test_data[0]["translation"]
    assert response.json()["tg_user_id"] == user_word_test_data[0]["tg_user_id"]


@pytest.mark.asyncio
async def test_delete_word_not_found_returns_404(inserted_user_specific_words, user_word_test_data, client):
    response = await client.delete(f"/words/{15646}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Word not found"}
