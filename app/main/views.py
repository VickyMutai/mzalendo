from flask import render_template, request, redirect, url_for,abort
from . import main
from .forms import ReportForm, CommentForm
from ..models import Reports, Comments,Community
from flask_login import login_required, current_user
from .. import db, photos
from ..email import mail_message

@main.route('/')
def index():
    """
    This function renders out home page and all its data
    """
    test = "Working"
    reports = Reports.query.all()
    return render_template('index.html', reports=reports, test=test)


@main.route('/reportForm', methods=['GET', 'POST'])
def reportForm():
    report_form = ReportForm()
    community = Community.query.all()

    if report_form.validate_on_submit():
        location = report_form.location.data
        institution = report_form.institution.data
        department = report_form.department.data
        category = report_form.category.data
        title = report_form.title.data
        description = report_form.description.data
        if 'photo' in request.files:
            filename = photos.save(request.files['photo'])
            path = f'photos/{filename}'
            report.pic_path = path
            db.session.commit()
            new_report = Reports(location=location,
                                 institution=institution,
                                 department=department,
                                 category=category,
                                 title=title,
                                 description=description)
            db.session.add(new_report)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            new_report = Reports(location=location,
                                 institution=institution,
                                 department=department,
                                 category=category,
                                 title=title,
                                 description=description)
        db.session.add(new_report)
        db.session.commit()
        for person in community:
            mail_message("New Report!","email/new_report",person.email)
        return redirect(url_for('main.index'))

    return render_template('reportForm.html', report_form=report_form)


@main.route('/reports')
@login_required
def report():
    # TODO: Add voting to this new page. So that comm members can vote.
    reports = Reports.query.all()

    #return redirect(url_for('main.report'))

    return render_template('reports.html',reports=reports)


@main.route('/report/<int:id>', methods=['POST'])
@login_required
def update_report(id):
    report = Reports.query.filter_by(id).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        report.pic_path = path
        db.session.commit()
    return redirect(url_for('main.new'))

# view single report
@main.route('/report/<int:id>')
@login_required
def view_report(id):
    form = ReportForm()
    member = Community.query.filter_by(id=id).first()
    report = Reports.query.filter_by(id=id).first()

    comments =  Comments.get_comments(id)

    title = 'Uzalendo'
    return render_template('reportReview.html',comments=comments,
                                               title=title,report=report,
                                               report_form=form,user=current_user)

@main.route('/comment/new/<int:id>', methods=['GET','POST'])
@login_required
def comments(id):
    report = Reports.query.filter_by(id=id).first()
    comment_form = CommentForm()

    if comment_form.validate_on_submit():
        comment = comment_form.comment.data
        verified = comment_form.verified.data
        new_comment = Comments(comment=comment,verified=verified,user=current_user)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('main.view_report',id=report.id))

    title = 'Uzalendo'
    return render_template('comments.html',title=title,
                                           report=report,
                                           comment_form=comment_form)
