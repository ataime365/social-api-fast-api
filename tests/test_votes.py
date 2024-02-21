import pytest
from app import models


@pytest.fixture()
def test_vote(test_conf_posts, session, test_user):
    new_vote = models.Vote(post_id=test_conf_posts[3].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()


def test_vote_on_post(authorized_client, test_conf_posts):
    res = authorized_client.post(
        "/vote/", json={"post_id": test_conf_posts[3].id, "vote_dir": 1})
    assert res.status_code == 201


def test_vote_twice_post(authorized_client, test_conf_posts, test_vote):
    res = authorized_client.post(
        "/vote/", json={"post_id": test_conf_posts[3].id, "vote_dir": 1})
    assert res.status_code == 409


def test_delete_vote(authorized_client, test_conf_posts, test_vote):
    res = authorized_client.post(
        "/vote/", json={"post_id": test_conf_posts[3].id, "vote_dir": 0})
    assert res.status_code == 201


def test_delete_vote_non_exist(authorized_client, test_conf_posts):
    res = authorized_client.post(
        "/vote/", json={"post_id": test_conf_posts[3].id, "vote_dir": 0})
    assert res.status_code == 404


def test_vote_post_non_exist(authorized_client, test_conf_posts):
    res = authorized_client.post(
        "/vote/", json={"post_id": 80000, "vote_dir": 1})
    assert res.status_code == 404


def test_vote_unauthorized_user(client, test_conf_posts):
    res = client.post(
        "/vote/", json={"post_id": test_conf_posts[3].id, "vote_dir": 1})
    assert res.status_code == 401