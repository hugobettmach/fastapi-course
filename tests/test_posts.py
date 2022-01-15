import pytest
from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)

    _ = list(map(validate, response.json()))
    assert len(response.json()) == len(test_posts)
    assert response.status_code == 200


def test_unauthorized_user_get_all_posts(client):
    response = client.get("/posts/")
    assert response.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    response = client.get(f"/posts/{test_posts.pop(0).id}")
    assert response.status_code == 401


def test_get_one_post_not_exists(authorized_client, test_posts):
    response = authorized_client.get("/posts/666")
    assert response.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**response.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title


@pytest.mark.parametrize(
    "title, content, published",
    [
        ("awesome_new_title", "awesome_new_content", True),
        ("favourite pizza", "i love margherita", False),
        ("tallest skyscrapers", "wahoo", True),
        ("coolest rock", "an eclogite surely", None),
    ],
)
def test_create_post(authorized_client, test_user, title, content, published):
    response = authorized_client.post(
        "/posts/", json={"title": title, "content": content, "published": published}
    )
    created_post = schemas.PostResponse(**response.json())
    assert response.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.user_id == test_user.get("id")
    if published is None:
        assert created_post.published is True
    else:
        assert created_post.published == published


def test_unauthorized_user_create_post(client):
    response = client.post(
        "/posts/",
        json={"title": "I should", "content": "not be able to do this"},
    )
    assert response.status_code == 401


def test_unauthorized_user_delete_post(client, test_posts):
    response = client.delete(f"/posts/{test_posts.pop(0).id}")
    assert response.status_code == 401


def test_delete_post_success(authorized_client, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts.pop(0).id}")
    assert response.status_code == 204


def test_delete_post_non_exist(authorized_client):
    response = authorized_client.delete("/posts/666")
    assert response.status_code == 404


def test_delete_other_user_post(authorized_client, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts.pop(3).id}")
    assert response.status_code == 403


def test_update_post(authorized_client, test_posts, updated_post_data):
    response = authorized_client.put(
        f"/posts/{test_posts[0].id}", json=updated_post_data
    )
    updated_post = schemas.PostResponse(**response.json())
    assert response.status_code == 200
    assert updated_post.title == updated_post_data.get("title")
    assert updated_post.content == updated_post_data.get("content")


def test_update_other_user_post(authorized_client, test_posts, updated_post_data):
    response = authorized_client.put(
        f"/posts/{test_posts.pop(3).id}", json=updated_post_data
    )
    assert response.status_code == 403


def test_unauthorized_user_update_post(client, test_posts, updated_post_data):
    response = client.put(f"/posts/{test_posts.pop(0).id}", json=updated_post_data)
    assert response.status_code == 401


def test_update_post_non_exist(authorized_client, updated_post_data):
    response = authorized_client.put("/posts/666", json=updated_post_data)
    assert response.status_code == 404
