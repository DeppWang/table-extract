from comments.db import get_db


def test_hello(client):
    response = client.get("/hello")
    assert response.data == b"Hello, World!"


def test_post_comments(client, auth):
    """
    测试发表留言
    :param client:
    :param auth:
    :return:
    """
    # 未登录。期待：可查看留言
    response = client.get("/")
    assert b"Log In" in response.data
    assert b"Sign Up" in response.data
    assert b"test_content" in response.data
    assert b"test_user" in response.data

    result = client.get("/?is_json=1").json
    assert result['data'] == [
        {
            "id": 1,
            "content": "test_content",
            "parent": 0,
            "username": "test_user",
            "created_time": "2022-05-21 00:00:00",
            "child": []
        }
    ]

    # 未登录留言。期待：留言失败
    response = client.post("/", data={"content": "123", "parent": 1})
    assert b"Redirecting..." in response.data

    # 登录后留言。期待：留言成功
    auth.login()
    client.post("/", data={"content": "test_content2", "parent": 1})
    result = client.get("/?is_json=1").json
    data = result['data']
    # result['data'] == [{'id': 1, 'content': 'test_content', 'parent': 0, 'username': 'test_user',
    # 'created_time': '2022-05-21 00:00:00', 'child': [{'id': 2, 'content': 'test_content2', 'parent': 1,
    # 'username': 'test', 'created_time': '***', 'child': []}]}]
    assert len(data) == 1
    assert data[0]['id'] == 1
    assert len(data[0]['child']) == 1
    assert data[0]['child'][0]['content'] == "test_content2"
    assert data[0]['child'][0]['username'] == "test_user"
    assert data[0]['child'][0]['parent'] == 1


def test_get_comments(client, app):
    """
    测试获取留言
    :param client:
    :param app:
    :return:
    """
    # 当只有一条留言时。期待：正常返回
    result = client.get("/?is_json=1").json
    assert result['data'] == [
        {
            "id": 1,
            "content": "test_content",
            "parent": 0,
            "username": "test_user",
            "created_time": "2022-05-21 00:00:00",
            "child": []
        }
    ]

    # 当存在多条留言时。期待：按时间倒序排序
    with app.app_context():
        db = get_db()
        db.executemany(
            "INSERT INTO comments (content, parent, username, created_time) VALUES (?, ?, ?, ?)",
            [('test_content2', 0, 'test_user', "2022-05-22 01:00:00"),
             ('test_content3', 0, 'test_user', "2022-05-22 02:00:00"),
             ('test_content4', 3, 'test_user', "2022-05-22 03:00:00")]
        )
        db.commit()
    result = client.get("/?is_json=1").json
    assert result['data'] == [
        {
            "id": 3,
            "content": "test_content3",
            "parent": 0,
            "username": "test_user",
            "created_time": "2022-05-22 02:00:00",
            "child": [
                {
                    "id": 4,
                    "content": "test_content4",
                    "parent": 3,
                    "username": "test_user",
                    "created_time": "2022-05-22 03:00:00",
                    "child": []
                }
            ]
        },
        {
            "id": 2,
            "content": "test_content2",
            "parent": 0,
            "username": "test_user",
            "created_time": "2022-05-22 01:00:00",
            "child": []
        },
        {
            "id": 1,
            "content": "test_content",
            "parent": 0,
            "username": "test_user",
            "created_time": "2022-05-21 00:00:00",
            "child": []
        }
    ]

    # 当超过 50 层时。期待：正常返回
    with app.app_context():
        db = get_db()
        db.executemany(
            "INSERT INTO comments (content, parent, username, created_time) VALUES (?, ?, ?, ?)",
            [('test_content{}'.format(i), i - 1, 'test_user', "2022-05-22 04:00:00") for i in range(5, 60)]
        )
        db.commit()
    result = client.get("/?is_json=1").json
    assert len(result['data']) == 3
    assert result['data'][0]['id'] == 3
