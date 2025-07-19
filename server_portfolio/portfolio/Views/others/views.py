from portfolio.utils.Firebase.database import auth, database
from portfolio.utils.Firebase.token import token
from portfolio.utils.Firebase.uploadImage import upload_helper, delete_image_helper
from portfolio.utils.Date.serializeDate import serialize_datetime
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from decouple import config as env_config
from portfolio.utils.Encrypt.encryption import EncryptToken, DecryptToken
from django.template.loader import render_to_string
import datetime
import json


@csrf_exempt
@api_view(["GET", "POST"])
def education_create(request):
    if request.method == "GET":
        dataEdu = []
        getEdu = database.child("Education").get(token).val()
        
        if not getEdu:
            return JsonResponse({"message": " Skills not Found"}, status=404)
        
        for education_id, education in getEdu.items():
            dataEdu.append(education)

        return JsonResponse(dataEdu, safe=False)

    elif request.method == "POST":
        body = request.data

        if not body:
            return JsonResponse({"message": "No data provided"}, status=400)

        education_data = body if isinstance(body, list) else [body]
        created_ids = []

        for edu in education_data:
            school = edu.get("school")
            degree = edu.get("degree")
            duration = edu.get("duration")
            course = edu.get("course")
            icon = edu.get("icon")
            iconColor = edu.get("iconColor")
            createdAt = datetime.datetime.now().isoformat()

            if not school or not degree or not duration or not course:
                return JsonResponse(
                    {"message": "school, degree, duration, and course are required"},
                    status=400,
                )

            data = {
                "school": school,
                "degree": degree,
                "duration": duration,
                "course": course,
                "icon": icon,
                "iconColor": iconColor,
                "created_at": createdAt,
            }

            education = database.child("Education").push(data, token)
            created_ids.append(education["name"])

        return JsonResponse(
            {"message": "Education entries created", "ids": created_ids}, status=201
        )

    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)


@csrf_exempt
@api_view(["GET", "POST"])
def experience_create(request):
    if request.method == "GET":
        dataExp = []
        getExp = database.child("Experience").get(token).val()
        
        if not getExp:
            return JsonResponse({"message": " Skills not Found"}, status=404)
        
        for experience_id, experience in getExp.items():
            dataExp.append(experience)

        return JsonResponse(dataExp, safe=False)

    elif request.method == "POST":
        body = request.data

        if not body:
            return JsonResponse({"message": "No data provided"}, status=400)

        experience_data = body if isinstance(body, list) else [body]
        created_ids = []

        for exp in experience_data:
            company = exp.get("company")
            position = exp.get("position")
            duration = exp.get("duration")
            description = exp.get("description")
            icon = exp.get("icon")
            iconColor = exp.get("iconColor")
            createdAt = datetime.datetime.now().isoformat()

            if not company or not position or not duration or not description:
                return JsonResponse(
                    {
                        "message": "company, position, duration, and description are required"
                    },
                    status=400,
                )

            data = {
                "company": company,
                "position": position,
                "duration": duration,
                "description": description,
                "icon": icon,
                "iconColor": iconColor,
                "created_at": createdAt,
            }

            experience = database.child("Experience").push(data, token)
            created_ids.append(experience["name"])

        return JsonResponse(
            {"message": "Experience entries created", "ids": created_ids}, status=201
        )

    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)


@csrf_exempt
@api_view(["GET", "POST"])
def softSkill(request):
    if request.method == "GET":
        softSkills = []
        gitSoftSkill = database.child("SoftSkill").get(token).val()

        for skill_id, softSkill in gitSoftSkill.items():
            softSkills.append(softSkill)

        return JsonResponse(softSkills, safe=False)

    elif request.method == "POST":
        body = request.data

        if not body:
            return JsonResponse({"message": "No data provided"}, status=400)

        skills_data = body if isinstance(body, list) else [body]
        created_ids = []

        for skill in skills_data:
            title = skill.get("title")
            created_at = datetime.datetime.now().isoformat()

            if not title:
                return JsonResponse(
                    {"message": "Each skill must include a title"}, status=400
                )

            data = {
                "title": title,
                "created_at": created_at,
            }

            skill_ref = database.child("SoftSkill").push(data, token)
            created_ids.append(skill_ref["name"])

        return JsonResponse(
            {"message": "Soft skill(s) created successfully", "ids": created_ids},
            status=201,
        )

    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)
