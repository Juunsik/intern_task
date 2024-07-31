from django.test import TestCase
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

# Create your tests here.
User = get_user_model()


# Signup success
@pytest.mark.django_db
def test_register_success():
    client = APIClient()
    url = reverse("register")

    data = {
        "username": "newuser",
        "password": "newpassword123",
        "nickname": "newnickname",
    }

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["username"] == data["username"]
    assert User.objects.filter(username=data["username"]).exists()


# username 중복 검증
@pytest.mark.django_db
def test_register_username_exists():
    existing_user = User.objects.create_user(
        username="user1", password="password123", nickname="nickname1"
    )

    client = APIClient()
    url = reverse("register")

    data = {"username": "user1", "password": "newpassword123", "nickname": "nickname2"}

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "username" in response.data
    assert response.data["username"][0] == "user with this username already exists."


# nickname 중복 검증
@pytest.mark.django_db
def test_register_nickname_exists():
    existing_user = User.objects.create_user(
        username="user2", password="password123", nickname="nickname2"
    )

    client = APIClient()
    url = reverse("register")

    data = {"username": "user3", "password": "newpassword123", "nickname": "nickname2"}

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "nickname" in response.data
    assert response.data["nickname"][0] == "user with this nickname already exists."


# Login success
@pytest.mark.django_db
def test_login_success():
    user = User.objects.create_user(
        username="user1", password="password123", nickname="nickname"
    )

    client = APIClient()
    url = reverse("login")

    data = {"username": "user1", "password": "password123"}

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.data


# 없는 아이디로 로그인
@pytest.mark.django_db
def test_login_invalid_username():
    client = APIClient()
    url = reverse("login")

    data = {"username": "user2", "password": "password123"}

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "message" in response.data
    assert response.data["message"] == "존재하지 않는 아이디입니다."


# 잘못된 password
@pytest.mark.django_db
def test_login_invalid_password():
    user = User.objects.create_user(
        username="user2", password="password123", nickname="nickname"
    )

    client = APIClient()
    url = reverse("login")

    data = {"username": "user2", "password": "password345"}

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "message" in response.data
    assert response.data["message"] == "잘못된 비밀번호입니다."
