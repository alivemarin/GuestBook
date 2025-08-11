import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from forms import PostForm
from models import db, Post

app = Flask(__name__)

# --- 보안 설정 및 구성 ---
# 실제 운영 환경에서는 환경 변수나 별도의 설정 파일을 사용해야 합니다.
# Secret Scanning 테스트를 위해 일부러 하드코딩된 예시입니다.
app.config['SECRET_KEY'] = 'a_very_secret_key_for_csrf_and_sessions' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///guestbook.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# CSRF 보호 초기화
csrf = CSRFProtect(app)

# 데이터베이스 초기화
db.init_app(app)

# 애플리케이션 컨텍스트 내에서 데이터베이스 테이블 생성
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    # --- SAST/DAST 테스트 포인트 (사용자 입력 처리) ---
    # form.validate_on_submit()을 통해 기본적인 입력 검증(e.g., CSRF)이 이루어집니다.
    # 하지만 저장되는 데이터에 대한 XSS 방어는 추가적인 처리가 필요할 수 있습니다.
    if form.validate_on_submit():
        author = form.author.data
        content = form.content.data
        
        # 새로운 Post 객체 생성 및 DB 저장
        new_post = Post(author=author, content=content)
        db.session.add(new_post)
        db.session.commit()
        
        return redirect(url_for('index'))

    # 모든 게시글을 최신순으로 조회
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', posts=posts, form=form)

if __name__ == '__main__':
    # host='0.0.0.0'는 컨테이너 환경에서 외부 접근을 허용하기 위해 필요합니다.
    app.run(host='0.0.0.0', port=5000, debug=True)