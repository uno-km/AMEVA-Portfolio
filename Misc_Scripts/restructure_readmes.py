import os
import re
import subprocess

projects = [
    "AMEVA-Agent-Orchestra",
    "AMEVA-Benchmark-Suite",
    "AMEVA-Data-Harvester",
    "AMEVA-Dead-Internet-Threatre",
    "AMEVA-Doc-AI",
    "AMEVA-Edge-Agent",
    "AMEVA-STT-Agent",
    "AMEVA-STT-Trainer",
    "AMEVA-Window-Assistant",
    "AMEVA-Model-Nexus"
]

def strip_emojis(text):
    # Targets only standard emoji blocks (4-byte emojis and explicit symbol/dingbat blocks)
    # This leaves mathematical symbols ($$, \sum, etc.) and diagram flow arrows (-->) intact.
    pattern = re.compile(
        r'[\U00010000-\U0010FFFF'  # 4-byte emojis
        r'\u2600-\u26FF'          # Misc Symbols (hearts, smiles)
        r'\u2700-\u27BF]'         # Dingbats (checkmarks, warnings)
    )
    return pattern.sub('', text)

def clean_markdown_formatting(text):
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'\n+(##+ .*?)\n+', r'\n\n\1\n\n', text)
    return text.strip()

def get_original_readme_content(project_dir):
    # Find the longest version of README.md in the git history
    # Excluding our own latest "restructure README layout" commit to avoid loop feedback.
    try:
        result = subprocess.run(
            ["git", "log", "-n", "15", "--format=%H %s"],
            capture_output=True,
            cwd=project_dir,
            check=True
        )
        log_lines = result.stdout.decode("utf-8").splitlines()
    except Exception as e:
        print(f"Error getting git log for {project_dir}: {e}")
        return ""

    best_content = ""
    max_len = 0

    for line in log_lines:
        parts = line.split(" ", 1)
        commit_hash = parts[0]
        subject = parts[1] if len(parts) > 1 else ""

        if "restructure README" in subject:
            continue

        try:
            show_res = subprocess.run(
                ["git", "show", f"{commit_hash}:README.md"],
                capture_output=True,
                cwd=project_dir,
                check=True
            )
            content = show_res.stdout.decode("utf-8")
            
            # The original detailed README is significantly longer than the summarized ones
            if len(content) > max_len:
                max_len = len(content)
                best_content = content
        except Exception:
            continue

    return best_content

nexus_summary_content = """> **[프로젝트 요약 (Resume Profile)]**
> 
> * **① 제목:** 분산형 LLM API 게이트웨이 및 워커 클러스터 (AMEVA Model Nexus)
> * **② 주제:** 
>   * 단일 노드의 물리적 하드웨어 한계를 극복하기 위해 다중 Docker 컨테이너 워커(Worker)와 라우팅 게이트웨이(Router)를 연동한 무중단 분산 LLM 서빙 플랫폼
>   * 큐(Queue) 버퍼링 메커니즘을 적용하여 모델 교체(Hot-swap)나 노드 장애 시에도 요청 연결 유실률 0%를 달성하는 고신뢰성 라우팅 설계
>   * CUDA GPU 가속 워커와 CPU 전용 워커를 능동 감지하여 요청을 로드밸런싱하는 아키텍처 실증
> * **③ 내용요지:**
>   * **사용 기술:** FastAPI 기반 라우터 API, Asyncio Queue 비동기 처리, Docker Compose 클러스터 오케스트레이션, SQLite WAL 모드 중앙 로깅
>   * **사용 모델:** Llama-3-8B-GGUF (GPU 워커 메인 추론), Qwen2.5-3B-GGUF (CPU 워커 보조 추론)
>   * **핵심 알고리즘:** 비동기 큐 기반의 무중단 핫스왑(Hot-Swap) 및 동적 스왑 지연 방어 메커니즘, Python gc.collect() 강제를 통한 VRAM 누수 및 단편화 방지 알고리즘, Hardware-Aware 동적 디스패칭 로드밸런서
>   * **에이전트/보안 제어 (또는 핵심 아키텍처 흐름):** Gateway 인입 -> SQLite Queue 버퍼 상태 전이 -> 대상 워커 Poll 작업 할당 -> SSE(Server-Sent Events) 스트리밍 토큰 반환 -> 완료 시 WAL 로거 아티팩트 보존 흐름
>   * **연구 성과:** 도커 격리 기반의 무중단 모델 교체 파이프라인을 구축하여 VRAM 오버플로우와 모델 교체 시 커넥션 끊김 문제를 하드웨어 단독 서버 제약 하에서 완벽히 해결함
> * **④ 기여도:** 단독 개발 (100% - 아키텍처 설계, 보안 시스템 구축, 코어 로직 구현 전담)

---

## 1. 프로젝트 목적 및 필요성

본 프로젝트는 단일 엣지 디바이스 또는 제한된 서버 인프라에서 발생하는 메모리 병목 및 추론 지연을 극복하기 위한 경량 API 게이트웨이 및 분산 워커 클러스터 플랫폼입니다. 

워커와 라우터를 비동기 큐와 DB 트랜잭션으로 격리함으로써 장애 전파를 방지하고, 실행 중단 없는 무중단 모델 교체(Zero-Downtime Hot-Swap)를 구현하여 로컬 가용성을 오프라인 환경에 맞게 제공하는 것을 목적으로 합니다.

---

## 2. 주요 기능 및 연구 목표

* **무중단 동적 가중치 스와핑**: API 게이트웨이 구동 중에도 요청 흐름의 단절 없이 새로운 GGUF 모델로 즉각 대체할 수 있는 동적 핫스왑 대기열을 제공합니다.
* **비동기 큐 버퍼링 및 장애 격리**: 특정 추론 노드(Worker)가 비정상 다운되거나 통신이 두절될 경우, 인입된 API 요청을 PENDING 큐에 임시 적재하여 노드가 복구되는 즉시 재중계함으로써 트래픽 연결 유실률 0%를 보장합니다.
* **Hardware-Aware 지능형 로드밸런싱**: 다중 Docker 컨테이너 워커들의 CUDA 사용 가능 여부를 자동 진단하여, 무거운 연산(8B 모델)은 GPU 워커로, 가벼운 대화(3B 모델)는 CPU 워커로 동적 로드밸런싱합니다."""

harvester_summary_content = """> **[프로젝트 요약 (Resume Profile)]**
> 
> * **① 제목:** 엣지 디바이스 기반 주기적 데이터 수집 및 자동화 파이프라인 (AMEVA-Data-Harvester)
> * **② 주제:** 
>   * 안드로이드 쉘 및 Python 환경의 엣지 디바이스에서 주기적으로 통화 음성 파일을 수집하여 로컬 STT와 소형 LLM으로 전사 및 요약·번역을 선제 처리한 뒤 메인 서버로 전송하는 파이프라인 구축
>   * 불안정한 네트워크 상태에 대비하여 메인 서버 전송 시 3~4가지의 다중 우회 전송 경로(SSH/SCP, API, Telegram 등)와 워크어라운드 체계 설계
>   * 데이터 수집 및 가공 과정을 엣지단에서 전담 처리하여 서버 부하를 경감시키는 엣지 컴퓨팅 아키텍처의 성능 신뢰성과 물리적 한계점을 계측/분석하기 위한 프로젝트
> * **③ 내용요지:**
>   * **사용 기술:** Python, Android Shell, STT Engine, SLM (소형 LLM), Network Protocols (SSH/SCP, HTTP API, Telegram API)
>   * **사용 모델:** Whisper (Small) (STT), Qwen (1.8B), Phi-3 (3B), Llama-3.1 (8B) (LLM)
>   * **핵심 알고리즘:** 통화 내역의 오프라인 텍스트 전사 및 소형 LLM 기반 요약·번역 알고리즘, 전송 실패 방지를 위한 3~4단계 다중 우회 전송 라우팅(PAC 아키텍처), 엣지 디바이스 스냅샷 기반 주기적 데이터 수집 스케줄러
>   * **에이전트/보안 제어 (또는 핵심 아키텍처 흐름):** 안드로이드 쉘/파이썬 기반 주기적 음성 파일 감지 -> 로컬 STT 및 SLM 구동 -> 텍스트 전사, 요약 및 한국어 번역 가공 -> ZIP 압축 패키징 -> 3~4가지 우회 경로를 통한 순차 전송 시도 -> 전송 성공 확인 후 로컬 잔여 데이터의 안전 소거 흐름
>   * **연구 성과:** 엣지 디바이스 환경에서 데이터 전처리를 완수하여 서버 대역폭 부하를 최소화했으며, 기기 사양별 한계 측정 실험(저성능 기기인 Galaxy A35 환경에서는 VRAM 및 연산 리소스 한계로 프로세스가 지연되었으나, 고성능 기기인 Galaxy S20 환경에서는 무중단으로 안정적으로 STT-LLM 요약 및 다중 우회 전송 완료)을 통해 기기별 실효성 검증
> * **④ 기여도:** 단독 개발 (100% - 아키텍처 설계, 보안 시스템 구축, 코어 로직 구현 전담)

---

## 1. 프로젝트 목적 및 필요성

본 프로젝트는 특정 도메인(보안 데이터 및 원격 통신)에 특화된 데이터 획득 및 전송(Harvester) 시스템을 구축하기 위한 엔드투엔드 파이프라인입니다. 

디렉토리 기반 아키텍처(DB 미사용)를 채택하였으며, 파일 수집의 자동화, O(1) 배치 폴링 전처리 알고리즘, 3단계 PAC를 활용한 효율적 통신망 어댑테이션, 그리고 ZIP 해시 검증을 통한 최적화된 파일 무결성 과정을 포함합니다.

---

## 2. 주요 기능 및 연구 목표

* **파일 수집 및 폴링 자동화**: O(1) 배치 폴링 전처리 알고리즘을 도입하여 엣지 단에서 주기적으로 신규 데이터를 자동 감지하고 이송합니다.
* **3단계 PAC 우회 라우팅**: 메인 서버 전송 실패 시 SSH(Primary), API(Alternate), Telegram(Contingency)의 다중 통신망 어댑터를 통해 전송 흐름의 조난을 막고 보존합니다.
* **로컬 경량 연산 전처리**: 모바일 엣지 기기 내부에서 Whisper 및 소형 SLM을 가동하여 전사 및 핵심 요약을 선제 완료한 뒤, 경량 텍스트 패키지만을 전송해 서버 네트워크 부하를 경감시킵니다."""

def merge_readme(project_name):
    project_dir = f"c:\\ameva\\{project_name}"
    current_path = os.path.join(project_dir, "README.md")
    
    if not os.path.exists(current_path):
        print(f"Skipping {project_name}: local README.md not found")
        return
        
    print(f"Merging README for: {project_name}")
    
    # 1. Retrieve the best (longest original) README content from Git history
    original_content = get_original_readme_content(project_dir)
    if not original_content:
        # Fallback to current filesystem if git retrieval fails completely
        try:
            with open(current_path, "r", encoding="utf-8") as f:
                original_content = f.read()
        except Exception as e:
            print(f"Error fallback reading {current_path}: {e}")
            return
            
    original_lines = original_content.splitlines(keepends=True)
    
    # Read current local README to fetch localized summary sections
    try:
        with open(current_path, "r", encoding="utf-8") as f:
            current_content = f.read()
    except Exception as e:
        print(f"Error reading local README: {e}")
        return
        
    # Extract the main title (# ...) from original README
    title_line = ""
    for line in original_lines:
        if line.strip().startswith("# "):
            title_line = line.strip()
            break
    if not title_line:
        title_line = f"# {project_name}"
        
    # Find the starting index of the first '##' header in original README
    split_index = -1
    for i, line in enumerate(original_lines):
        if line.strip().startswith("## "):
            split_index = i
            break
            
    # Extract original detailed body (from the first ## header onward)
    original_detail_body = ""
    if split_index != -1:
        original_detail_body = "".join(original_lines[split_index:])
    else:
        original_detail_body = "".join([l for l in original_lines if not l.strip().startswith("# ")])
        
    # Construct summary part
    if project_name == "AMEVA-Model-Nexus":
        summary_part = f"{title_line}\n\n{nexus_summary_content}\n\n---\n\n"
    elif project_name == "AMEVA-Data-Harvester":
        summary_part = f"{title_line}\n\n{harvester_summary_content}\n\n---\n\n"
    else:
        # Extract headers and body from current README
        resume_profile = ""
        purpose_sec = ""
        features_sec = ""
        
        resume_match = re.search(r'(> \*\*\[프로젝트 요약.*?\n)(?=\n---|\n## |\Z)', current_content, re.DOTALL)
        if resume_match:
            resume_profile = resume_match.group(1).strip()
            
        purpose_match = re.search(r'(## 1\. 프로젝트 목적.*?)(?=\n---|\n## 2\.|\Z)', current_content, re.DOTALL)
        if purpose_match:
            purpose_sec = purpose_match.group(1).strip()
            
        features_match = re.search(r'(## 2\. 주요 기능.*?)(?=\n---|\n## 3\.|\Z)', current_content, re.DOTALL)
        if features_match:
            features_sec = features_match.group(1).strip()
            
        summary_part = f"{title_line}\n\n"
        if resume_profile:
            summary_part += f"{resume_profile}\n\n"
        summary_part += "---\n\n"
        if purpose_sec:
            summary_part += f"{purpose_sec}\n\n"
        if features_sec:
            summary_part += f"{features_sec}\n\n"
        summary_part += "---\n\n"
        
    # Combine summary part + original detailed body
    full_content = summary_part + original_detail_body
    
    # 1. Strip emojis safely (does not affect sum, arrays, limits, and arrow structures)
    full_content = strip_emojis(full_content)
    
    # 2. Re-index headers from original_detail_body to continue from 3.
    lines = full_content.split('\n')
    header_counter = 3
    final_lines = []
    in_original_body = False
    
    for line in lines:
        stripped = line.strip()
        if not in_original_body and split_index != -1 and stripped.startswith("## ") and not stripped.startswith("## 1. 프로젝트 목적") and not stripped.startswith("## 2. 주요 기능"):
            in_original_body = True
            
        if in_original_body and stripped.startswith("## "):
            match = re.match(r'^##\s+(\d+(?:\.\d+)*)?\.?\s*(.*)$', stripped)
            if match:
                num_part = match.group(1)
                text_part = match.group(2)
                if num_part and '.' in num_part:
                    parts = num_part.split('.')
                    parts[0] = str(header_counter)
                    new_num = ".".join(parts)
                    line = f"## {new_num}. {text_part}"
                elif num_part:
                    line = f"## {header_counter}. {text_part}"
                    header_counter += 1
                else:
                    line = f"## {header_counter}. {text_part}"
                    header_counter += 1
            else:
                line = f"## {header_counter}. {stripped[3:]}"
                header_counter += 1
                
        final_lines.append(line)
        
    full_content = "\n".join(final_lines)
    
    # 3. Add Contact section as Section 9
    contact_section = f"""
## 9. 연락처 (Contact)

저는 Multi-Agent Systems, Edge Computing, 그리고 AI SRE 분야에 대한 학술적 담론을 언제나 환영합니다.

- **GitHub**: [@uno-km](https://github.com/uno-km)
- **Email**: zhfldk014745@naver.com
- **Tstory**: [my-blog](https://uno-kim.tistory.com/)
- **Research Focus**: Hierarchical AI Orchestration, Edge-native Inference, Data Sovereignty
- **Generated by AMEVA Researcher Portfolio Builder**

*Last Updated: June 9, 2026*
"""
    philosophy_footer = """
---

<sub>*빅테크의 클라우드 종속을 거부하고, 온프레미스 자율 지능의 독립과 생존을 실증합니다.*</sub>
"""
    
    full_content = clean_markdown_formatting(full_content)
    full_content += "\n" + contact_section + "\n" + philosophy_footer
    full_content = clean_markdown_formatting(full_content) + "\n"
    
    # Write back to README.md
    with open(current_path, "w", encoding="utf-8") as f:
        f.write(full_content)
        
    print(f"Successfully merged and updated with UTF-8: {current_path}")

if __name__ == "__main__":
    for p in projects:
        merge_readme(p)
