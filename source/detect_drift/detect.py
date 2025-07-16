import json
from typing import List, Dict
def detect_drift(plan_json_path : str) -> List[Dict] :

    
    with open(plan_json_path, 'r') as f:
        data = json.load(f)

    resource_changes = data.get("resource_changes", [])

    drifted_resources = []

    for change in resource_changes:
        address = change.get("address")
        actions = change.get("change", {}).get("actions", [])
        before = change.get("change", {}).get("before")
        after = change.get("change", {}).get("after")

        # Bỏ qua những thay đổi không thực tế (no-op)
        if "no-op" in actions:
            continue

        drifted_resources.append({
            "resource": address,
            "action": ", ".join(actions),
            "before": before,
            "after": after
        })
    return drifted_resources



# if __name__ == "__main__":

#     path_file_planJson = '../../plan.json'
#     detect= detect_drift(path_file_planJson)
#     print(type(detect[0]))
#     for i in detect[0]:
#         print(i)
#         print('------------------------------------')


