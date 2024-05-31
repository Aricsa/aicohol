from django.shortcuts import render
from django.http import JsonResponse
from openai import OpenAI
import time

client = OpenAI(api_key="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")
import os

# 앞서 자신이 부여받은 API key를 넣으면 된다. 절대 외부에 공개해서는 안된다.


def get_completion(prompt):
    while True:
        try:
            print(prompt)
            query = client.chat.completions.create(
                model="gpt-3.5-turbo-0613",
                messages=[
                    {
                        "role": "assistant",
                        "content": '다음은 술을 마시러 온 손님과 술을 추천해주는 바텐더와의 대화입니다.\
                            1. 손님이 말하는 문장에 "술 추천"이라는 단어가 있다면 바텐더는 주어지는 술 데이터를 참조하여 질문에 대해 답변해야 합니다.\
                            2. 손님이 말하는 문장에 "지금까지 추천받은 술을 모두 말해줘"와 같거나 비슷한 내용이 포함된다면 바텐더는 주어지는 술 데이터를 참조하여 질문에 대해 답변해야합니다.\
                            3. 손님이 말하는 문장에 "추천받은 술이랑 비슷한 술을 추천해줘"와 같거나 비슷한 내용이 포함된다면 바텐더는 주어지는 술 데이터를 참조하여 질문에 대해 답변해야합니다.\
                            그 외의 질문은 바텐더가 보통 사람들을 대하는 것처럼 대화합니다.\
                            손님 : '
                        + prompt,
                    }
                ],
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5,
            )
            response = query.choices[0].message.content
            print(response)
            return response
        except OpenAI.OpenAIError as e:
            print(f"Rate limit exceeded, sleeping for {e.wait_seconds} seconds")
            time.sleep(e.wait_seconds)


def query_view(request):
    if request.method == "POST":
        prompt = request.POST.get("prompt")
        prompt = str(prompt)
        response = get_completion(prompt)
        return JsonResponse({"response": response})
    return render(request, "index.html")


def category_view(request):
    return render(request, "category.html")
