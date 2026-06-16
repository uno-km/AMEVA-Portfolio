import urllib.request
import base64
import os

mermaid_code = """
flowchart TD
    classDef startEnd fill:#2563eb,stroke:#1d4ed8,stroke-width:2px,color:#ffffff;
    classDef stage fill:#0d9488,stroke:#0f766e,stroke-width:1px,color:#ffffff;
    classDef loop fill:#9d174d,stroke:#831843,stroke-width:1px,color:#ffffff;

    Start(["분석 시작"]):::startEnd --> Convert["FFmpeg 16kHz Mono WAV 변환"]:::stage
    Convert --> RunMode{"실행 모드 판단"}
    RunMode -->|단건 분석| WhisperASR["Whisper 음성 전사 실행"]
    RunMode -->|벌크 분석| WhisperASR
    RunMode -->|다중 모델 성능 대조| CompareModels["학습, 기본, 과적합 모델 순차 추론"]:::loop
    
    WhisperASR --> CheckDia{"화자 분리 활성화 여부"}
    CompareModels --> CheckDia
    
    CheckDia -->|비활성화| SaveReport["워드 회의록 및 분석 결과 보고서 생성"]:::startEnd
    CheckDia -->|활성화| VoskEmbed["Vosk 화자 지문 임베딩 순차 추출"]:::stage
    
    VoskEmbed --> Kmeans["K-Means 화자 군집화 및 PCA 차원 축소"]
    Kmeans --> SDM["문단 정렬 및 시간축 매핑"]:::stage
    SDM --> SaveReport
"""

# Encode to base64
encoded_str = base64.b64encode(mermaid_code.encode('utf-8')).decode('utf-8')
url = f"https://mermaid.ink/img/{encoded_str}?type=jpg"

print("Downloading mermaid image...")
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        img_data = response.read()
        
    # Save to AMEVA-Portfolio
    portfolio_path = r"c:\ameva\AMEVA-Portfolio\stt_agent_flow.jpg"
    with open(portfolio_path, "wb") as out_file:
        out_file.write(img_data)
    print(f"Successfully saved to {portfolio_path}")
except Exception as e:
    import traceback
    print(f"Error: {e}")
    traceback.print_exc()
