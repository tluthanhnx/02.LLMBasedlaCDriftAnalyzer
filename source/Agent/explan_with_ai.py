from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import List, Dict

def explan_drift(drift : List, model : str = 'deepseek/deepseek-r1-0528:free') -> str:
    
    openRouter_api_key = os.getenv('open_router_api_key')
    print(openRouter_api_key)
    prompt = f"""
                Bạn là một chuyên gia DevOps giàu kinh nghiệm đang tham gia đánh giá hệ thống hạ tầng tự động bằng mã nguồn (Infrastructure as Code - IaC), sử dụng Terraform.

                Dưới đây là một thay đổi (drift) đã được phát hiện khi so sánh hạ tầng thực tế với cấu hình định nghĩa trong mã Terraform. Yêu cầu bạn:

                1. Giải thích kỹ lưỡng sự thay đổi (drift) bằng ngôn ngữ đơn giản, dễ hiểu.
                2. Phân tích nguyên nhân gốc có thể gây ra sự khác biệt này.
                3. Đánh giá tác động của sự thay đổi đối với bảo mật, hiệu năng, tính ổn định hoặc chi phí.
                4. Phân loại mức độ nghiêm trọng của drift: Nhẹ / Trung bình / Nghiêm trọng.
                5. Đưa ra khuyến nghị kỹ thuật rõ ràng.
                6. Nếu có thể, hãy đề xuất chiến lược phòng ngừa drift tương tự trong tương lai.

                ### Thông tin drift:
                    {drift}

                Vui lòng trả lời chi tiết như một chuyên gia đang viết báo cáo audit cho đội DevOps và bảo mật.
                Hãy phản hồi theo dạng markdown.
            """
    
    client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=openRouter_api_key,
            )
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Bạn là một trợ lý DevOps thông minh, chuyên phân tích drift từ Terraform."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        print(e)
        return f"Lỗi khi gọi Openrouter API: {e}"
    
def select_better_response(AI1_output: str, AI2_output:str, model: str = 'deepseek/deepseek-r1-0528-qwen3-8b:free') -> str:
    
    openRouter_api_key = os.getenv('open_router_api_key')
    
    prompt = f"""
                Bạn là một trọng tài AI chuyên về DevOps. Dưới đây là hai phản hồi khác nhau từ hai hệ thống AI về một thay đổi hạ tầng (drift) trong Terraform.

                Hãy đánh giá một cách **ngắn gọn và thầm lặng**, chọn **duy nhất một** phản hồi tốt hơn (AI1 hoặc AI2) dựa trên độ chính xác, rõ ràng, và khả năng hành động. Chỉ cần phản hồi bằng một trong hai giá trị chính xác sau:

                - `AI1`
                - `AI2`

                ### Phản hồi AI1:
                {AI1_output}

                ---

                ### Phản hồi AI2:
                {AI2_output}

                ---

                Lựa chọn của bạn (chỉ ghi `AI1` hoặc `AI2`):
            """
    
    openRouter_api_key = os.getenv('open_router_api_key')

    client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=openRouter_api_key,
            )
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                        {"role": "system", "content": "Bạn là một trọng tài AI DevOps trung lập. Không giải thích, chỉ chọn 1 phương án tốt hơn."},
                        {"role": "user", "content": prompt}
                     ]
        )
        result  = response.choices[0].message.content

        if result == 'AI1' :
            return AI1_output
        return AI2_output

    except Exception as e:
        return f"Lỗi khi gọi Openrouter API: {e}"
