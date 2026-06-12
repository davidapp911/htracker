import pytest

from backend.schemas.stats import StreakResponse, SummaryResponse

_CUTOFF = 7


@pytest.mark.stats
def test_get_streak(client, create_completion, auth_headers):
    response = client.get("/stats/streaks", headers=auth_headers)

    habit_stats = response.json()[0]

    assert response.status_code == 200
    StreakResponse.model_validate(habit_stats)
    assert habit_stats["streak_length"] == 1


@pytest.mark.stats
def test_get_zero_length_streak(client, create_habit, auth_headers):
    response = client.get("/stats/streaks", headers=auth_headers)

    habit_stats = response.json()[0]

    assert response.status_code == 200
    StreakResponse.model_validate(habit_stats)
    assert habit_stats["streak_length"] == 0


@pytest.mark.stats
@pytest.mark.parametrize(
    "habit_count, completions_patterns, streak_lengths",
    [(2, [[-1, 0, 1, 2, 4], [-1, 0, 1, 3, 4]], [3, 2])],
)  # offsets from today: negative = future (ignored by streak), positive = days ago
def test_get_multiple_habit_streaks(
    client,
    auth_headers,
    create_data_for_user,
    habit_count,
    completions_patterns,
    streak_lengths,
):
    create_data_for_user(habit_count, completions_patterns)

    response = client.get("/stats/streaks", headers=auth_headers)

    assert response.status_code == 200

    for item, expected in zip(response.json(), streak_lengths):
        StreakResponse.model_validate(item)
        assert item["streak_length"] == expected


@pytest.mark.stats
def test_zero_habits(client, auth_headers):
    response = client.get("/stats/streaks", headers=auth_headers)

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.stats
def test_streaks_unauthorized_user(client):
    response = client.get("/stats/streaks")

    assert response.status_code == 401


@pytest.mark.stats
@pytest.mark.parametrize(
    "completions_pattern, longest_streak",
    [([0, 1, 2, 3, 4, 5, 6, 7, 9, 10], 8)],
)
def test_get_summary(
    client,
    auth_headers,
    create_habit,
    create_multiple_completions,
    completions_pattern,
    longest_streak,
):
    create_multiple_completions(completions_pattern, create_habit)
    response = client.get("/stats/summary", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["longest_streak"] == longest_streak
    SummaryResponse.model_validate(response.json())


@pytest.mark.stats
def test_get_summary_no_habits(client, auth_headers):
    response = client.get("/stats/summary", headers=auth_headers)

    assert response.status_code == 200
    SummaryResponse.model_validate(response.json())

    assert all(v == 0 for v in response.json().values())


@pytest.mark.stats
def test_get_summary_no_completions(client, auth_headers, create_habit):
    expected_summary = [0, 7, 0]  # default day value is 7
    response = client.get("/stats/summary", headers=auth_headers)

    assert response.status_code == 200
    SummaryResponse.model_validate(response.json())
    summary = response.json()
    assert all(a == b for a, b in zip(summary.values(), expected_summary))


@pytest.mark.stats
@pytest.mark.parametrize(
    "habit_count, completions_patterns, expected_summary",
    [(2, [[0, 1, 2, 4, 5, 6], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]], [13, 1, 10])],
)
def test_summary_cutoff(
    client,
    auth_headers,
    create_data_for_user,
    habit_count,
    completions_patterns,
    expected_summary,
):
    create_data_for_user(habit_count, completions_patterns)
    response = client.get(f"/stats/summary?days={_CUTOFF}", headers=auth_headers)
    summary = response.json()

    assert response.status_code == 200

    assert all(a == b for a, b in zip(summary.values(), expected_summary))


@pytest.mark.stats
def test_summary_unauthorized_user(client):
    response = client.get("/stats/summary")

    assert response.status_code == 401
