from flask import render_template, request, redirect, url_for, abort  
from . import main  
from ..models import Comment, Pitch, User, Category 
from flask_login import login_required, current_user
from .. import db,photos
from .forms import CommentsForm, UpdateProfile, PitchForm, UpvoteForm
import markdown2



@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Home - Pitch your cause and take your first step in changing the world!'
    search_pitch= request.args.get('pitch_query')
    pitch= Pitch.get_all_pitches()  

    return render_template('index.html', title = title, pitch= pitch)

#this section consist of the category root functions
#  end of category root functions


@main.route('/environment/pitch/')
def environment():
    '''
    View root page function that returns the index page and its data
    '''
    pitch= Pitch.get_all_pitches()
    title = 'Home - pitch your cause, and get funded'  
    return render_template('environmental.html', title = title, pitch= pitch )

@main.route('/education/pitch/')
def education():
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Education causes'

    pitch= Pitch.get_all_pitches()

    return render_template('education.html', title = title, pitch= pitch )


@main.route('/health/pitch/')
def health():
    '''
    View root page function that returns the index page and its data
    '''
    title = 'health and wellness causes'
    pitch= Pitch.get_all_pitches()
    return render_template('health.html', title = title, pitch= pitch )

@main.route('/social-movements/pitch/')
def social_movement():
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Start a social movement'

    pitch= Pitch.get_all_pitches()

    return render_template('social-movements.html', title = title, pitch= pitch )
 
#  end of category root functions

@main.route('/pitch/<int:pitch_id>')
def pitch(pitch_id):

    '''
    View pitch page function that returns the pitch details page and its data
    '''
    found_pitch= get_pitch(pitch_id)
    title = pitch_id
    pitch_comments = Comment.get_comments(pitch_id)

    return render_template('pitch.html',title= title ,found_pitch= found_pitch, pitch_comments= pitch_comments)

@main.route('/search/<pitch_name>')
def search(pitch_name):
    '''
    View function to display the search results
    '''
    searched_pitches =search_pitch(pitch_name)
    title = f'search results for {pitch_name}'

    return render_template('search.html',pitch = searched_pitches)

@main.route('/pitch/new/', methods = ["GET","POST"])
@login_required
def new_pitch():
    '''
    Function that creates new pitch
    '''
    form = PitchForm()


    if category is None:
        abort( 404 )

    if form.validate_on_submit():
        pitch= form.content.data    
        category_id = form.category_id.data
        new_pitch= Pitch(pitch= pitch, category_id= category_id)

        new_pitch.save_pitch()
        return redirect(url_for('main.index'))

    return render_template('new_pitch.html', new_pitch_form= form, category= category)

@main.route('/category/<int:id>')
def category(id):
    '''
    function that returns pitch based on the entered category id
    '''
    category = Category.query.get(id)

    if category is None:
        abort(404)

    pitches_in_category = Pitch.get_pitch(id)
    return render_template('category.html' ,category= category, pitch= pitches_in_category)

@main.route('/pitch/comments/new/<int:id>',methods = ["GET","POST"])
@login_required
def new_comment(id):
    form = CommentsForm()
    vote_form = UpvoteForm()
    if form.validate_on_submit():
        new_comment = Comment(pitch_id =id,comment=form.comment.data,username=current_user.username,votes=form.vote.data)
        new_comment.save_comment()
        return redirect(url_for('main.index'))
    #title = f'{pitch_result.id} review'
    return render_template('new_comment.html',comment_form=form, vote_form= vote_form)

@main.route('/user/<uname>/update/pic',methods= ["POST"])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path 
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/user/<uname>/update',methods = ["GET","POST"])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))
    
    return render_template('profile/update.html',form =form)


@main.route('/view/comment/<int:id>')
def view_comments(id):
    '''
    Function that returs  the comments belonging to a particular pitch
    '''
    comments = Comment.get_comments(id)
    return render_template('view_comments.html',comments = comments, id=id)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)



