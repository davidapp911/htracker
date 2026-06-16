import pytest

from backend.schemas.habit import HabitCompletionResponse, HabitResponse
from tests.constants import COMPLETION_TODAY, HABIT_UPDATE_DATA, NOT_FOUND_ID


@pytest.mark.habits
def test_create_habit(client, auth_headers, habit_factory):
    new_habit = habit_factory.build()
    response = client.post(
        "/habits/",
        json={"name": new_habit.name, "frequency": new_habit.frequency},
        headers=auth_headers,
    )

    assert response.status_code == 201
    HabitResponse.model_validate(response.json())
    assert response.json()["name"] == new_habit.name
    assert response.json()["frequency"] == new_habit.frequency


@pytest.mark.habits
@pytest.mark.parametrize("count", [0, 10])
def test_list_habits(client, auth_headers, create_multiple_habits, count):
    create_multiple_habits(count)
    response = client.get("/habits/", headers=auth_headers)

    assert response.status_code == 200
    for habit in response.json():
        HabitResponse.model_validate(habit)


@pytest.mark.habits
def test_list_habits_no_auth(client):
    response = client.get("/habits/")

    assert response.status_code == 401


@pytest.mark.habits
def test_get_habit_by_id(client, auth_headers, create_habit):
    response = client.get(f"/habits/{create_habit.id}", headers=auth_headers)
    habit_data = response.json()

    assert response.status_code == 200
    HabitResponse.model_validate(habit_data)
    assert habit_data["id"] == create_habit.id
    assert habit_data["name"] == create_habit.name
    assert habit_data["frequency"] == create_habit.frequency


@pytest.mark.habits
def test_get_habit_by_id_wrong_user(client, auth_headers, user_factory, habit_factory):
    new_habit = habit_factory.create(user=user_factory.create())
    response = client.get(f"/habits/{new_habit.id}", headers=auth_headers)

    assert response.status_code == 403


@pytest.mark.habits
def test_get_habit_by_id_not_found(client, auth_headers):
    response = client.get(f"/habits/{NOT_FOUND_ID}", headers=auth_headers)

    assert response.status_code == 404


@pytest.mark.habits
def test_update_habit(client, auth_headers, create_habit):
    response = client.put(
        f"/habits/{create_habit.id}", json=HABIT_UPDATE_DATA, headers=auth_headers
    )
    habit_data = response.json()

    assert response.status_code == 200
    HabitResponse.model_validate(habit_data)
    assert habit_data["name"] == HABIT_UPDATE_DATA["name"]
    assert habit_data["frequency"] == HABIT_UPDATE_DATA["frequency"]


@pytest.mark.habits
def test_update_habit_no_auth(client, create_habit):
    response = client.put(f"/habits/{create_habit.id}", json=HABIT_UPDATE_DATA)

    assert response.status_code == 401


@pytest.mark.habits
def test_update_habit_wrong_user(client, auth_headers, user_factory, habit_factory):
    new_habit = habit_factory.create(user=user_factory.create())
    response = client.put(f"/habits/{new_habit.id}", json=HABIT_UPDATE_DATA, headers=auth_headers)

    assert response.status_code == 403


@pytest.mark.habits
def test_update_habit_not_found(client, auth_headers):
    response = client.put(f"/habits/{NOT_FOUND_ID}", json=HABIT_UPDATE_DATA, headers=auth_headers)

    assert response.status_code == 404


@pytest.mark.habits
def test_delete_habit(client, auth_headers, create_habit):
    response = client.delete(f"/habits/{create_habit.id}", headers=auth_headers)

    assert response.status_code == 204


@pytest.mark.habits
def test_delete_habit_not_found(client, auth_headers):
    response = client.delete(f"/habits/{NOT_FOUND_ID}", headers=auth_headers)

    assert response.status_code == 404


@pytest.mark.habits
def test_delete_habit_wrong_user(client, auth_headers, user_factory, habit_factory):
    new_habit = habit_factory.create(user=user_factory.create())
    response = client.delete(f"/habits/{new_habit.id}", headers=auth_headers)

    assert response.status_code == 403


@pytest.mark.habits
def test_check_in(client, auth_headers, create_habit):
    response = client.post(
        f"/habits/{create_habit.id}/logs", json=COMPLETION_TODAY, headers=auth_headers
    )

    assert response.status_code == 201
    HabitCompletionResponse.model_validate(response.json())


@pytest.mark.habits
def test_check_in_duplicate(client, auth_headers, create_completion):
    response = client.post(
        f"/habits/{create_completion.habit.id}/logs",
        json=COMPLETION_TODAY,
        headers=auth_headers,
    )

    assert response.status_code == 409


@pytest.mark.habits
def test_check_in_wrong_user(client, auth_headers, user_factory, habit_factory):
    habit = habit_factory(user=user_factory())
    response = client.post(f"/habits/{habit.id}/logs", json=COMPLETION_TODAY, headers=auth_headers)

    assert response.status_code == 403


@pytest.mark.habits
def test_delete_checkin(client, auth_headers, create_completion):
    response = client.delete(
        f"/habits/{create_completion.habit.id}/logs/{create_completion.id}",
        headers=auth_headers,
    )

    assert response.status_code == 204


@pytest.mark.habits
def test_delete_checkin_not_found(client, auth_headers, create_habit):
    response = client.delete(f"/habits/{create_habit.id}/logs/{NOT_FOUND_ID}", headers=auth_headers)

    assert response.status_code == 404


@pytest.mark.habits
def test_delete_checkin_wrong_user(
    client, auth_headers, user_factory, habit_factory, completion_factory
):
    completion = completion_factory.create(habit=habit_factory.create(user=user_factory.create()))
    response = client.delete(
        f"/habits/{completion.habit.id}/logs/{completion.id}", headers=auth_headers
    )

    assert response.status_code == 403


@pytest.mark.habits
@pytest.mark.parametrize(
    "completions_pattern, actual_length", [([-1, 0, 1, 2], 3), ([-1, 1, 2], 2)]
)
def test_get_streak(
    client,
    auth_headers,
    create_habit,
    create_multiple_completions,
    completions_pattern,
    actual_length,
):
    create_multiple_completions(completions_pattern, create_habit)
    response = client.get(f"/habits/{create_habit.id}/streak", headers=auth_headers)

    assert response.status_code == 200
    assert response.json() == actual_length


@pytest.mark.habits
def test_get_streak_no_auth(client, create_habit):
    response = client.get(f"/habits/{create_habit.id}/streak")

    assert response.status_code == 401


@pytest.mark.habits
def test_create_habit_missing_field(client, auth_headers):
    response = client.post("/habits/", json={"name": "new habit"}, headers=auth_headers)

    assert response.status_code == 422


@pytest.mark.habits
def test_update_habit_invalid_type(client, auth_headers, create_habit):
    response = client.put(f"/habits/{create_habit.id}", json={"name": 123}, headers=auth_headers)

    assert response.status_code == 422


@pytest.mark.focus
def test_check_in_invalid_date(client, auth_headers, create_habit):
    response = client.post(
        f"/habits/{create_habit.id}/logs",
        json={"logged_at": "not-a-date"},
        headers=auth_headers,
    )

    assert response.status_code == 422
