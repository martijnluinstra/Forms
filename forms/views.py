from flask import render_template, redirect, url_for, request
from flask.ext.wtf import Form
from forms import app, db
from models import Form
from form_models import generate_field, BaseForm

@app.route('/forms/<int:form_id>', methods=['GET'])
def render_form(form_id):
    form_data = Form.query.filter_by(id=form_id).first_or_404()

    class F(BaseForm):
        pass

    for field in form_data.fields.all():
        setattr(F, 'field'+str(field.id), generate_field(field))

    form = F(request.form)


    return render_template('form.html', form=form)
