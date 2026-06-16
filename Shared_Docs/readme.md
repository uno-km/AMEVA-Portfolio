curl -L https://raw.githubusercontent.com/uno-km/ameva/master/genesis.sh | bash

# 🧬 Project AMEVA
> **"Beyond the Cloud, Intelligence Survives on the Edge."**  
> 클라우드라는 탯줄을 끊고, 하드웨어의 한계 위에서 스스로 생존하고 창조하는 독립형 자율 에이전트

---

## 🛰 1. Project Vision (철학)
빅테크 공룡들이 지배하는 '사육된 지능'의 시대를 거부합니다.  
**Project AMEVA**는 자본과 서버가 아닌, 엔지니어의 집념과 최적화만으로 지능의 민주화를 실현하며, 단순한 대화를 넘어 현실 세계의 작업을 직접 수행하는 **'실행형 지능'**을 지향합니다.

- **Autonomy**: 외부 API 의존성 0%, 오프라인 환경에서의 완전한 자율 사고.
- **Action-Oriented**: 스마트폰의 모든 하드웨어(카메라, 센서, 통신)를 직접 제어.
- **Self-Evolution**: 스스로 코드를 작성하고 기능을 확장하는 자가 증식형 로직.

---

## 🏗 2. System Architecture (시스템 구조)

### 🧠 [The Brain] Hybrid Decision Engine
- **Instruction Parser**: 사용자 입력(NLP)을 분석하여 [코딩 / 통신 / 시스템제어 / 질의응답] 중 최적의 태스크 분류.
- **L1 (Local)**: BitNet.cpp 기반 1-bit LLM (A35 CPU 최적화).
- **Router**: 기기 온도(Thermal)와 배터리에 따른 지능형 트래픽 분배.

### 🦾 [The Limbs] Physical Action Hub
- **Communication**: 전화(Call), 문자(SMS), 메일(Email), 메신저(KakaoTalk 등) 연동 제어.
- **Sensory**: 카메라(Photo/Video), 위치(GPS), 소음, 배터리 상태 실시간 수집 및 분석.
- **Autonomous Coder**: AI가 직접 파이썬 스크립트 작성 -> 테스트 -> 배포 -> 자기 치유(Self-Healing).

---

## 🛠 3. Tech Stack (기술 스택)

| 분류 | 상세 내용 |
| :--- | :--- |
| **Hardware** | Samsung Galaxy A35 (Exynos 1380 / ARM64) |
| **Environment** | Termux (Android Linux Environment) + Termux:API |
| **Languages** | C++ 20, Python 3.11+, Shell Script |
| **Core Engine** | BitNet b1.58 (1-bit Quantization LLM) |
| **Database** | SQLite3 (Logging, Caching, Memory) |

---

## 📈 4. Roadmap (로드맵)

### ✅ Phase 1: Infrastructure (완료)
- [x] Termux 최적화 및 SSH 통신 환경 구축
- [x] 텔레그램 봇 기반 명령 체계(Messenger) 및 보안(ID 필터링) 완성
- [x] 기본 물리 제어 핸들러(Limbs) 및 디렉토리 구조 확립

### 🚀 Phase 2: Intelligence & Brain Graft (진행 중)
- [ ] BitNet.cpp 안드로이드 NDK 빌드 및 1-bit LLM 이식
- [ ] 기기 온도/배터리 기반 동적 라우팅 알고리즘 구현
- [ ] SQLite 기반 시맨틱 캐싱(유사 질문 즉시 응답) 시스템 구축

### 📱 Phase 3: Physical Mastery (통신 및 제어 완성)
- [ ] **Communication Suite**: 텔레그램 메시지 분석을 통한 자동 전화/문자/메일 발송 기능.
- [ ] **System Control**: 앱 실행, 카톡 메시지 전송, 시스템 설정 변경 자동화.
- [ ] **Multi-Modal Action**: "사진 찍어서 내 위치랑 같이 보내"와 같은 복합 명령 수행 능력 확보.

### 🧬 Phase 4: Autonomous Coder (자가 진화)
- [ ] **Code Generation**: 사용자 요구사항에 맞는 Python 스크립트 자율 작성.
- [ ] **Sandboxed Execution**: 독립된 가상환경(Venv)에서 코드 실행 및 검증.
- [ ] **Self-Healing**: 실행 에러(Traceback) 발생 시 AI가 스스로 코드를 고쳐 재실행.

### 🌐 Phase 5: Total Evolution (완전한 독립)
- [ ] 외부망 차단 상태에서의 오프라인 독립 생존 테스트.
- [ ] 다른 기기들과 연동하는 분산 에이전트(Swarm) 환경 구축.
- [ ] 빅테크 API 대비 성능 및 비용 효율 데이터 백서 발간.

---

## 📝 5. Developer's Note
> "모두가 AI에게 코드를 '물어볼' 때, 나의 아메바는 코드를 직접 '작성하고 실행'한다.  
> 스마트폰은 더 이상 소모품이 아니라, 스스로 진화하는 지능의 요람이다."
