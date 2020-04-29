import faker
from flask import render_template, url_for, redirect
from main import app
from main.forms import UsersForm, VcfForm, SerialsForm

fake = faker.Faker()
local_user = ''


class Results:
    def __init__(self, test):
        self.test = test

    def get_test(self):
        return self.test

    def set_test(self, test):
        self.test = test


p = Results('')


def generate_full_name():
    return fake.name()


def generate_local_users(t):
    local_users = ''
    for i in range(0, t):
        fullname = generate_full_name()
        names = fullname.split(' ')
        email = f'{names[0].lower()}.{names[1].lower()}@proget.pl'
        nickname = f'{names[0][0].lower()}{names[1].lower()}'
        local_users += email + ';' + names[0] + ';' + names[1] + ';' + nickname + '\n'
    local_user = local_users
    p.set_test(local_user)
    return local_users[:-1]


@app.route('/')
def home():
    form = UsersForm()
    vcf_form = VcfForm()
    serials_form = SerialsForm()
    return render_template('home.html', form=form, vcf_form=vcf_form, serials_form=serials_form)


@app.route('/results')
def results():
    t = p.get_test()
    return render_template('users.html', t=t)


@app.route('/generate_users', methods=['GET', 'POST'])
def user():
    form = UsersForm()
    if form.validate_on_submit():
        generate_local_users(form.count.data)
        return redirect(url_for('results'))
    return render_template('home.html', form=form)


@app.route('/generate_vcf', methods=['GET', 'POST'])
def vcf():
    vcf_form = VcfForm()
    if vcf_form.validate_on_submit():
        print(vcf_form.count.data)
        return redirect(url_for('home'))
    return render_template('home.html', vcf_form=vcf_form)


@app.route('/generate_serials', methods=['GET', 'POST'])
def serials():
    serials_form = SerialsForm()
    if serials_form.validate_on_submit():
        print(serials_form.count.data)
        return redirect(url_for('home'))
    return render_template('home.html', serials_form=serials_form)
