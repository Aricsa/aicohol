from django.shortcuts import render
from django.http import JsonResponse
from openai import OpenAI
from .query import prompt_research, recommend, reference, reference_recommend
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO


# client = openai.api_key = "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"
client = OpenAI(api_key="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")
import os

# 앞서 자신이 부여받은 API key를 넣으면 된다. 절대 외부에 공개해서는 안된다.


def get_completion(prompt):
    original_prompt = prompt
    print(prompt)
    prompt2 = prompt_research(prompt)
    print(prompt2)
    if prompt2 == 2:
        prompt = reference()
        print(prompt)
    elif prompt2 == 1 or prompt2 == 3:
        prompt = reference_recommend(prompt)
        print(prompt)
    else:
        return "죄송합니다. 말씀하신 바를 잘 이해하지 못했어요..."
    return prompt


def query_view(request):
    if request.method == "POST":
        prompt = request.POST.get("prompt")
        prompt = str(prompt)
        response = get_completion(prompt)
        return JsonResponse({"response": response})
    return render(request, "index.html")


def list_view(request):
    return render(request, "list.html")


def detail_view(request):
    return render(request, "detail.html")

@csrf_exempt
def transcribe_audio(request):
    if request.method == "POST":
        audio_file = request.FILES.get("audio_file")
        if audio_file:
            try:
                audio_file_obj = BytesIO(audio_file.read())
                audio_file_obj.name = audio_file.name
                # openai.api_key = os.getenv("OPENAI_API_KEY")
                # transcription = openai.Audio.transcribe(
                #     "whisper-1", file=audio_file_obj, language="ko"
                # )
                transcription = client.audio.transcriptions.create(
                    model="whisper-1", file=audio_file_obj, language="ko"
                )
                print(f"Transcription: {transcription.text}")
                return JsonResponse({"transcription": transcription.text})
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)
