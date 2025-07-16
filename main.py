from source.detect_drift.detect import detect_drift
from source.Agent.explan_with_ai import explan_drift,select_better_response
from source.send_email.send import send_email_to_member
from dotenv import load_dotenv
load_dotenv('.env')

path_fide_planJson = 'plan.json'

drift = detect_drift(path_fide_planJson)

AI1 = explan_drift(drift=drift,model='deepseek/deepseek-r1-0528-qwen3-8b:free')
AI2 = explan_drift(drift=drift,model='deepseek/deepseek-chat-v3-0324:free')
best_response = select_better_response(AI1,AI2,model='mistralai/mistral-small-3.2-24b-instruct:free')


send_email_to_member(best_response)