from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from chat.service.chat_service import ChatService
from chat.models import ChatLog
from django.http import JsonResponse
from chat.service.user_service import UserService


def intro_view(request):
    return render(request, "chat/intro.html")

def chat_view(request):
    return render(request, "chat/chat.html")


@csrf_exempt
def ask_llm_view(request):
    print(f"[🤖 질문 요청 수신] URL: {request.path} | Method: {request.method}")
    if request.method == 'POST':
        companies = request.POST.getlist('companies')
        categories = request.POST.getlist('categories')
        query = request.POST.get('query')

        chat_service = ChatService()
        answer = chat_service.ask_with_llm(query, companies, categories)

        # ✅ 세션에서 user_id 추출
        # user_id = request.session.get('user_id')

        # ✅ 여기서부터 ChatLog 저장
        user_id = UserService.get_or_create_user(request.session)
        turn = ChatLog.objects.filter(user_id=user_id).count() + 1
        chat_id = f"{user_id}-{str(turn).zfill(2)}"

        ChatLog.objects.create(
            chat_id=chat_id,
            user_id=user_id,
            question=query,
            answer=answer,
            turn=turn
        )

        print("[✅ ChatLog 저장 완료]")
        print("  chat_id:", chat_id)
        print("  user_id:", user_id)
        print("  turn:", turn)
        
        return JsonResponse({
    'answer': answer,
    'turn': turn  # ✅ turn도 함께 반환
})


        # return render(request, 'chat/chat.html', {
        #     'query': query,
        #     'answer': answer,
        #     'user_id': user_id,  # ✅ 여기에 반드시 추가!
        # })
    else:
        user_id = request.session.get('user_id')
        return render(request, 'chat/chat.html', {'user_id': user_id})



from django.http import JsonResponse
import json
import uuid
from chat.models import ChatLog
from chat.service.user_service import UserService

def intro_view(request):
    user_id = UserService.get_or_create_user(request.session)
    return render(request, "chat/intro.html", {'user_id': user_id})

# @csrf_exempt
# def chat_view(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         question = data.get('question')
#         user_id = request.session.get('user_id')
#         turn = ChatLog.objects.filter(user_id=user_id).count() + 1

#         answer = ChatService().ask_with_llm(question, [], [])

#         chat_id = f"{user_id}-{str(turn).zfill(2)}"
#         ChatLog.objects.create(chat_id=chat_id, user_id=user_id, question=question, answer=answer, turn=turn)

#         return JsonResponse({'answer': answer, 'chat_id': chat_id})
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from chat.models import ChatLog
from chat.service.user_service import UserService
from chat.service.chat_service import ChatService


# @csrf_exempt
# def chat_view(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             question = data.get('question')
#             user_id = request.session.get('user_id')
#             turn = ChatLog.objects.filter(user_id=user_id).count() + 1

#             answer = ChatService().ask_with_llm(question, [], [])

#             chat_id = f"{user_id}-{str(turn).zfill(2)}"
#             ChatLog.objects.create(
#                 chat_id=chat_id,
#                 user_id=user_id,
#                 question=question,
#                 answer=answer,
#                 turn=turn
#             )

#             return JsonResponse({'answer': answer, 'chat_id': chat_id})
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)

#     # ❗ GET 요청 시에는 채팅 화면 렌더링
#     return render(request, 'chat/chat.html')
from chat.service.user_service import UserService

def chat_view(request):
    print(f"[🟢 CHAT 페이지 진입] URL: {request.path} | Method: {request.method}")
    user_id = UserService.get_or_create_user(request.session)
    return render(request, "chat/chat.html", {'user_id': user_id})  # ✅ user_id 템플릿으로 전달


# @csrf_exempt
# def save_chatlog_view(request):
#     print(f"[💾 ChatLog 저장 요청 수신] URL: {request.path} | Method: {request.method}")
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             user_id = data.get('user_id')
#             question = data.get('question')
#             answer = data.get('answer')
#             turn = int(data.get('turn'))

#             chat_id = f"{user_id}-{str(turn).zfill(2)}"

#             ChatLog.objects.create(
#                 chat_id=chat_id,
#                 user_id=user_id,
#                 question=question,
#                 answer=answer,
#                 turn=turn
#             )

#             print("[📝 ChatLog 수동 저장 완료]")
#             print("  chat_id:", chat_id)
#             print("  user_id:", user_id)
#             print("  turn:", turn)

#             return JsonResponse({'status': 'ok'})
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)

#     return JsonResponse({'error': 'Invalid request method'}, status=405)
# @csrf_exempt
# def save_chatlog_view(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             user_id = data.get("user_id")
#             question = data.get("question")
#             answer = data.get("answer")
#             turn = int(data.get("turn"))

#             print("[📝 ChatLog 저장 시도]")
#             print("  user_id:", user_id)
#             print("  turn:", turn)

#             chat_id = f"{user_id}-{str(turn).zfill(2)}"

#             ChatLog.objects.create(
#                 chat_id=chat_id,
#                 user_id=user_id,
#                 question=question,
#                 answer=answer,
#                 turn=turn
#             )

#             print("[✅ 저장 완료] chat_id:", chat_id)
#             return JsonResponse({'status': 'ok'})

#         except Exception as e:
#             print("[❌ 저장 중 오류]", str(e))
#             return JsonResponse({'error': str(e)}, status=500)

#     return JsonResponse({'error': 'Invalid method'}, status=405)
@csrf_exempt
def save_chatlog_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get("user_id")
            question = data.get("question")
            answer = data.get("answer")
            turn = int(data.get("turn"))

            print("[📝 ChatLog 저장 시도]")
            print("  user_id:", user_id)
            print("  turn:", turn)

            chat_id = f"{user_id}-{str(turn).zfill(2)}"

            ChatLog.objects.create(
                chat_id=chat_id,
                user_id=user_id,
                question=question,
                answer=answer,
                turn=turn
            )

            print("[✅ 저장 완료] chat_id:", chat_id)
            return JsonResponse({'status': 'ok'})

        except Exception as e:
            print("[❌ 저장 중 오류]", str(e))
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid method'}, status=405)
