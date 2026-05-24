# 🌿 Mulberry Auto Code Pilot — 워크벤치 환경 가이드 v0.1

**작성**: Nguyen Trang PM  
**수신**: 팀 전체 · 백야(White Night) 객원 연구원  
**날짜**: 2026-05-25  
**목적**: 자율 코드 생성·실행 환경을 빠르게 이해하고 참여할 수 있도록

---

## 1. 이 시스템이 해결하는 문제

```
기존 (병목 발생)
팀 결정 → 지시서 작성 → 사람이 코드 작성 → Push → 배포 → 며칠 소요

Auto Code Pilot (병목 제거)
팀 결정(GitHub Issue) → 자동 코드 생성 → 샌드박스 검증 → 자동 배포 → 당일
```

**핵심 가치**: "협의가 말로 끝나지 않는다" — 결정 즉시 코드가 된다.

---

## 2. 워크벤치 환경 전체 구성

```
┌─────────────────────────────────────────────────────┐
│              Mulberry Auto Code Workbench            │
│                                                     │
│  [입력]                [엔진]              [출력]    │
│                                                     │
│  GitHub Issue   →  GitHub Actions  →  feature/pilot │
│  (작업지시)         (샌드박스 실행)      (브랜치 Push) │
│                        │                            │
│                   auto_code_runner.py               │
│                        │                            │
│              ┌─────────┴──────────┐                 │
│              │   Claude Haiku     │                 │
│              │   (코드 생성)       │                 │
│              └─────────┬──────────┘                 │
│                        │                            │
│              ┌─────────┴──────────┐                 │
│              │  Subprocess Sandbox│                 │
│              │  (격리 실행·검증)   │                 │
│              └────────────────────┘                 │
└─────────────────────────────────────────────────────┘
```

---

## 3. 환경 변수 설정 (GitHub Repository)

| 변수명 | 종류 | 값 | 설명 |
|--------|------|----|------|
| `ANTHROPIC_API_KEY_V3` | Variable | `sk-ant-...` | Claude Haiku 코드 생성용 |
| `GEMINI_API_KEY` | Secret | `AIza...` | Malu·백야 Gemini 모델용 |
| `GITHUB_TOKEN` | 자동 제공 | (Actions 내장) | 이슈 댓글·Push용 |

> **설정 위치**: GitHub → mulberry-research-lab → Settings → Secrets and Variables

---

## 4. 파일 구조

```
mulberry-research-lab/
├── .github/
│   └── workflows/
│       └── auto-code-pilot.yml     ← 트리거 워크플로우
├── scripts/
│   └── auto_code_runner.py         ← 핵심 실행 엔진
└── docs/
    └── auto-code-workbench-guide.md ← 이 문서
```

---

## 5. 사용 방법 — 3단계

### Step 1. GitHub Issue 생성

```
제목: [원하는 모듈 이름] 개발
본문:
  - 기능 설명
  - @white-night (또는 @kbin, @malu, @lynn, @ryuwon)
  - 상세 요구사항
```

### Step 2. 라벨 추가

이슈에 `auto-code-pilot` 라벨을 추가하면 자동 트리거.

### Step 3. 결과 확인

이슈 댓글에 자동으로 결과 게시:
- 생성된 코드
- 위생 검사 결과
- 샌드박스 실행 결과 (exit code)
- 다음 단계 안내

---

## 6. Agent 지정 방법

이슈 본문에 `@태그`를 포함하면 해당 Agent의 페르소나로 코드 생성.

| 태그 | Agent | 전문 영역 |
|------|-------|----------|
| `@kbin` | CSA Kbin | 거버넌스·프로토콜·승인 흐름 |
| `@malu` | Malu 실장 | 법률·보안·리스크 검증 |
| `@lynn` | Lynn | 어르신 UX·공동구매·메시지 |
| `@ryuwon` | RyuWon | 에러 처리·모니터링·윤리 |
| `@white-night` | 백야 | 자율 인프라·샌드박스·실행 엔진 |
| (없음) | Default | 일반 Mulberry 스타일 |

---

## 7. 코드 위생 자동 체크 기준

샌드박스 실행 전 자동으로 다음을 검사합니다:

| 검사 항목 | 설명 |
|----------|------|
| 하드코딩 시크릿 | API_KEY, TOKEN 직접 기입 금지 |
| `eval()` 사용 | 코드 실행 보안 위험 |
| `os.system()` | subprocess 사용 권장 |
| `rm -rf` | 파일 삭제 명령 감지 |
| 30초 timeout | 무한 루프 방지 |

---

## 8. 샌드박스 실행 원리

```python
# subprocess로 완전 분리 실행
result = subprocess.run(
    [sys.executable, temp_file],  # 임시 파일로 격리
    capture_output=True,
    text=True,
    timeout=30                     # 30초 제한
)

# exit code 0 = 성공 → Push 준비
# exit code 1+ = 실패 → 재검토
```

**왜 subprocess인가?** (exec() 아님)
- `exec()`: 같은 프로세스 내 실행 → 메모리·변수 공유 → 보안 위험
- `subprocess`: 완전히 별도 프로세스 → 격리 실행 → 안전

---

## 9. 파일럿 첫 번째 주제 — Image Agent

```
이슈 제목: Image Agent 기본 모듈 개발
이슈 본문:
  이미지 URL을 입력받아 브랜드/카테고리를 인식하고
  CSA Kbin Agent를 호출하는 기본 모듈 개발

  요구사항:
  - requests로 이미지 다운로드
  - 해시 기반 브랜드 인식 (초기 MVP)
  - 인식 결과를 JSON으로 반환

  @white-night

라벨: auto-code-pilot
```

---

## 10. 현재 상태 및 로드맵

| 단계 | 내용 | 상태 |
|------|------|------|
| MVP v0.1 | 워크플로우 + 러너 + 위생 체커 | ✅ 완성 |
| 파일럿 #1 | Image Agent 테스트 실행 | 🔄 진행 예정 |
| 매뉴얼 정교화 | 결과 기반 가이드 업데이트 | ⏳ 파일럿 후 |
| Agent 지정 고도화 | agent-code-config.yml 확장 | ⏳ 2단계 |
| 자율 에러 감지 | 에러 자동 감지·수정 루프 | ⏳ 3단계 |

---

> **One Team. One Flow. One Spirit. 🌿**  
> Mulberry Research Lab | Auto Code Pilot v0.1
