from django.urls import path
from rest_framework.routers import DefaultRouter

from lms.apps import LmsConfig
from lms.views import (CourseViewSet, LessonCreateAPIView,
                       LessonDestroyAPIView, LessonListAPIView,
                       LessonRetrieveAPIView, LessonUpdateAPIView, SubscriptionAPIView)

app_name = LmsConfig.name

router = DefaultRouter()
router.register(r"course", CourseViewSet, basename="courses")

urlpatterns = [
                  path("lesson/", LessonListAPIView.as_view(), name="lesson-list"),
                  path("lesson/create/", LessonCreateAPIView.as_view(), name="lesson-create"),
                  path("lesson/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson-get"),
                  path("lesson/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="lesson-update"),
                  path("lesson/delete/<int:pk>/", LessonDestroyAPIView.as_view(), name="lesson-delete"),

                  path('subscription/', SubscriptionAPIView.as_view(), name='subscription'),
              ] + router.urls
