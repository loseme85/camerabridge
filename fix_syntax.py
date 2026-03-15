import re

def fix_code():
    with open('test.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        # 오류가 발생한 라인을 찾아서 올바른 형식으로 교체합니다.
        if "SEARCH_ITEMS =" in line:
            # 괄호 오류를 제거하고 깨끗한 리스트 형식으로 바꿉니다.
            new_lines.append("SEARCH_ITEMS = ['0.95', '1.0', 'Noctilux', '녹티', '녹티룩스']\n")
        else:
            new_lines.append(line)

    with open('test.py', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("✅ 코드 구문 오류 수정 완료!")

if __name__ == "__main__":
    fix_syntax.py()
