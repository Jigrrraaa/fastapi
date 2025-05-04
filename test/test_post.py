from typing import List
from app import schemas
import pytest
from fastapi import status

def test_get_all_posts(authorised_client, test_posts):
    res = authorised_client.get("/posts")
    def validate(post):
        return schemas.PostOut(**post)
    post_map = map(validate, res.json())
    post_list = list(post_map)

    assert len(res.json()) == len(test_posts)
    assert res.status_code == status.HTTP_200_OK

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED 

def test_unauthorized_user_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED 

def test_get_one_post_not_exists(authorised_client, test_posts):
    res = authorised_client.get(f"/posts/8888")
    assert res.status_code == status.HTTP_404_NOT_FOUND 

def test_get_one_post(authorised_client, test_posts):
    res = authorised_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.post.id == test_posts[0].id
    assert post.post.title == test_posts[0].title
    assert post.post.content == test_posts[0].content

@pytest.mark.parametrize("title, content, published",[
    ("awesome title", "awesome content", True),
    ("Batsman", "Virat Kohli", False),
    ("Bowler", "Bumrah", True)
])
def test_create_post(authorised_client, test_user, test_posts, title,content,published):
    res = authorised_client.post("/posts", json = {"title" :title, "content" : content, "published" : published})
    # print (res.json())
    created_post = schemas.Post(**res.json())
    # print(created_post)
    assert res.status_code == status.HTTP_201_CREATED
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.who_created_user == test_user['id']


def test_create_post_default_published_true(authorised_client, test_user,test_posts):
    res = authorised_client.post("/posts", json = {"title" :"test default", "content" : "default content"})
    created_post = schemas.Post(**res.json())
    assert res.status_code == status.HTTP_201_CREATED
    assert created_post.title == "test default"
    assert created_post.content == "default content"
    assert created_post.published == True
    assert created_post.who_created_user == test_user['id']

def test_unauthorized_user_create_posts(client, test_posts, test_user):
    res = client.post("/posts", json = {"title" :"test default", "content" : "default content"})
    assert res.status_code == status.HTTP_401_UNAUTHORIZED 

def test_unauthorized_user_delete_posts(client, test_posts, test_user):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED 

def test_delete_post_sucess(authorised_client, test_posts, test_user):
    res = authorised_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == status.HTTP_204_NO_CONTENT 

def test_delete_post_non_exists(authorised_client, test_posts, test_user):
    res = authorised_client.delete(f"/posts/1234")
    assert res.status_code == status.HTTP_404_NOT_FOUND 
    assert res.json().get('detail') == "Post with id: 1234 does not exits"

def test_delete_other_user_post(authorised_client, test_user, test_posts):
    res = authorised_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == status.HTTP_403_FORBIDDEN
    assert res.json().get('detail') == "Not authorised to perform requested action"

def test_update_post(authorised_client, test_user, test_posts):
    data = {
        "title" : "Updated Title",
        "content" : "updated content",
        "id" : test_posts[0].id
    }

    res = authorised_client.put(f"/posts/{test_posts[0].id}", json = data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == status.HTTP_200_OK
    assert updated_post.id == data['id']
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']


def test_update_post_non_exists(authorised_client, test_posts, test_user):
    data = {
        "title" : "Updated Title",
        "content" : "updated content",
        "id" : test_posts[0].id
    }
    res = authorised_client.put(f"/posts/1234", json = data)
    assert res.status_code == status.HTTP_404_NOT_FOUND 
    assert res.json().get('detail') == "Post with id: 1234 does not exits"

def test_update_other_user_post(authorised_client, test_user, test_posts):
    data = {
        "title" : "Updated Title",
        "content" : "updated content",
        "id" : test_posts[3].id
    }
    res = authorised_client.put(f"/posts/{test_posts[3].id}", json = data)
    assert res.status_code == status.HTTP_403_FORBIDDEN
    assert res.json().get('detail') == "Not authorised to perform requested action"

    


