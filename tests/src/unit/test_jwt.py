from src.common.decode_auth_token import get_decoded_data


def test_jwt_decoding(get_encoded_token, user_settings):
    decoded_token = get_decoded_data(get_encoded_token)

    assert decoded_token["user_id"] == user_settings["user_id"]
