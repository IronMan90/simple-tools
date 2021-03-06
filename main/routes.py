import random
import string
import os
import glob
import datetime
import pyperclip
import faker
from flask import render_template, url_for, redirect, send_file, request, flash
from main import app
from main.forms import UsersForm, VcfForm, SerialsForm

fake = faker.Faker()
local_user = ''
date_time = datetime.datetime.today().strftime("%M-%S-%f")


class Results:
    def __init__(self, users_, vcf_, serials_):
        self.users = users_
        self.vcf_ = vcf_
        self.serials_ = serials_

    def get_users(self):
        return self.users

    def set_users(self, users_):
        self.users = users_

    def get_vcf(self):
        return self.vcf_

    def set_vcf(self, vcf_):
        self.vcf_ = vcf_

    def get_serials(self):
        return self.serials_

    def set_serials(self, serials_):
        self.serials_ = serials_


p = Results('', '', '')
faker = faker.Faker(['it_IT', 'en_US', 'ja_JP'])


def save_to_file(function, filename, extension="csv"):
    os.remove(os.getcwd() + '/' + os.path.join('main/static') + '/' + filename + '.' + extension)
    with open(os.getcwd() + '/' + os.path.join('main/static') + '/' + filename + '.' + extension, 'w',
              encoding="utf-8") as file:
        file.write(f'{function}')
        file.close()


def generate_full_name():
    return fake.name()


def randstr():
    randomstr = ''
    for i in range(0, 10):
        randomstr += random.choice(string.ascii_uppercase)
    return randomstr


def generate_local_users(number, domain='example.com'):
    local_users = ''
    for i in range(0, number):
        fullname = generate_full_name()
        names = fullname.split(' ')
        email = f'{names[0].lower()}.{names[1].lower()}@{domain}'
        nickname = f'{names[0][0].lower()}{names[1].lower()}'
        local_users += email + ';' + names[0] + ';' + names[1] + ';' + nickname + '\n'
    p.set_users(local_users)
    return local_users[:-1]


def generate_vcf(number):
    contacts = ''
    for i in range(0, number):
        fullname = faker.name().split(' ')
        address = faker.address().split(',')[0]
        contacts += f'BEGIN:VCARD\n' \
            f'N:{fullname[1]};{fullname[0]}\n' \
            f'FN:{fullname[0]} {fullname[1]}\n' \
            f'ORG:{randstr()}\n' \
            f'ADR;TYPE=WORK:{address}\n' \
            f'TEL;TYPE=WORK,MSG:{random.randint(10 ** 6, 10 ** 7)}\n' \
            f'EMAIL;TYPE=INTERNET:{fullname[1].lower()}@example.com\n' \
            f'END:VCARD\n'
    p.set_vcf(contacts)
    return contacts


def generate_devices_serial_number(number):
    serials = ''
    for i in range(0, number):
        r = random.randrange(1, 1000)
        serials += f'{randstr()[1:3]}{r // 2}{randstr()[4:7]}{r}-example\n'
    p.set_serials(serials)
    return serials[:-1]


@app.route('/users_copy_to_clipboard')
def users_copy_to_clipboard():
    pyperclip.copy(p.get_users())
    return redirect(url_for('results'))


@app.route('/users_save_file')
def users_save_file():
    save_to_file(p.get_users(), "users")
    return redirect(url_for('results'))


@app.route('/serials_copy_to_clipboard')
def serials_copy_to_clipboard():
    pyperclip.copy(p.get_serials())
    return redirect(url_for('results'))


@app.route('/serials_save_file')
def serials_save_file():
    save_to_file(p.get_serials(), "serials")
    return redirect(url_for('results'))


@app.route('/contacts_copy_to_clipboard')
def contacts_copy_to_clipboard():
    pyperclip.copy(p.get_vcf())
    return redirect(url_for('results'))


@app.route('/contacts_save_file')
def contacts_save_file():
    save_to_file(p.get_vcf(), "contacts", 'vcf')
    return redirect(url_for('results'))


@app.route('/')
def home():
    form = UsersForm()
    vcf_form = VcfForm()
    serials_form = SerialsForm()
    return render_template('home.html', form=form, vcf_form=vcf_form, serials_form=serials_form)


@app.route('/results', methods=['GET', 'POST'])
def results():
    t = p.get_users()
    result_vcf = p.get_vcf()
    result_serials = p.get_serials()
    return render_template('users.html', t=t, result_vcf=result_vcf, result_serials=result_serials)


@app.route('/generate_users', methods=['GET', 'POST'])
def user():
    form = UsersForm()
    if form.validate_on_submit():
        generate_local_users(form.count.data, form.email.data)
        return redirect(url_for('results'))
    return render_template('home.html', form=form)


@app.route('/generate_vcf', methods=['GET', 'POST'])
def vcf():
    vcf_form = VcfForm()
    if vcf_form.validate_on_submit():
        generate_vcf(vcf_form.count.data)
        return redirect(url_for('results'))
    return render_template('home.html', vcf_form=vcf_form)


@app.route('/generate_serials', methods=['GET', 'POST'])
def serials():
    serials_form = SerialsForm()
    if serials_form.validate_on_submit():
        generate_devices_serial_number(serials_form.count.data)
        return redirect(url_for('results'))
    return render_template('home.html', serials_form=serials_form)
