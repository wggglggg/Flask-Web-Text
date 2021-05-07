from app import app, db, bcrypt
from app.email import sent_token_to_email
from flask import render_template, flash, redirect, url_for, request
from app.models import User, Text, relationships
from app.forms import RegisterForm, LoginForm, ResetPasswordRequest, ResetPasswordForm, Texts, UploadFile
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, login_required, current_user
import click, os





@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
	title = 'This is in apppy give to base'
	form = Texts()
	if form.validate_on_submit():
		text = form.text.data
		post = Text(body=text)
		current_user.texts.append(post)
		print('current_user::::', current_user)
		db.session.commit()
		flash('发表成功', category='success')

	#len来计算粉丝与订阅别人有多少人
	count_fans = len(current_user.fans)
	count_subscribe = len(current_user.subscribe)
	page = request.args.get('page', 1, type=int) # 在网页url上取到？后面的page=多少， 默认是第1页，Int类型
	print('当前页是第几页:::', page)
	# posts = Text.query.order_by(Text.timestamp.desc()).all()
	posts = Text.query.order_by(Text.timestamp.desc()).paginate(page, 4, False)
	print('显示前面是第几页',posts.prev_num)
	print('显示后面是第几页',posts.next_num)
	#.all()查询时返回的是List， .paginate()返回的是对象
	#paginage第一个参数是在url上获取的第几页，也就是上面page拿到的值 ， 第二个参数一页上有几条信息， 第三个参数不满足4条一页时，不报错
	return render_template('index.html', title=title, form=form, posts=posts,count_fans=count_fans,count_subscribe=count_subscribe)

@app.route('/user_page/<username>', methods=['GET','POST'])
@login_required
def user_page(username):
	user = User.query.filter_by(username=username).first()
	if user:
		page = request.args.get('page', 1, type=int)
		posts = Text.query.filter_by(user_id=user.id).order_by(Text.timestamp.desc()).paginate(page, 4, False)
		return render_template('user_page.html',user=user, posts=posts)
	else:
		return '404'

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = UploadFile()
	if form.validate_on_submit():
		f = form.photo.data
		if f.filename == '':
			flash('No selected file', category='danger')
			return render_template('edit_profile.html', form=form)
		if f:#and allowed_file(f.filename):
			filename = secure_filename(f.filename)  # 上传的照片再处理, 提高文件安全性
			f.save(os.path.join(app.config['UPLOAD_FOLDER'],'app', 'static', 'assets', filename))
			current_user.avatar_img = '/static/assets/' + filename
			db.session.commit()
			return redirect(url_for('user_page', username=current_user.username))
	return render_template('edit_profile.html', form=form)

@app.route('/follow/<username>')
@login_required
def follow(username):
	user = User.query.filter_by(username=username).first()
	if user:
		current_user.to_subscrib(user)
		db.session.commit()
		page = request.args.get('page', 1, type=int)
		posts = Text.query.filter_by(user_id=user.id).order_by(Text.timestamp.desc()).paginate(page, 4, False)
		return render_template('user_page.html', user=user, posts=posts)



@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
	user = User.query.filter_by(username=username).first()
	if user:
		current_user.del_followers(user)
		db.session.commit()
		page = request.args.get('page', 1, type=int)
		posts = Text.query.filter_by(user_id=user.id).order_by(Text.timestamp.desc()).paginate(page, 4, False)
		return render_template('user_page.html', user=user, posts=posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegisterForm()
	if form.validate_on_submit():
		username = form.username.data
		password = bcrypt.generate_password_hash(form.password.data) #将用户密码hash一下, 保护用户敏感数据
		email = form.email.data
		user = User(username=username, password=password, email=email)
		db.session.add(user)
		db.session.commit()
		flash('注册成功', category='success')
		return redirect(url_for('login'))

	return render_template('register.html', form=form, )

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		username = form.username.data
		password = form.password.data
		remember = form.remember.data
		user = User.query.filter_by(username=username).first()
		if user and bcrypt.check_password_hash(user.password, password):
			# print(user,bcrypt.check_password_hash(user.password, password))
			# 不明确提示到底是用户或者是密码错误,用 and 提高用户敏感数据安全性
			login_user(user, remember=remember)
			flash('登陆成功', category='success')
			if request.args.get('next'):
				next_page = request.args.get('next')
				return redirect(next_page)
			return redirect(url_for('index'))

		else:
			flash('输入的用户名或者密码错误', category='danger')

	return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))


@app.route('/coffee')
@login_required
def coffee():
	title = 'This is coffee'
	return render_template('coffee.html', title=title)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = ResetPasswordRequest()
	if form.validate_on_submit():
		email = form.email.data
		user = User.query.filter_by(email=email).first()
		token = user.generate_reset_password_token()
		sent_token_to_email(user, token)
		flash('重置链接已发往邮箱,请去邮箱获取重置链接', category='info')
	return render_template('reset_password_request.html', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		print(token)
		user = User.check_reset_password_token(token)
		print('form.password.data:=====', form.password.data)
		if user:
			user.password = bcrypt.generate_password_hash(form.password.data)
			print('user--->', user.password)
			db.session.commit()
			flash('密码更改成功,请用新密码登陆', category='info')
			redirect(url_for('login'))
		else:
			flash('用户不存在', category='info')
			redirect(url_for('login'))
	return render_template('reset_password.html',form=form)




@app.cli.command()
def hello():
	click.echo('This is click command')