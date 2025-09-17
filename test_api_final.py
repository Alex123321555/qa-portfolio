import requests
import pytest

BASE_URL = "https://jsonplaceholder.typicode.com/"

class TestJsonPlaceholderAPI:

    def test_create_new_post(self):
        new_post_data = {
            "title": "My test post",
            "body": "This is a test post created by my awesome autotest! Да-Да",
            "userId": 1
        }
        headers = {"Content-Type": "application/json"}

        response = requests.post(f"{BASE_URL}/posts", json=new_post_data, headers=headers)
        assert response.status_code == 201
        created_post = response.json()

        assert created_post["title"] == new_post_data["title"]
        assert created_post["body"] == new_post_data["body"]
        assert created_post["userId"] == new_post_data["userId"]
        assert "id" in created_post

    def test_get_all_posts(self):
        response = requests.get(f"{BASE_URL}/posts")

        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json; charset=utf-8"

        posts = response.json()
        assert isinstance(posts, list)
        assert len(posts) > 0

        for post in posts[:3]:
            assert all(key in post for key in["userId", "id", "title", "body"])

    def test_get_post_by_id(self):
        target_id = 42
        response = requests.get(f"{BASE_URL}/posts/{target_id}")
        assert  response.status_code == 200

        post = response.json()
        assert post["id"] == target_id

    def test_delete_post_by_id(self):
        post_id_to_delete = 1
        response = requests.delete(f"{BASE_URL}/posts/{post_id_to_delete}")
        assert response.status_code in [200, 204], f"Ожидался статус 200 или 204, но получен {response.status_code}"
        #Просто проверка что успешно все
        if response.status_code == 200:
            deleted_post_data = response.json()
            print(f" DELETE /posts/1: Сервер вернул ответ с телом {deleted_post_data}")
        else:
            print(f" DELETE /posts/1: Пост успешно удален")
