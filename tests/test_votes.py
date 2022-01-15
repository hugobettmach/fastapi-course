def test_vote_on_post(authorized_client, test_posts):
    response = authorized_client.post(
        "/votes/", json={"post_id": test_posts.pop(3).id, "direction": 1}
    )
    assert response.status_code == 201


def test_vote_twice_on_post(authorized_client, test_posts, test_vote):
    response = authorized_client.post(
        "/votes/", json={"post_id": test_posts.pop(3).id, "direction": 1}
    )
    assert response.status_code == 409


def test_delete_vote(authorized_client, test_posts, test_vote):
    response = authorized_client.post(
        "/votes/", json={"post_id": test_posts.pop(3).id, "direction": 0}
    )
    assert response.status_code == 201


def test_delete_vote_non_exist(authorized_client, test_posts):
    response = authorized_client.post(
        "/votes/", json={"post_id": test_posts.pop(3).id, "direction": 0}
    )
    assert response.status_code == 404


def test_vote_on_post_non_exist(authorized_client):
    response = authorized_client.post("/votes/", json={"post_id": 666, "direction": 1})
    assert response.status_code == 404


def test_vote_unauthorized_user(client, test_posts):
    response = client.post(
        "/votes/", json={"post_id": test_posts.pop(3).id, "direction": 1}
    )
    assert response.status_code == 401
