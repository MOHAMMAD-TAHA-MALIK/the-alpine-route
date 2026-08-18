from django.test import TestCase

# Create your tests here.
from datetime import date, timedelta
from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Trek, TrekEvent, Comment, UserProfile
from .forms import TrekForm, TrekEventForm
from . import views


class TrekModelTest(TestCase):
    """Tests for the Trek model and custom properties/methods."""

    def setUp(self):
        self.guide = User.objects.create_user(username='guide_user', password='password123', is_staff=True)
        self.user1 = User.objects.create_user(username='hiker1', password='password123')
        self.user2 = User.objects.create_user(username='hiker2', password='password123')

        self.trek = Trek.objects.create(
            title="Alpine Peak Challenge",
            destination="Matterhorn",
            date=date.today() + timedelta(days=10),
            difficulty="hard",
            created_by=self.guide,
            max_participants=2
        )

    def test_trek_creation_and_str(self):
        self.assertEqual(str(self.trek), f"Alpine Peak Challenge ({self.trek.date})")
        self.assertEqual(self.trek.max_participants, 2)
        self.assertFalse(self.trek.is_full)

    def test_trek_is_full_property(self):
        self.trek.participants.add(self.user1)
        self.assertFalse(self.trek.is_full)

        self.trek.participants.add(self.user2)
        self.assertTrue(self.trek.is_full)


class TrekEventModelTest(TestCase):
    """Tests for the TrekEvent model and helper methods."""

    def setUp(self):
        self.user = User.objects.create_user(username='event_liker', password='password123')
        self.past_event = TrekEvent.objects.create(
            title="Past Summit",
            description="Historical hike",
            date=timezone.now().date() - timedelta(days=5),
            location="High Peak"
        )
        self.future_event = TrekEvent.objects.create(
            title="Future Expedition",
            description="Upcoming climb",
            date=timezone.now().date() + timedelta(days=5),
            location="Ridge Line"
        )

    def test_is_past_method(self):
        self.assertTrue(self.past_event.is_past())
        self.assertFalse(self.future_event.is_past())

    def test_total_likes(self):
        self.assertEqual(self.future_event.total_likes(), 0)
        self.future_event.likes.add(self.user)
        self.assertEqual(self.future_event.total_likes(), 1)


class UserProfileSignalTest(TestCase):
    """Tests that UserProfile is automatically created via post_save signals."""

    def test_profile_creation_on_user_save(self):
        user = User.objects.create_user(username='new_hiker', password='password123')
        self.assertTrue(UserProfile.objects.filter(user=user).exists())
        self.assertEqual(str(user.profile), "new_hiker's Profile")


class TrekFormsTest(TestCase):
    """Tests for Trek and TrekEvent forms."""

    def test_trek_form_valid(self):
        form_data = {
            'title': 'Forest Hike',
            'destination': 'Greenwood',
            'date': date.today() + timedelta(days=3),
            'difficulty': 'easy'
        }
        form = TrekForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_trek_event_form_valid(self):
        form_data = {
            'title': 'Sunset Walk',
            'description': 'Relaxing evening trail.',
            'date': date.today(),
            'location': 'Meadow Overlook'
        }
        form = TrekEventForm(data=form_data)
        self.assertTrue(form.is_valid())


class TrekUrlsTest(TestCase):
    """Tests for URL routing and view function resolution."""

    def test_urls_resolve_to_correct_views(self):
        self.assertEqual(resolve(reverse('trek_list')).func, views.trek_list)
        self.assertEqual(resolve(reverse('upcoming_treks')).func, views.upcoming_treks)
        self.assertEqual(resolve(reverse('previous_treks')).func, views.previous_treks)
        self.assertEqual(resolve(reverse('create_trek')).func, views.create_trek)


class TrekViewsTest(TestCase):
    """Tests for HTTP views, authentication permissions, and state changes."""

    def setUp(self):
        self.client = Client()
        self.guide = User.objects.create_user(username='guide', password='password123', is_staff=True)
        self.user = User.objects.create_user(username='regular_user', password='password123')

        self.trek = Trek.objects.create(
            title="Basecamp Trek",
            destination="Everest Base",
            date=date.today() + timedelta(days=15),
            difficulty="hard",
            created_by=self.guide,
            max_participants=1
        )
        self.event = TrekEvent.objects.create(
            title="Community Meetup",
            description="Discussing equipment.",
            date=date.today(),
            location="Clubhouse"
        )

    # --- Auth & Profile ---

    def test_register_view(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('signup'), {
            'username': 'newuser123',
            'password1': 'StrongPassword123!',
            'password2': 'StrongPassword123!'
        })
        self.assertRedirects(response, reverse('trek_list'))
        self.assertTrue(User.objects.filter(username='newuser123').exists())

    def test_profile_view_authenticated(self):
        self.client.login(username='regular_user', password='password123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    # --- Guide Authorization Checks ---

    def test_create_trek_guide_only(self):
        # Unauthenticated user redirected to login
        response = self.client.get(reverse('create_trek'))
        self.assertRedirects(response, f"/login/?next={reverse('create_trek')}")

        # Regular non-staff user forbidden/redirected by user_passes_test
        self.client.login(username='regular_user', password='password123')
        response = self.client.get(reverse('create_trek'))
        self.assertNotEqual(response.status_code, 200)

        # Staff/Guide user allowed access
        self.client.login(username='guide', password='password123')
        response = self.client.get(reverse('create_trek'))
        self.assertEqual(response.status_code, 200)

    # --- Participation Actions ---

    def test_join_and_leave_trek(self):
        self.client.login(username='regular_user', password='password123')

        # Join Trek
        response = self.client.post(reverse('join_trek', kwargs={'pk': self.trek.pk}))
        self.assertRedirects(response, reverse('trek_list'))
        self.assertIn(self.user, self.trek.participants.all())

        # Attempt to join full trek with another user
        user2 = User.objects.create_user(username='user2', password='password123')
        self.client.login(username='user2', password='password123')
        self.client.post(reverse('join_trek', kwargs={'pk': self.trek.pk}))
        self.assertNotIn(user2, self.trek.participants.all())

        # Leave Trek
        self.client.login(username='regular_user', password='password123')
        response = self.client.post(reverse('leave_trek', kwargs={'pk': self.trek.pk}))
        self.assertRedirects(response, reverse('trek_list'))
        self.assertNotIn(self.user, self.trek.participants.all())

    # --- Social Interactions ---

    def test_like_event_toggle(self):
        self.client.login(username='regular_user', password='password123')
        
        # Like event
        self.client.post(reverse('like_event', kwargs={'pk': self.event.pk}))
        self.assertEqual(self.event.likes.count(), 1)

        # Unlike event
        self.client.post(reverse('like_event', kwargs={'pk': self.event.pk}))
        self.assertEqual(self.event.likes.count(), 0)

    def test_add_comment(self):
        self.client.login(username='regular_user', password='password123')
        response = self.client.post(
            reverse('add_comment', kwargs={'pk': self.event.pk}),
            {'content': 'Looking forward to this event!'}
        )
        self.assertRedirects(response, reverse('trek_detail', kwargs={'pk': self.event.pk}))
        self.assertEqual(Comment.objects.filter(trek=self.event).count(), 1)