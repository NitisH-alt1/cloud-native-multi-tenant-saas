from auth.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token
)


def test_password_hashing():
    password = "StrongPassword123"

    hashed_password = hash_password(password)

    assert hashed_password != password
    assert verify_password(password, hashed_password)


def test_wrong_password_fails():
    password = "StrongPassword123"
    wrong_password = "WrongPassword123"

    hashed_password = hash_password(password)

    assert not verify_password(
        wrong_password,
        hashed_password
    )


def test_access_token_creation_and_decoding():
    token_data = {
        "user_id": 1,
        "tenant_id": 1,
        "role": "admin"
    }

    token = create_access_token(token_data)

    decoded_data = decode_access_token(token)

    assert decoded_data["user_id"] == 1
    assert decoded_data["tenant_id"] == 1
    assert decoded_data["role"] == "admin"
    assert "exp" in decoded_data
