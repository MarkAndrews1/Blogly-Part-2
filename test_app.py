from unittest import TestCase
from app import app
from models import db, USER

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False


class AppTest(TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_add_user(self):
        with app.test_client() as client:
            res = client.post('users/new', data={
                'first-name': 'John',
                'last-name': 'doe',
                'img-url': 'https://img.freepik.com/premium-vector/empty-face-icon-avatar-with-black-hair-vector-illustration_601298-13402.jpg?w=2000'
            })
        self.assertEqual(res.status_code, 302)
    
    def test_404_status(self):
        with app.test_client() as client:
            res = client.get('/users/234')
            self.assertEqual(res.status_code, 404)

    def test_edit_user(self):
        user = USER(first_name='John', last_name='Doe', img_url='https://img.freepik.com/premium-vector/empty-face-icon-avatar-with-black-hair-vector-illustration_601298-13402.jpg?w=2000')
        db.session.add(user)
        db.session.commit()

        with app.test_client() as client:
            res = client.post(f"/users/{user.id}/edit", data={
                'first-name': 'Jason',
                'last-name': 'Andrews',
                'img-url': 'https://img.freepik.com/premium-vector/empty-face-icon-avatar-with-black-hair-vector-illustration_601298-13402.jpg?w=2000'
            })
        self.assertEqual(res.status_code, 302)

    def test_delete_user(self):
        user = USER(first_name='John', last_name='Doe', img_url='https://img.freepik.com/premium-vector/empty-face-icon-avatar-with-black-hair-vector-illustration_601298-13402.jpg?w=2000')
        db.session.add(user)
        db.session.commit()

        with app.test_client() as client:
            res = client.delete(f"/users/{user.id}/delete")
        self.assertEqual(res.status_code, 302)