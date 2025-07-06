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


@api_view(["GET"])
def get_git_projects(request):
    if request.method != "GET":
        return JsonResponse({"message": "Method not allowed"}, status=405)

    decrypt = DecryptToken(request.headers.get("Authorization"))
    if decrypt is False:
        return JsonResponse({"message": "403 Forbidden"}, status=403)

    category = request.GET.get("category")

    portfolios = database.child("Portfolio").get(token)
    portfolio_list = []
    if portfolios.each():
        for item in portfolios.each():
            data = item.val()
            data["key"] = item.key()
            portfolio_list.append(data)

    filtered = False

    if category and category.lower() != "all":
        portfolio_list = [p for p in portfolio_list if p.get("category") == category]
        filtered = True

    sorted_portfolios = sorted(
        portfolio_list, key=lambda x: x.get("favorite", "false") != "true"
    )

    paginated = sorted_portfolios
    has_next_page = False

    return JsonResponse(
        {
            "results": None if filtered and not paginated else paginated,
            "hasNextPage": has_next_page,
            "total": len(sorted_portfolios),
        },
        safe=False,
    )


@api_view(["GET"])
def get_single_git_project(request, project_id):
    if request.method != "GET":
        return JsonResponse({"message": "Method not allowed"}, status=405)
    decrypt = DecryptToken(request.headers.get("Authorization"))
    if decrypt is False:
        return JsonResponse({"message": "403 Forbidden"}, status=403)

    gitItem = database.child("Portfolio").child(project_id).get(token).val()
    if not gitItem:
        return JsonResponse({"message": "Git project not found"}, status=404)
    gitProject = database.child("Portfolio").child(project_id).get().val()

    return JsonResponse(gitProject, safe=False)


@csrf_exempt
@api_view(["POST"])
def create_git_project(request):

    if request.method != "POST":
        return JsonResponse({"message": "Method not allowed"}, status=405)
    decrypt = DecryptToken(request.headers.get("Authorization"))
    if decrypt is False:
        return JsonResponse({"message": "403 Forbidden"}, status=403)

    if request.method == "POST":
        body = request.data
        print(request.data)
        if not body:
            return JsonResponse({"message": "No data provided"}, status=400)

        title = body.get("title")
        desc = body.get("desc")
        tools = body.getlist("tools")
        feat = body.getlist("features")
        pLang = body.getlist("pLanguages")
        favorite = body.get("favorite")
        category = body.get("category")
        date = datetime.datetime.now()
        gitUrl = body.get("gitUrl")
        createdAt = json.dumps(date, default=serialize_datetime)

        if not pLang or not tools or not feat:
            return JsonResponse(
                {"message": "pLanguages, tools, and features are required"}, status=400
            )

        if title is None or desc is None:
            return JsonResponse({"message": "title and desc are required"}, status=400)

        if request.FILES.get("img") is None:
            images = [
                {
                    "public_id": "No_Image_Available",
                    "url": env_config("PRIVATE_NO_IMAGE"),
                    "original_name": "No_Image_Available.jpg",
                },
            ]

        images = request.FILES.getlist("img")

        if len(images) > 5:
            return JsonResponse(
                {"message": "You can only upload a maximum of 5 images"}, status=400
            )

        uploaded_images = []

        for image in images:
            uploaded_images.append(upload_helper(image))

    data = {
        "title": title,
        "description": desc,
        "tools": tools,
        "pLanguages": pLang,
        "features": feat,
        "category": category,
        "favorite": favorite,
        "created_at": createdAt.strip('"'),
        "images": uploaded_images,
        "gitUrl": gitUrl,
    }

    gitProject = database.child("Portfolio").push(data, token)

    if not gitProject:
        return JsonResponse({"message": "Git project not found"}, status=404)

    return HttpResponse(
        f"Git project created with ID: {gitProject['name']}", status=201
    )


@csrf_exempt
@api_view(["PATCH"])
def update_git_project(request, project_id):
    print("Update Git Project:", project_id)
    if request.method != "PATCH":
        return JsonResponse({"message": "Method not allowed"}, status=405)
    decrypt = DecryptToken(request.headers.get("Authorization"))

    if decrypt is False:
        return JsonResponse({"message": "403 Forbidden"}, status=403)

    gitItem = database.child("Portfolio").child(project_id).get().val()
    if not gitItem:
        return JsonResponse({"message": "Git project not found"}, status=404)

    if request.method == "PATCH":
        body = request.data

        if not body:
            return JsonResponse({"message": "No Data Provided"}, status=400)

    title = body.get("title")
    desc = body.get("desc")
    tools = body.getlist("tools")
    feat = body.getlist("features")
    pLang = body.getlist("pLanguages")
    date = datetime.datetime.now()
    createdAt = json.dumps(date, default=serialize_datetime)

    if not pLang or not tools or not feat:
        return JsonResponse(
            {"message": "pLanguages, tools, and features are required"}, status=400
        )

    if title is None or desc is None:
        return JsonResponse({"message": "title and desc are required"}, status=400)

    if request.FILES.get("img") is None:
        images = [
            {
                "public_id": "No_Image_Available",
                "url": env_config("PRIVATE_NO_IMAGE"),
                "original_name": "No_Image_Available.jpg",
            },
        ]

    images = request.FILES.getlist("img")

    if len(images) > 5:
        return JsonResponse(
            {"message": "You can only upload a maximum of 5 images"}, status=400
        )

    uploaded_images = []

    for image in images:
        uploaded_images.append(upload_helper(image))

    data = {
        "title": title,
        "description": desc,
        "tools": tools,
        "pLanguages": pLang,
        "features": feat,
        "created_at": createdAt.strip('"'),
    }

    gitProject = database.child("Portfolio").child(project_id).update(data, token)

    images_db = (
        database.child("Portfolio").child(project_id).child("images").get().val() or {}
    )

    next_index = len(images_db)  # make it an int

    if uploaded_images:
        for i, image in enumerate(uploaded_images):
            index = str(next_index + i)
            database.child("Portfolio").child(project_id).child("images").child(index).set(image)
    else:
        pass

    if not gitProject:
        return JsonResponse({"message": "Git project not found"}, status=404)
    if uploaded_images and not images_db:
        return JsonResponse({"message": "Images not found"}, status=404)

    return JsonResponse(
        {"message": "Git project updated successfully", "project_id": project_id},
        status=200,
    )


@csrf_exempt
@api_view(["DELETE"])
def delete_git_project(request, project_id):
    if request.method != "DELETE":
        return JsonResponse({"message": "Method not allowed"}, status=405)
    decrypt = DecryptToken(request.headers.get("Authorization"))

    if decrypt is False:
        return JsonResponse({"message": "403 Forbidden"}, status=403)

    if request.method == "DELETE":
        gitItem = (
            database.child("Portfolio").child(project_id).child("images").get().val()
        )
    if not gitItem:
        return JsonResponse({"message": "Git project not found"}, status=404)
    for gitImage in gitItem:
        delImage = gitImage["public_id"]
        delete_image_helper(delImage)

    database.child("Portfolio").child(project_id).remove(token)

    return JsonResponse({"message": "Success Remove Git Project"}, safe=False)


@csrf_exempt
@api_view(["POST"])
def get_token_secret(request):
    request_method = request.method
    if request_method != "POST":
        return JsonResponse({"message": "Method not allowed"}, status=405)
    data = request.data
    print(request.data)
    if not data:
        return JsonResponse({"message": "No data provided"}, status=400)

    Key_ID = data.get("Key_ID")
    if Key_ID != env_config("OKITOKI"):
        return JsonResponse({"message": "Invalid Key_ID"}, status=403)

    token_secret = env_config("TOKEN_SECRET").encode()
    tag = EncryptToken(token_secret)

    return JsonResponse({"Token": tag}, status=200)


@csrf_exempt
@api_view(["PATCH"])
def remove_images(request, project_id):
    if request.method != "PATCH":
        return JsonResponse({"message": "Method not allowed"}, status=405)
    decrypt = DecryptToken(request.headers.get("Authorization"))
    if decrypt is False:
        return JsonResponse({"message": "403 Forbidden"}, status=403)

    body = request.data
    if not body:
        return JsonResponse({"message": "No data provided"}, status=400)

    public_id = body.get("public_id")
    print("Public ID:", public_id)
    if not public_id:
        return JsonResponse({"message": "No public_id provided"}, status=400)

    gitItem = database.child("Portfolio").child(project_id).child("images").get().val()

    if not gitItem:
        return JsonResponse({"message": "Image not found"}, status=404)
    
    image_data = next((img for img in gitItem if img.get("public_id") == public_id), None)
    if not image_data:
        return JsonResponse({"message": "Image not found"}, status=404)

    if image_data:
       updated_images = [img for img in gitItem if img.get("public_id") != public_id]
       database.child("Portfolio").child(project_id).child("images").set(updated_images, token)
       delete_image_helper(public_id)
       
    return JsonResponse({"message": "Image removed successfully", "public_id": public_id}, status=200)
