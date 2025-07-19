"""
URL configuration for server_portfolio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from portfolio.Views.GitProdject.views import (
    get_git_projects,
    create_git_project,
    get_single_git_project,
    update_git_project,
    delete_git_project,
    get_token_secret,
    SkillsCreate,
    remove_images,
)
from portfolio.Views.others.views import (
    education_create,
    experience_create,
    softSkill,
)

# from ..portfolio.Views.User.views import ( AuthCreateNewUserView, AuthLoginExistingUserView)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("git-projects", get_git_projects, name="get_git_projects"),
    path("git-projects/create", create_git_project, name="create_git_project"),
    path(
        "git-projects/<str:project_id>",
        get_single_git_project,
        name="get_single_git_project",
    ),
    path(
        "git-projects/patch/<str:project_id>",
        update_git_project,
        name="update_git_project",
    ),
    path(
        "git-projects/delete/<str:project_id>",
        delete_git_project,
        name="delete_git_project",
    ),
    path("git-projects/secret/", get_token_secret, name="get_token_secret"),
    path(
        "git-projects/remove-images/<str:project_id>",
        remove_images,
        name="remove_images",
    ),
    path("skills", SkillsCreate, name="skills_create"),
    path("education", education_create, name="education_create"),
    path("experience", experience_create, name="experience_create"),
    path("soft-skill", softSkill, name="soft_skill_create"),
]
