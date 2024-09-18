import requests
import json
import time

# Mobius 서버 정보
CSE_BASE = "http://203.253.128.177:7579/Mobius"
AE_NAME = "SubTest"
CONTAINER_NAME = "testcnt1"

# Mobius 요청에 필요한 헤더 정보
HEADERS = {
    "X-M2M-Origin": "SOrigin",  # Mobius 인증 정보 (기본 값)
    "X-M2M-RI": "12345",        # 요청 ID (임의 값)
    "Content-Type": "application/json;ty=3"  # 리소스 타입 3 (컨테이너 생성)
}

# 컨테이너 생성
def create_container():
    url = f"{CSE_BASE}/{AE_NAME}"
    payload = {
        "m2m:cnt": {
            "rn": CONTAINER_NAME  # 새 컨테이너의 이름
        }
    }
    response = requests.post(url, headers=HEADERS, data=json.dumps(payload))
    
    if response.status_code == 201:
        print(f"Container '{CONTAINER_NAME}' created successfully.")
    elif response.status_code == 409:
        print(f"Container '{CONTAINER_NAME}' already exists.")
    else:
        print(f"Failed to create container. Status code: {response.status_code}, Response: {response.text}")

# 콘텐츠 인스턴스 생성
def create_cin(content):
    url = f"{CSE_BASE}/{AE_NAME}/{CONTAINER_NAME}"
    payload = {
        "m2m:cin": {
            "cnf": "text",    # 콘텐츠 포맷
            "con": content    # 실제 콘텐츠 (여기서는 1)
        }
    }
    headers = {
        "X-M2M-Origin": "SOrigin",  # Mobius 인증 정보 (기본 값)
        "X-M2M-RI": "12345",        # 요청 ID (임의 값)
        "Content-Type": "application/json;ty=4"  # 리소스 타입 4 (콘텐츠 인스턴스 생성)
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 201:
        print(f"Content Instance with content '{content}' created successfully.")
    else:
        print(f"Failed to create content instance. Status code: {response.status_code}, Response: {response.text}")

# 메인 로직
if __name__ == "__main__":
    # 컨테이너를 먼저 생성 (이미 있으면 생성되지 않음)
    create_container()

    # 1초마다 콘텐츠 인스턴스를 생성 (content: 1)
    try:
        while True:
            create_cin("1")
            time.sleep(3)  # 1초 대기
    except KeyboardInterrupt:
        print("Terminated by user")