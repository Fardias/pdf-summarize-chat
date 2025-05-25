import google.generativeai as genai
genai.configure(api_key="AIzaSyA9zCd8m_A0nhTpjGz5Uy332rdBJglt5lE")

models = genai.list_models()
for model in models:
    print(model.name)
