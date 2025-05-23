from fastapi import status
import pytest
from app import models

@pytest.fixture()
def test_vote(session, test_posts, test_user, test_user1):
    vote_data = [{"post_id" : test_posts[3].id, "user_id" : test_user['id']},
                 {"post_id" : test_posts[1].id, "user_id" : test_user1['id']}]
    # new_vote = models.Vote(vote_data)
    # session.add(new_vote)
    def create_vote_model(votes):
        return models.Vote(**votes)
    vote_map = map(create_vote_model, vote_data)
    votes = list(vote_map)
    session.add_all(votes)
    session.commit()



def test_vote_on_post(authorised_client, test_posts):
    res = authorised_client.post("/vote", json = {"post_id" : test_posts[3].id, "dir" : 1})
    assert res.status_code == status.HTTP_200_OK
    assert res.json().get('message') == "sucessfully added a vote"

def test_vote_on_own_post(authorised_client, test_posts, test_user):
    res = authorised_client.post("/vote", json = {"post_id" : test_posts[0].id, "dir" : 1})
    assert res.status_code == status.HTTP_409_CONFLICT
    assert res.json().get('detail') == f'user {test_user['id']} can not vote own on post'

def test_vote_twice_post(authorised_client, test_posts, test_user, test_vote):
    res = authorised_client.post("/vote" , json = {"post_id" : test_posts[3].id, "dir" : 1})
    assert res.status_code == status.HTTP_409_CONFLICT
    assert res.json().get('detail') == f'user {test_user['id']} has already voted on post {test_posts[3].id}'

def test_delete_vote(authorised_client, test_posts, test_vote):
    res = authorised_client.post("/vote" , json = {"post_id" : test_posts[3].id, "dir" : 0})
    assert res.status_code == status.HTTP_200_OK
    assert res.json().get('message') == "successfully deleted vote"

def test_delete_vote_non_exist(authorised_client, test_posts):
    res = authorised_client.post("/vote", json = {"post_id" : test_posts[4].id, "dir" : 0})
    assert res.status_code == status.HTTP_404_NOT_FOUND
    assert res.json().get('detail') == "vote does not exists"

def test_vote_non_exist_post(authorised_client):
    res = authorised_client.post("/vote", json = {"post_id" : 1111, "dir" : 1})
    assert res.status_code == status.HTTP_404_NOT_FOUND
    assert res.json().get('detail') == f'post with id 1111 does not exists '

def test_vote_unauthorized_user(client, test_posts):
    res = client.post("/vote", json = {"post_id" : test_posts[0].id, "dir" : 1})
    assert res.status_code == status.HTTP_401_UNAUTHORIZED



