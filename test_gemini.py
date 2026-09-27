from utils.llm import get_llm


llm = get_llm()


response = llm.invoke(
    "Explain what an insurance claim is in one sentence."
)


print("\nGEMINI CONNECTION SUCCESSFUL")
print("=" * 50)
print(response.content)