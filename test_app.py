import pytest
from app import app, db, Post # app 외에 db와 Post 모델도 가져옵니다.

@pytest.fixture
def client():
    # --- 테스트를 위한 설정 ---
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # 실제 DB가 아닌 메모리 DB 사용
    app.config['WTF_CSRF_ENABLED'] = False  # 테스트 시에는 CSRF 보호를 비활성화하는 것이 편리합니다.

    # 테스트 클라이언트 생성
    client = app.test_client()

    # --- 테스트 데이터베이스 설정 ---
    with app.app_context():
        db.create_all() # 테스트용 DB 테이블 생성

    yield client # 테스트 실행

    # --- 테스트 종료 후 정리 ---
    with app.app_context():
        db.drop_all() # 사용한 테스트 DB 테이블 삭제


def test_index_page_loads(client):
    """
    1. GET /: 홈페이지가 정상적으로 로드되는지 테스트합니다.
    """
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'Guestbook' in resp.data # 페이지 제목에 'Guestbook'이 있는지 확인 (템플릿에 따라 수정)
    assert b'name' in resp.data       # 폼에 '이름' 필드가 있는지 확인


def test_post_submission(client):
    """
    2. POST /: 방명록에 글을 작성하고, 작성된 글이 보이는지 테스트합니다.
    """
    # 'follow_redirects=True'는 POST 후 리다이렉트 되는 페이지까지 따라가라는 의미입니다.
    resp = client.post('/', data={
        'author': 'tester',
        'content': '이것은 테스트 게시물입니다.'
    }, follow_redirects=True)

    # 요청이 성공적으로 처리되었는지 확인
    assert resp.status_code == 200

    # 먼저 utf-8로 인코딩
    html = resp.data.decode('utf-8')
    # 게시물이 페이지에 잘 나타나는지 확인
    assert 'tester' in html
    assert '이것은 테스트 게시물입니다.' in html


def test_database_entry(client):
    """
    3. POST /: 글 작성 후 실제 데이터베이스에 데이터가 저장되었는지 확인합니다.
    """
    client.post('/', data={
        'author': 'DB 테스터',
        'content': '데이터베이스 저장 테스트'
    })

    # with app.app_context()를 통해 앱 컨텍스트 안에서 DB에 접근합니다.
    with app.app_context():
        # Post 테이블에 데이터가 1개 있는지 확인
        assert Post.query.count() == 1
        # 저장된 데이터의 내용이 올바른지 확인
        entry = Post.query.first()
        assert entry.author == 'DB 테스터'