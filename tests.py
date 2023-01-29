from unittest import TestCase
from flask import url_for, request
from models import db, User, Post, Tags, PostTags
from app import app
from sqlalchemy.exc import IntegrityError
import time

app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True


db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    """Test User model"""
    def setUp(self):
        """Clear existing users"""
        PostTags.query.delete()
        Post.query.delete()
        User.query.delete()
        Tags.query.delete()

    def tearDown(self):
        """Clear bad transactions"""
        db.session.rollback()

    def test_def_pfp(self):
        print('*************************************************************************')

        user = User(first_name='First', last_name='Last')
        db.session.add(user)
        db.session.commit()

        self.assertEquals(user.profile_pic, 'https://twirpz.files.wordpress.com/2015/06/twitter-avi-gender-balanced-figure.png?w=640')

class TagsModelTestCase(TestCase):
    """Test Tags Model"""
    def setUp(self):
        """Clear existing tags"""
        PostTags.query.delete()
        Post.query.delete()
        User.query.delete()
        Tags.query.delete()

    def tearDown(self):
        """Clear bad transactions"""
        db.session.rollback()

    def test_unique_tags(self):
        print('*************************************************************************')
        print('*************************************************************************')

        tag1 = Tags(name='Tag')
        tag2 = Tags(name='Tag')
        db.session.add_all([tag1, tag2])

        with self.assertRaises(IntegrityError):
            db.session.commit()

class HomepageTestCase(TestCase):
    """Test homepage display"""
    def setUp(self):
        """Clear tables"""
        User.query.delete()
        Post.query.delete()
        Tags.query.delete()
        PostTags.query.delete()

        """Create a user"""
        user = User(first_name='First', last_name='Last')

        db.session.add(user)
        db.session.commit()

        """Create posts from that user to display on homepage"""
        post1 = Post(title='Oldest Post', content='This is the oldest post', posted_by=user.id)
        post2 = Post(title='Older Post', content='This is the second post', posted_by=user.id)
        post3 = Post(title='Middle Post', content='This is the Third post', posted_by=user.id)
        post4 = Post(title='New Post', content='This is the Fourth post', posted_by=user.id)
        post5 = Post(title='Newer Post', content='This is the Fifth post', posted_by=user.id)
        post6 = Post(title='Newest Post', content='This is the Sixth post', posted_by=user.id)

        db.session.add_all([post1, post2, post3, post4, post5, post6])
        db.session.commit()

        """Create tags for the posts"""
        tag1 = Tags(name='Tag1')
        tag2 = Tags(name='Tag2')
        tag3 = Tags(name='Tag3')
        tag4 = Tags(name='Tag4')
        tag5 = Tags(name='Tag5')
        tag6 = Tags(name='Tag6')

        db.session.add_all([tag1, tag2, tag3, tag4, tag5, tag6])
        db.session.commit()

        """Link tags to posts"""
        pt1 = PostTags(post_id=post1.id, tag_id=tag1.id)
        pt2 = PostTags(post_id=post1.id, tag_id=tag2.id)
        pt3 = PostTags(post_id=post2.id, tag_id=tag3.id)
        pt4 = PostTags(post_id=post2.id, tag_id=tag4.id)
        pt5 = PostTags(post_id=post3.id, tag_id=tag5.id)
        pt6 = PostTags(post_id=post4.id, tag_id=tag6.id)
        pt7 = PostTags(post_id=post4.id, tag_id=tag5.id)        
        pt8 = PostTags(post_id=post4.id, tag_id=tag4.id)
        pt9 = PostTags(post_id=post5.id, tag_id=tag3.id)
        pt10 = PostTags(post_id=post6.id, tag_id=tag2.id)

        db.session.add_all([pt1, pt2, pt3, pt4, pt5, pt6, pt7, pt8, pt9, pt10])
        db.session.commit()

    def tearDown(self):
        """Clear bad transactions"""
        db.session.rollback()

    def test_homepage(self):
        print('*************************************************************************')
        print('*************************************************************************')
        print('*************************************************************************')

        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            """Test that post titles for 5 most recent posts are displayed"""
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Newest Post', html)
            self.assertIn('Newer Post', html)
            self.assertIn('New Post', html)
            self.assertIn('Middle Post', html)
            self.assertIn('Older Post', html)
            self.assertNotIn('Oldest Post', html)

            """That post tag names are displayed on homepage"""
            self.assertIn('Tag2', html)
            self.assertIn('Tag3', html)
            self.assertIn('Tag4', html)
            self.assertIn('Tag5', html)
            self.assertIn('Tag6', html)




class EditTagTestCase(TestCase):
    """Test homepage display"""
    def setUp(self):
        """Clear tables"""
        Post.query.delete()
        User.query.delete()
        Tags.query.delete()
        PostTags.query.delete()

    def tearDown(self):
        """Clear bad transactions"""
        db.session.rollback()

    def test_submit_edit_tag(self):
        print('*************************************************************************')
        print('*************************************************************************')
        print('*************************************************************************')
        print('*************************************************************************')

        """Create tags to edit"""
        tag = Tags(name='Edit_Me')
        db.session.add(tag)
        db.session.commit()

        tag_id = tag.id

        with app.test_client() as client:
            """Check that initial tag name is displayed on tag page"""
            init = client.get(f'/tags/{ tag_id }')
            init_html = init.get_data(as_text=True)

            self.assertEqual(init.status_code, 200)
            self.assertIn('Edit_Me', init_html)
            self.assertNotIn('Edited', init_html)

            """Submit edit tag form and follow redirect"""
            post = client.post(f'/tags/{ tag_id }/edit', data={'tag_name': 'Edited'}) 

            """Test that newly edited tag name is displayed on tag page"""
            resp = client.get(f'/tags/{ tag_id }')
            html = resp.get_data(as_text=True) 

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Edit_Me', html)
            self.assertIn('Edited', html)


class EditPostTestCase(TestCase):
    """Test homepage display"""
    def setUp(self):
        """Clear tables"""
        PostTags.query.delete()
        User.query.delete()
        Post.query.delete()
        Tags.query.delete()

    def tearDown(self):
        """Clear bad transactions"""
        db.session.rollback()

    def test_submit_edit_post(self):
        print('*************************************************************************')
        print('*************************************************************************')
        print('*************************************************************************')
        print('*************************************************************************')
        print('*************************************************************************')

        """Create user to make post"""
        user = User(first_name='First', last_name='Last')
        db.session.add(user)
        db.session.commit()

        """Create post to edit"""
        post = Post(title='Edit Me', content='I am not edited', posted_by=user.id)
        db.session.add(post)
        db.session.commit()

        post_id = post.id

        with app.test_client() as client:
            """Check that initial tag name is displayed on tag page"""
            init = client.get(f'/posts/{ post_id }')
            init_html = init.get_data(as_text=True)

            self.assertEqual(init.status_code, 200)
            self.assertIn('Edit Me', init_html)
            self.assertNotIn('Edited', init_html)

            """Submit edit tag form and follow redirect"""
            post = client.post(f'/posts/{ post_id }/edit', data={'edit_post_title': 'Edited', 
                                                                 'edit_post_content': 'I am edited'})

            """Test that newly edited tag name is displayed on tag page"""
            resp = client.get(f'/posts/{ post_id }')
            html = resp.get_data(as_text=True)  

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Edit Me', html)
            self.assertIn('Edited', html)


class EditUserTestCase(TestCase):
    """Test homepage display"""
    def setUp(self):
        """Clear tables"""
        PostTags.query.delete()
        User.query.delete()
        Post.query.delete()
        Tags.query.delete()

    def tearDown(self):
        """Clear bad transactions"""
        db.session.rollback()

    def test_submit_edit_user(self):
        print('*************************************************************************')
        print('*************************************************************************')
        print('*************************************************************************')
        print('*************************************************************************')
        print('*************************************************************************')
        print('*************************************************************************')

        """Create user to make post"""
        user = User(first_name='First', last_name='Last')
        db.session.add(user)
        db.session.commit()

        user_id = user.id

        with app.test_client() as client:
            """Check that initial tag name is displayed on tag page"""
            init = client.get(f'/users/{ user_id }')
            init_html = init.get_data(as_text=True)

            self.assertEqual(init.status_code, 200)
            self.assertIn('First', init_html)
            self.assertIn('Last', init_html)
            self.assertNotIn('EditedName', init_html)
            self.assertNotIn('UserName', init_html)

            """Submit edit tag form and follow redirect"""
            post = client.post(f'/users/{ user_id }/edit', data={'first_name': 'EditedName', 
                                                                 'last_name': 'UserName', 
                                                                 'profile_pic': 'https://twirpz.files.wordpress.com/2015/06/twitter-avi-gender-balanced-figure.png?w=640'})

            """Test that newly edited tag name is displayed on tag page"""
            resp = client.get(f'/users/{ user_id }')
            html = resp.get_data(as_text=True)  

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('First', html)
            self.assertNotIn('Last', html)
            self.assertIn('EditedName', html)
            self.assertIn('UserName', html)