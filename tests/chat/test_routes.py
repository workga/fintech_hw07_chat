def test_websocket(client):
    with client.websocket_connect("/chat/connection") as websocket:
        data = websocket.receive_json()
        assert data == {"message": "Hello!"}