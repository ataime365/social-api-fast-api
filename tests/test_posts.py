from typing import List
from app import schemas
import pytest


def test_get_all_posts(authorized_client, test_conf_posts):
    res = authorized_client.get("/posts/")

    def validate(post): #we want to use python mapping
        return schemas.PostWithVoteCount(**post)
    
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)
    assert len(res.json()) == len(test_conf_posts)
    assert res.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_conf_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_user_get_one_post(client, test_conf_posts):
    res = client.get(f"/posts/{test_conf_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exists(authorized_client, test_conf_posts):
    res = authorized_client.get(f"/posts/8888")
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_conf_posts):
    res = authorized_client.get(f"/posts/{test_conf_posts[0].id}")
    # print(res.json())
    post = schemas.PostWithVoteCount(**res.json())
    # print(post)
    # print(post.post.title)
    assert post.post.id == test_conf_posts[0].id
    assert post.post.title == test_conf_posts[0].title
    assert post.post.content == test_conf_posts[0].content
    assert res.status_code == 200


@pytest.mark.parametrize("title, content, published", [
                    ("awesome new title", "awesome new content", True),
                    ("favourite pizza", "I love pepperoni", False),
                    ("tallest skyscrapers", "wahoo", True),
])
def test_create_post(authorized_client, test_user, test_conf_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title":title, "content": content, "published": published})
    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']

def test_create_post_published_true(authorized_client, test_user, test_conf_posts):
    res = authorized_client.post("/posts/", json={"title":"arbitrary title", "content": "Random content"})
    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == "arbitrary title"
    assert created_post.content == "Random content"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']

def test_unauthorized_user_create_post(client,test_user ,test_conf_posts):
    res = client.post("/posts/", json={"title":"arbitrary title", "content": "Random content"})
    assert res.status_code == 401

def test_unauthorized_user_delete_Post(client, test_user, test_conf_posts):
    res = client.delete(
        f"/posts/{test_conf_posts[0].id}")
    assert res.status_code == 401


def test_delete_post_success(authorized_client, test_user, test_conf_posts):
    res = authorized_client.delete(
        f"/posts/{test_conf_posts[0].id}")

    assert res.status_code == 204


def test_delete_post_non_exist(authorized_client, test_user, test_conf_posts):
    res = authorized_client.delete(
        f"/posts/8000000")
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_conf_posts):
    res = authorized_client.delete(
        f"/posts/{test_conf_posts[3].id}")
    assert res.status_code == 403


def test_update_post(authorized_client, test_user, test_conf_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_conf_posts[0].id

    }
    res = authorized_client.put(f"/posts/{test_conf_posts[0].id}", json=data)
    updated_post = schemas.PostResponse(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']


def test_update_other_user_post(authorized_client, test_user, test_user2, test_conf_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_conf_posts[3].id

    }
    res = authorized_client.put(f"/posts/{test_conf_posts[3].id}", json=data)
    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_user, test_conf_posts):
    res = client.put(
        f"/posts/{test_conf_posts[0].id}")
    assert res.status_code == 401


def test_update_post_non_exist(authorized_client, test_user, test_conf_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_conf_posts[3].id

    }
    res = authorized_client.put(
        f"/posts/8000000", json=data)

    assert res.status_code == 404

    