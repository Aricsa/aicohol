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
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
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
    return render(request, 'category.html')