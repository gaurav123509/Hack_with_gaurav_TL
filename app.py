import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from models import db, User, Skill, Swap, Rating, AdminLog
from config import Config
from forms import RegistrationForm, LoginForm, ProfileForm, SwapRequestForm, RatingForm

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Setup Login Manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def save_uploaded_file(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(f"{current_user.id}_{file.filename}")
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return filename
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if query:
        skills = Skill.query.filter(Skill.name.ilike(f'%{query}%')).all()
        user_ids = {skill.user_id for skill in skills}
        users = User.query.filter(User.id.in_(user_ids), User.is_public==True, User.is_banned==False).all()
    else:
        users = User.query.filter_by(is_public=True, is_banned=False).all()
    return render_template('search.html', users=users, query=query)

@app.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user.is_banned:
        flash('This account has been banned', 'danger')
        return redirect(url_for('index'))
    return render_template('profile.html', user=user)

@app.route('/swap/request/<int:user_id>', methods=['GET', 'POST'])
@login_required
def request_swap(user_id):
    receiver = User.query.get_or_404(user_id)
    form = SwapRequestForm()
    
    if form.validate_on_submit():
        swap = Swap(
            sender_id=current_user.id,
            receiver_id=user_id,
            offered_skill=form.offered_skill.data,
            requested_skill=form.requested_skill.data
        )
        db.session.add(swap)
        db.session.commit()
        flash('Swap request sent successfully!', 'success')
        return redirect(url_for('profile', username=receiver.username))
    
    return render_template('swap_request.html', form=form, receiver=receiver)

@app.route('/swaps')
@login_required
def swap_requests():
    pending_received = Swap.query.filter_by(receiver_id=current_user.id, status='pending').all()
    pending_sent = Swap.query.filter_by(sender_id=current_user.id, status='pending').all()
    accepted = Swap.query.filter(
        ((Swap.sender_id == current_user.id) | (Swap.receiver_id == current_user.id)) &
        (Swap.status == 'accepted')
    ).all()
    return render_template('swap_requests.html', 
                         pending_received=pending_received,
                         pending_sent=pending_sent,
                         accepted=accepted)

@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied', 'danger')
        return redirect(url_for('index'))
    
    users = User.query.all()
    swaps = Swap.query.all()
    return render_template('admin_dashboard.html', users=users, swaps=swaps)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)