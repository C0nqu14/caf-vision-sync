import google.generativeai as genai

genai.configure(api_key="AIzaSyC3FRVJRGrot2zsczCkp4M-rNBRv0LWLAQ")

modelo = genai.GenerativeModel("gemini-1.5-flash")

msg = input("MSG: ")
prompt = f"Analise o seguinte feedback {msg} e determine o sentimento geral (positivo, negativo, neutro). Forneça uma breve explicação para justificar a sua conclusão."

resposta = modelo.generate_content(prompt)
print(resposta.text)
