import json
from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv('./source/.env')
api_key =  os.getenv('open_router_api_key')
print(api_key)

# with open('plan.json','r') as f:
#     resource_changes = json.load(f)
#     resource_changes = resource_changes['resource_changes']
#     new_resource = resource_changes[2]['change']['after']
#     old_resource = resource_changes[2]['change']['before']
#     action = resource_changes[2]['change']['actions']
# print(len(resource_changes))
# print(action)
# print(new_resource.keys())
# print()
# print(old_resource.keys())
# print('___________________')
with open("plan.json", "r", encoding="utf-8") as f:
    content = f.read()
    

messages = [
    {'role':'system', 'content':f"""Bạn là một chuyên gia DevOps cấp cao với nhiều năm kinh nghiệm triển khai hạ tầng bằng Terraform.
                                    Nếu không có sự khác biệt nào thì trả lời là "Tình huống cho thấy rằng hạ tầng hiện tại khớp với cấu hình Terraform, không cần thực hiện thay đổi nào."
Còn nếu có tôi sẽ cung cấp cho bạn một đoạn thông tin về sự sai lệch (drift) giữa định nghĩa hạ tầng trong mã Terraform và trạng thái thực tế trên hệ thống.

Bạn hãy thực hiện các bước phân tích sau và trả lời bằng **tiếng Việt**, chi tiết và chuyên nghiệp:

### 1. **Tóm tắt drift**
- Tài nguyên nào bị ảnh hưởng?
- Loại thay đổi là gì? (Tạo mới, bị xoá, hay bị thay đổi thuộc tính)

### 2. **Phân tích kỹ thuật**
- Mô tả chính xác thuộc tính nào bị thay đổi (trước và sau)
- Định nghĩa kỹ thuật của thuộc tính đó có ảnh hưởng gì đến hạ tầng?
- Có liên quan đến hiệu năng, bảo mật, hoặc chi phí không?

### 3. **Xác định nguyên nhân gốc**
- Có khả năng thay đổi này đến từ thao tác thủ công?
- Hay do một công cụ/CI/CD khác đã can thiệp?
- Có khả năng nào drift xảy ra do chính Terraform bị lỗi?

### 4. **Đánh giá tác động**
- Mức độ nghiêm trọng của drift này là gì? (Thấp / Trung bình / Cao)
- Có thể gây lỗi ứng dụng, downtime hay rủi ro bảo mật không?

### 5. **Khuyến nghị hành động**
- Nếu thay đổi là có chủ đích: có nên cập nhật lại mã Terraform không?
- Nếu không phải chủ đích: có nên rollback? dùng `terraform apply` hay xử lý thủ công?
- Đề xuất cách ngăn chặn drift tương tự trong tương lai (tag audit, CI/CD validate, drift detection định kỳ, v.v.)

### 6. **Kết luận**
- Tóm tắt lại 1 câu về tình huống và đề xuất của bạn.

---

Dưới đây là dữ liệu drift cần phân tích:

"""
    },
    {'role':'user', 'content':f""" Tôi sẽ cung cap  file.txt. 
                                      {content}
                                  """
    }
]

client = OpenAI(
  base_url= "https://openrouter.ai/api/v1",
  api_key= api_key,
)

completion = client.chat.completions.create(
  
  model="deepseek/deepseek-r1-distill-llama-70b:free",
  messages=messages
)
result1  = completion.choices[0].message.content
print(result1)

# completion = client.chat.completions.create(
  
#   model="deepseek/deepseek-r1-0528:free",
#   messages=messages,
 
# )
# result2 = completion.choices[0].message.content

# print('sssssss')
# result = {
#     'result1' : result1,
#     'result2': result2
# }


# messages = [
#     {'role':'system', 'content':f"""Bạn là một chuyên gia DevOps và reviewer trong một cuộc thi về hệ thống phát hiện drift Terraform.

# Dưới đây là **2 câu trả lời từ hai mô hình AI khác nhau** cho cùng một tình huống drift.  

# Hãy phân tích và đánh giá chúng theo các tiêu chí sau.phân tích trong thầm nặng và trả ra kết quả result1 hay result2:

# 1. Câu trả lời nào **đúng hơn về kỹ thuật**?
# 2. Câu trả lời nào **giải thích rõ ràng hơn**?
# 3. Câu trả lời nào **đưa ra khuyến nghị hợp lý hơn**?
# 4. Có lỗi hoặc thông tin không chính xác nào không?

# Sau đó:

# - Phản hồi theo dạng json cái nào tốt hơn lên trước ví dụ result1 tốt hơn result 2 thì trả ra array có dạng. Không trả về bát cứ lời giải thích nào chỉ cần trả về danh sách xếp hạng của các câu trả lời

# """
#     },
#     {'role':'user', 'content':f""" Tôi sẽ cung cap  ket qua. 
#                                       {result}
#                                   """
#     }
# ]
# completion = client.chat.completions.create(
  
#   model="qwen/qwen3-235b-a22b:free",
#   messages=messages
# )
# print(completion.choices[0].message.content)
# print(result['completion.choices[0].message.content'])


import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import markdown
# Thiết lập thông tin email
result1 = markdown.markdown(result1)
message = Mail(
    from_email='nhphan.ai01@gmail.com',           # Địa chỉ email của bạn (phải được xác thực với SendGrid)
    to_emails='phannguyenhuu46@gmail.com;thanhnx1979@gmail.com',        # Người nhận
    subject='Detect Drift',
    html_content= result1
)
sengrid_api_key = os.getenv('sengrid_api_key')
try:
    # Gửi email
    sg = SendGridAPIClient(sengrid_api_key)  # Thay bằng API key của bạn
    response = sg.send(message)
    print(f"Status Code: {response.status_code}")
    print("Email sent successfully.")
except Exception as e:
    print(f"Error sending email: {e}")


