# from django.shortcuts import render
# import json
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from chat.service.feedback_service import save_feedback

# # chat/controller/views_feedback.py

# def save_feedback_view1(request):
#     if request.method == "POST":
#         data = request.POST
#         user_id = data.get("user")
#         question = data.get("question")
#         answer = data.get("answer")
#         feedback = data.get("feedback")  # 'good', 'normal', 'bad'
#         turn = int(data.get("turn"))

#         save_feedback(user_id, question, answer, feedback, turn)
#         return JsonResponse({"status": "ok"})
#     return JsonResponse({"status": "fail", "reason": "Not POST"})

# def save_feedback_view(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)

#             user_id = data.get('user_id')
#             turn = int(data.get('turn'))
#             feedback = data.get('feedback')

#             # 필수값 체크
#             if not all([user_id, feedback, turn]):
#                 return JsonResponse({'error': 'Invalid data'}, status=400)

#             # 채팅 로그가 이미 저장되어 있어야 question, answer를 불러와 피드백 저장 가능
#             from chat.models import ChatLog
#             chat = ChatLog.objects.filter(user_id=user_id, turn=turn).first()

#             if not chat:
#                 return JsonResponse({'error': 'Chat record not found'}, status=404)

#             # 저장
#             save_feedback(
#                 user_id=user_id,
#                 question=chat.question,
#                 answer=chat.answer,
#                 feedback=feedback,
#                 turn=turn
#             )

#             return JsonResponse({'status': 'ok'})
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=405)
    

# from django.http import JsonResponse
# from chat.service.feedback_service import UserService

# def register_user_view(request):
#     if request.method == 'POST':
#         user_id = request.POST.get('user_id')
#         success = UserService.register_user(user_id)
#         if success:
#             return JsonResponse({'status': 'success'})
#         else:
#             return JsonResponse({'status': 'error', 'message': '이미 존재하는 사용자입니다.'})
#     return JsonResponse({'status': 'error', 'message': 'POST 요청만 허용됩니다.'})

# chat/controller/views_feedback.py

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from chat.service.feedback_service import save_feedback
from chat.models import ChatLog
from chat.service.user_service import UserService


# @csrf_exempt
# def save_feedback_view(request):
#     print(f"[💬 피드백 요청 수신] URL: {request.path} | Method: {request.method}") 
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)

#             user_id = data.get('user_id')
#             feedback = data.get('feedback')
#             turn_raw = data.get('turn')
            
#             print("[📨 피드백 요청 수신]")
#             print("  user_id:", user_id)
#             print("  turn:", turn_raw)

#             print("[🔍 DB에 저장된 ChatLog 목록]", list(ChatLog.objects.filter(user_id=user_id).values()))


#             # 필수값 존재 여부
#             if not all([user_id, feedback, turn_raw]):
#                 return JsonResponse({'error': 'Invalid data'}, status=400)

#             try:
#                 turn = int(turn_raw)
#             except ValueError:
#                 return JsonResponse({'error': 'Invalid turn number'}, status=400)

#             # DB에서 해당 chat 찾기
#             chat = ChatLog.objects.filter(user_id=user_id, turn=turn).first()
#             if not chat:
#                 return JsonResponse({'error': 'Chat record not found'}, status=404)

#             # 저장
#             save_feedback(
#                 user_id=user_id,
#                 question=chat.question,
#                 answer=chat.answer,
#                 feedback=feedback,
#                 turn=turn
#             )

#             return JsonResponse({'status': 'ok'})

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)

#     return JsonResponse({'error': 'Invalid request method'}, status=405)
# @csrf_exempt
# def save_feedback_view(request):
#     print(f"[💬 피드백 요청 수신] URL: {request.path} | Method: {request.method}")

#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             user_id = data.get('user_id')
#             turn_raw = data.get('turn')
#             feedback = data.get('feedback')

#             print("[📨 피드백 요청 수신]")
#             print("  user_id:", user_id)
#             print("  turn:", turn_raw)

#             from chat.models import ChatLog
#             print("[🔍 DB에 저장된 ChatLog 목록]", list(ChatLog.objects.filter(user_id=user_id).values()))

#             turn = int(turn_raw)
#             # ✅ ② 디버깅 로그 2: 필터 조건 로그
#             print("[🧾 필터링 조건 확인] user_id =", user_id, "| turn =", turn)

#             # ✅ ③ 디버깅 로그 3: 전체 ChatLog 보기
#             from chat.models import ChatLog
#             print("[🔍 DB에 저장된 전체 ChatLog 목록]", list(ChatLog.objects.all().values()))

#             chat = ChatLog.objects.filter(user_id=user_id, turn=turn).first()

#             if not chat:
#                 print("[🚫 ChatLog 없음 → 404 반환]")
#                 return JsonResponse({'error': 'Chat record not found'}, status=404)

#             chat.feedback = feedback
#             chat.save()

#             print("[✅ 피드백 저장 완료]")
#             return JsonResponse({'status': 'ok'})

#         except Exception as e:
#             print("[❌ 예외 발생]", str(e))
#             return JsonResponse({'error': str(e)}, status=500)

#     print("[🚫 POST 아님 → 405 반환]")
#     return JsonResponse({'error': 'Invalid request method'}, status=405)
from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from chat.models import ChatLog

@csrf_exempt
def save_feedback_view(request):
    print(f"[💬 피드백 요청 수신] URL: {request.path} | Method: {request.method}")

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            turn_raw = data.get('turn')
            feedback = data.get('feedback')

            print("[📨 피드백 요청 수신]")
            print("  user_id:", user_id)
            print("  turn_raw:", turn_raw)
            print("  feedback:", feedback)

            turn = int(turn_raw)

            # ✅ 디버깅 로그: DB에 저장된 user_id들과 비교
            chatlog_all = ChatLog.objects.all().values('user_id', 'turn')
            print("[🧾 저장된 ChatLog user_id/turn 목록]")
            for entry in chatlog_all:
                print(f" - user_id: '{entry['user_id']}' (len={len(entry['user_id'])}) | turn: {entry['turn']}")
            print(f"[🧾 비교 대상] user_id: '{user_id}' (len={len(user_id)}) | turn: {turn}")

            user_id = user_id.strip()  # 앞뒤 공백 제거

            chat = ChatLog.objects.filter(user_id=user_id, turn=turn).first()

            if not chat:
                print("[🚫 ChatLog 없음 → 404 반환]")
                return JsonResponse({'error': 'Chat record not found'}, status=404)

            chat.feedback = feedback
            chat.save()

            print("[✅ 피드백 저장 완료]")
            return JsonResponse({'status': 'ok'})

        except Exception as e:
            print("[❌ 예외 발생]", str(e))
            return JsonResponse({'error': str(e)}, status=500)

    print("[🚫 POST 아님 → 405 반환]")
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def register_user_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        if not user_id:
            return JsonResponse({'status': 'error', 'message': 'user_id 누락됨'}, status=400)

        success = UserService.register_user(user_id)
        if success:
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': '이미 존재하는 사용자입니다.'})
    return JsonResponse({'status': 'error', 'message': 'POST 요청만 허용됩니다.'})
