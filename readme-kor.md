# MobiusSubscription을 활용한 다중 구독 Python 프로그램

본 프로젝트는 **Mobius** 플랫폼의 리소스에 구독을 설정하고, 해당 리소스에서 생성되는 **컨텐츠 인스턴스(cin)**의 **컨텐츠(con)** 값을 읽어오는 Python 프로그램입니다. 각 구독은 개별 스레드로 동작하여 충돌이나 간섭 없이 독립적으로 운영되며, 다중 구독을 지원합니다.

## 주요 기능

- **구독 생성:** Mobius 서버의 특정 AE(Application Entity)와 컨테이너(endpoint)에 대해 구독을 생성합니다.
- **MQTT 클라이언트 설정:** MQTT 프로토콜을 사용하여 Mobius 서버와 통신하고, 알림을 수신합니다.
- **메시지 처리:** 수신된 MQTT 메시지에서 cin의 con 값을 추출하여 출력합니다.
- **다중 구독 및 스레드 관리:** 각 구독은 별도의 스레드에서 동작하여 독립적으로 메시지를 수신하고 처리합니다.
- **구독 해제 및 자원 정리:** 프로그램 종료 시 안전하게 구독을 해제하고 연결을 종료합니다.

## 시작하기

### 사전 준비

- **Python 3.x**가 설치되어 있어야 합니다.
- 필요한 라이브러리를 설치합니다:

  ```bash
  pip install paho-mqtt requests
  ```

### 코드 다운로드

이 저장소를 클론하거나 필요한 파일을 다운로드합니다.

```bash
git clone https://github.com/yourusername/mobius-subscription.git
```

## 사용 방법

### MobiusSubscription 클래스 임포트

```python
from mobius_subscription import MobiusSubscription
```

### 구독 인스턴스 생성 및 실행 예시

```python
# 첫 번째 구독 인스턴스 생성
subscription1 = MobiusSubscription(
    cse_host="YOUR_MOBIUS_HOST",
    cse_port=YOUR_MOBIUS_PORT,
    ae_name="YOUR_AE_NAME",
    endpoint="YOUR_CONTAINER_NAME_1"
)
subscription1.run()

# 두 번째 구독 인스턴스 생성
subscription2 = MobiusSubscription(
    cse_host="YOUR_MOBIUS_HOST",
    cse_port=YOUR_MOBIUS_PORT,
    ae_name="YOUR_AE_NAME",
    endpoint="YOUR_CONTAINER_NAME_2"
)
subscription2.run()
```

### 프로그램 실행 유지 및 종료 처리

```python
try:
    while True:
        # 메인 스레드는 다른 작업을 수행하거나 대기 상태 유지
        pass
except KeyboardInterrupt:
    # 프로그램 종료 시 구독 해제 및 자원 정리
    subscription1.stop()
    subscription2.stop()
```

## 클래스 상세 설명

### MobiusSubscription 클래스 초기화

```python
MobiusSubscription(
    cse_host,       # Mobius 서버의 호스트 주소 (예: "203.253.128.177")
    cse_port,       # Mobius 서버의 포트 번호 (예: 7579)
    ae_name,        # 구독할 AE의 이름 (예: "SubTest")
    endpoint,       # 구독할 컨테이너의 이름 (예: "testcnt1")
    cse_mqttport=1883,  # (옵션) MQTT 포트 번호, 기본값은 1883
    cse_name="Mobius",  # (옵션) CSE의 이름, 기본값은 "Mobius"
    origin="UbicompSub" # (옵션) Originator 식별자, 기본값은 "UbicompSub"
)
```

- **cse_host:** Mobius 서버의 IP 주소 또는 도메인 이름.
- **cse_port:** Mobius 서버의 HTTP 포트 번호.
- **ae_name:** 구독을 생성할 AE의 이름.
- **endpoint:** 구독할 컨테이너의 이름.
- **cse_mqttport:** (선택 사항) MQTT 브로커의 포트 번호. 기본값은 1883.
- **cse_name:** (선택 사항) Mobius CSE의 이름. 기본값은 "Mobius".
- **origin:** (선택 사항) Originator 식별자. 기본값은 "UbicompSub".

### 주요 메서드

- **run():** 구독을 생성하고 MQTT 클라이언트를 설정하여 메시지 수신을 시작합니다.
- **stop():** 구독을 해제하고 MQTT 연결과 스레드를 종료합니다.

## 실행 흐름

1. **인스턴스 생성:** `MobiusSubscription` 클래스를 필요한 매개변수와 함께 인스턴스화합니다.
2. **구독 시작:** `run()` 메서드를 호출하여 구독을 생성하고 MQTT 클라이언트를 시작합니다.
3. **메시지 수신 및 처리:** 각 구독은 개별 스레드에서 메시지를 수신하며, 새로운 cin이 생성될 때마다 con 값을 출력합니다.
4. **프로그램 종료 및 자원 정리:** 프로그램이 종료되거나 구독이 더 이상 필요하지 않을 때 `stop()` 메서드를 호출하여 구독을 해제하고 자원을 정리합니다.

## 주의 사항

- **Mobius 서버 설정:** `cse_host`, `cse_port`, `ae_name`, `endpoint` 등은 실제 환경에 맞게 설정해야 합니다.
- **AE 및 컨테이너 사전 생성:** 구독하려는 AE와 컨테이너(endpoint)가 Mobius 서버에 미리 생성되어 있어야 합니다.
- **자원 해제:** 프로그램 종료 시 반드시 `stop()` 메서드를 호출하여 구독을 해제하고 연결을 종료해야 합니다.
- **예외 처리:** 예기치 않은 종료에 대비하여 `try-except` 블록을 사용하여 자원 해제를 보장하는 것이 좋습니다.

## 라이선스

이 프로젝트는 [MIT 라이선스](LICENSE)에 따라 배포됩니다.

## 기여

버그 신고, 기능 개선 요청 또는 풀 리퀘스트는 언제든지 환영합니다.

## 문의

질문이나 문의 사항이 있으시면 이메일(woojin2296@kakao.com)로 연락해 주십시오.