# AMEVA STT 관련 프로젝트 요약 (Resume Profiles)

이 문서는 `AMEVA-STT-Agent`와 `AMEVA-STT-Trainer` 프로젝트의 개별 프로젝트 요약(Resume Profile)을 한데 모아놓은 문서입니다.

---

## 1. AMEVA STT Agent 요약 프로필

> **[프로젝트 요약 (Resume Profile)]**
> 
> * **제목:** Whisper-Vosk 하이브리드 화자 분리 및 전사 엔진 (AMEVA STT Agent)
> * **주제:** 
>   * 엣지/모바일 환경에서 외부 클라우드 의존성 없이 로컬 오프라인만으로 고정밀 음성 인식 및 다중 화자 식별 대시보드를 통합 구축 지향
>   * `Streamlit` 프론트엔드, `STTPipeline` 코어 오케스트레이터, `whisper.cpp` 디코딩 프로세스, `Vosk` 임베딩, 그리고 SQLite3 영속성 로거 간의 유기적 협업 구현
>   * 모바일 OS(Termux) 환경 우회, 다중 화자 VAD 분할 딜레이, 그리고 CPU 스레드 과부하로 인한 대시보드 무반응 문제를 방지하기 위한 비동기 제어 구조 구현
> * **내용 요지:**
>   * **사용 기술:** `Python 3.12`, `Streamlit`, `vosk` (python-vosk), `pywhispercpp`, `plotly`, `pandas`, `tkinter`, `matplotlib`, `yt_dlp`, `sqlite3`, `wave`
>   * **핵심 알고리즘:** 화자 인격 임베딩 벡터 간의 `cosine_similarity` 산출, 다차원 임베딩 축소를 위한 멱반복법(`Power Iteration`) 기반 2D `PCA` 변환 및 `K-Means Clustering` 화자 군집화, 문맥 분할을 위한 Whisper `VAD` 제어, 타임라인 오차 제한을 위한 `시간차 최소화 정렬 매핑`
>   * **에이전트/보안 제어 (또는 핵심 아키텍처 흐름):** 사용자 오디오 업로드 또는 유튜브 주소 유입 -> subprocess 경유 `whisper.cpp` 구동 및 임계 길이 단위 세그먼트 전사 -> wave 모듈 및 `Vosk` spk_model 결합을 통한 X-Vector 화자 임베딩 생성 -> K-Means Clustering 군집 분석 및 PCA 좌표 사영 -> 임베딩 중심값(Centroid) 도출 -> 시간차 및 코사인 유사도 기준 Whisper-Vosk 인터벌 교차 정렬 -> SQLite3 히스토리/에러 감사 로그 적재 -> Streamlit 대시보드 시각화 및 Word 회의록 출력 흐름
>   * **연구 성과:** `sys.platform = 'linux'` bypass 구조를 이식해 모바일 터미널(Termux)에서도 동일 인퍼런스 파이프라인을 온전히 실현하고, 시간 최소화 정렬 매핑 알고리즘을 도입해 단락별 화자 지정 매칭 신뢰도 대폭 증가
> * **기여도:** 단독 개발 (100% - 아키텍처 설계, 보안 시스템 구축, 코어 로직 구현 전담)

---

## 2. AMEVA STT Trainer 요약 프로필

> **[프로젝트 요약 (Resume Profile)]**
> 
> * **제목:** Windows CPU 최적화 Whisper LoRA 파인튜닝 플랫폼 (AMEVA STT Trainer)
> * **주제:** 
>   * 척박한 로컬 윈도우 CPU 가속 환경 하에서 대용량 한국어 오디오 및 자막 코퍼스를 기반으로 Whisper 모델의 LoRA 파인튜닝 및 배포용 포맷 변환 자동화 지향
>   * `01_build_dataset` 파싱 엔진, `02_start_training` 트랜스포머 루프, `03_export_model` LoRA 어댑터 병합 모듈, GGUF 변환기 간의 파이프라인 협업 구현
>   * 윈도우 커널의 메모리 맵핑 제한(`WinError 87`), 멀티프로세싱 Pickling 충돌, 그리고 오디오 디코딩 라이브러리 비호환성 문제를 해결하기 위해 격리형 아키텍처 구현
> * **내용 요지:**
>   * **사용 기술:** `Python 3.12`, `torch`, `torchaudio`, `transformers`, `peft` (LoRA), `datasets`, `accelerate`, `evaluate`, `jiwer`, `librosa`, `soundfile`, `pydub`, `yt-dlp`, `gguf`, `psutil`, `win10toast`
>   * **핵심 알고리즘:** 가중치 행렬 경량 파인튜닝을 위한 `LoRA` 학습 알고리즘, 메모리 맵 충돌을 방지하는 `IterableDataset` 스트리밍 데이터 로더 제어, soundfile/librosa 기반 오디오 리샘플링 전처리, 모델 가중치 병합(`peft.PeftModel.merge_and_unload`), `GGUF` 모델 양자화 및 바이너리 직렬화
>   * **에이전트/보안 제어 (또는 핵심 아키텍처 흐름):** yt-dlp 활용 학습용 미디어 취득 및 webvtt-py 싱크 정렬 -> metadata.csv 구축 -> IterableDataset 기반 캐싱 없는 스트리밍 토크나이저 초기화 -> LoRA 파인튜닝 진행 및 체크포인트 체크 -> lora_weights 저장 -> 베이스 Whisper 모델과 LoRA 어댑터 가중치 병합 -> gguf 스크립트를 통한 4-bit 양자화 바이너리 내보내기 흐름
>   * **연구 성과:** 스트리밍 학습 모델 및 pin_memory 해제 설정을 구현하여 윈도우 CPU 단독 환경에서도 OOM 크래시나 매개변수 오류(`WinError 87`) 없이 LoRA 학습의 무한 가용성을 입증하고, LoRA 병합-GGUF 변환 연계를 통한 추론 속도 극대화
> * **기여도:** 단독 개발 (100% - 아키텍처 설계, 보안 시스템 구축, 코어 로직 구현 전담)
