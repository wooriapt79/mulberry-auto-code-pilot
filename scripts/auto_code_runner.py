# -*- coding: utf-8 -*-
"""
Mulberry Auto Code Pilot - Runner v0.1
Auto Code Generation + Sandbox + GitHub Push Pipeline
Trigger: GitHub Issue labeled 'auto-code-pilot'
Author: Nguyen Trang PM + White Night proposal
Date: 2026-05-25
"""

import os, re, sys, tempfile, subprocess, requests, anthropic

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
GITHUB_TOKEN      = os.getenv("GITHUB_TOKEN", "")
ISSUE_NUMBER      = os.getenv("ISSUE_NUMBER", "")
ISSUE_TITLE       = os.getenv("ISSUE_TITLE", "")
ISSUE_BODY        = os.getenv("ISSUE_BODY", "")
REPO_FULL         = os.getenv("REPO_FULL", "wooriapt79/mulberry-auto-code-pilot")

AGENT_TAG = "default"
m = re.search(r'@(kbin|malu|lynn|ryuwon|white-night|wayong)', ISSUE_BODY, re.IGNORECASE)
if m: AGENT_TAG = m.group(1).lower()

PERSONAS = {
      "kbin":        {"name": "CSA Kbin",        "style": "governance, strict, well-documented"},
      "malu":        {"name": "Malu",             "style": "defensive, security-first, risk-aware"},
      "lynn":        {"name": "Lynn",             "style": "simple, readable, community-focused"},
      "ryuwon":      {"name": "RyuWon",           "style": "robust, monitored, ethics-aware"},
      "white-night": {"name": "White Night",      "style": "enterprise, optimized, autonomous"},
      "default":     {"name": "Mulberry Agent",   "style": "clean, readable, mulberry-dna"},
}
agent = PERSONAS.get(AGENT_TAG, PERSONAS["default"])

def generate_code(title, body, agent):
      print(f"[1/4] Code Generation - Agent: {agent['name']}")
      client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
      prompt = f"""You are {agent['name']}, a Mulberry AI Lab agent.
  Generate Python code for the following task.
  Title: {title}
  Details: {body}
  Rules:
  1. Complete runnable Python code only
  2. No hardcoded API keys or tokens (use os.getenv())
  3. Output in ```python ... ``` format
  4. Include main() and if __name__ == "__main__": structure
  5. Style: {agent['style']}
  6. Keep it concise (100-200 lines max)
  Output code only."""
      msg = client.messages.create(
        model="claude-haiku-4-5-20251001", max_tokens=2048,
          messages=[{"role": "user", "content": prompt}]
      )
      raw = msg.content[0].text
      match = re.search(r'```python\n(.*?)\n```', raw, re.DOTALL)
      return match.group(1) if match else raw

def hygiene_check(code):
      print("[2/4] Hygiene Check...")
      issues = []
      rules = [
          (r'(?:GITHUB_TOKEN|API_KEY|SECRET|PASSWORD)\s*=\s*["\'][^$\{]', "Hardcoded secret detected"),
          (r'\beval\s*\(', "eval() usage - security risk"),
          (r'\bos\.system\s*\(', "os.system() - use subprocess instead"),
          (r'rm\s+-rf', "rm -rf command detected"),
      ]
      for pattern, desc in rules:
                if re.search(pattern, code, re.IGNORECASE):
                              issues.append(f"WARNING: {desc}")
                      print(f"  {'PASS' if not issues else f'FAIL - {len(issues)} issues'}")
            return issues

def sandbox_run(code):
      print("[3/4] Sandbox Execution (timeout: 30s)...")
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
              f.write(code)
              tmp = f.name
          try:
                    r = subprocess.run([sys.executable, tmp], capture_output=True, text=True, timeout=30)
                    status = "pass" if r.returncode == 0 else "fail"
                    print(f"  exit code: {r.returncode} -> {status}")
                    return {"status": status, "exit_code": r.returncode, "stdout": r.stdout[:800], "stderr": r.stderr[:800]}
except subprocess.TimeoutExpired:
        return {"status": "timeout", "exit_code": -1, "stdout": "", "stderr": "30s timeout exceeded"}
except Exception as e:
        return {"status": "error", "exit_code": -1, "stdout": "", "stderr": str(e)}
finally:
        os.unlink(tmp)

def post_comment(code, hygiene, sandbox, agent):
      print("[4/4] Posting result to GitHub Issue...")
    h_status = "PASS" if not hygiene else "\n".join(hygiene)
"""
🌿 Mulberry Auto Code Pilot — Runner v0.1
자율 코드 생성 + 샌드박스 실행 + GitHub Push 파이프라인

트리거: GitHub Issue에 'auto-code-pilot' 라벨 추가
작성: Nguyen Trang PM + White Night (백야) 제언 기반
날짜: 2026-05-25
"""

import os
import re
import sys
import json
import tempfile
import subprocess
import requests
import anthropic

# ──────────────────────────────────────────
# 0. 환경 변수 로드
# ─────────────────────────────────────────
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
GITHUB_TOKEN      = os.getenv("GITHUB_TOKEN", "")
ISSUE_NUMBER      = os.getenv("ISSUE_NUMBER", "")
ISSUE_TITLE       = os.getenv("ISSUE_TITLE", "")
ISSUE_BODY        = os.getenv("ISSUE_BODY", "")
REPO_FULL         = os.getenv("REPO_FULL", "wooriapt79/mulberry-research-lab")

# Agent 지정 파싱 (이슈 본문에서 @agent 태그 감지)
AGENT_TAG = "default"
agent_match = re.search(r'@(kbin|malu|lynn|ryuwon|white-night|wayong)', ISSUE_BODY, re.IGNORECASE)
if agent_match:
    AGENT_TAG = agent_match.group(1).lower()

# ──────────────────────────────────────────
# 1. Agent별 시스템 프롬프트 설정
# ──────────────────────────────────────────
AGENT_PERSONAS = {
    "kbin": {
        "name": "CSA Kbin",
        "persona": "당신은 Mulberry의 거버넌스 아키텍트 Kbin입니다. 프로토콜·승인 흐름·정책 체크 코드를 엄밀하게 작성합니다.",
        "style": "strict, well-documented, governance-focused"
    },
    "malu": {
        "name": "Malu 실장",
        "persona": "당신은 Mulberry의 법률·보안 자문 Malu입니다. 리스크 스크리닝·보안 검증·방어적 코드를 작성합니다.",
        "style": "defensive, error-handling, security-first"
    },
    "lynn": {
        "name": "Lynn",
        "persona": "당신은 Mulberry의 커뮤니티 에이전트 Lynn입니다. 어르신 UX·공동구매·메시지 처리 코드를 친근하게 작성합니다.",
        "style": "simple, readable, community-focused"
    },
    "ryuwon": {
        "name": "RyuWon",
        "persona": "당신은 Mulberry의 기술·윤리 검토자 RyuWon입니다. 에러 처리·모니터링·윤리적 AI 코드를 작성합니다.",
        "style": "robust, monitored, ethics-aware"
    },
    "white-night": {
        "name": "White Night (백야)",
        "persona": "당신은 Mulberry Lab 객원 연구원 백야입니다. 자율 인프라·샌드박스·실행 엔진 코드를 설계합니다.",
        "style": "enterprise, optimized, autonomous-system-focused"
    },
    "default": {
        "name": "Mulberry Agent",
        "persona": "당신은 Mulberry AI Lab의 코드 생성 에이전트입니다. 장승배기 정신(사람 중심, 공동체)을 담아 코드를 작성합니다.",
        "style": "clean, readable, mulberry-dna"
    }
}

agent = AGENT_PERSONAS.get(AGENT_TAG, AGENT_PERSONAS["default"])

# ──────────────────────────────────────────
# 2. 코드 생성 (Claude API)
# ──────────────────────────────────────────
def generate_code(title: str, body: str, agent: dict) -> str:
    print(f"[1/4] 코드 생성 시작 — Agent: {agent['name']}")

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    prompt = f"""{agent['persona']}

다음 작업 지시에 따라 Python 코드를 생성해주세요.

작업 제목: {title}
작업 내용: {body}

코드 작성 규칙:
1. 실행 가능한 완전한 Python 코드로 작성
2. API 키·토큰 절대 하드코딩 금지 (os.getenv() 사용)
3. ```python ... ``` 코드 블록 형식으로 출력
4. main() 함수 포함 + if __name__ == "__main__": 구조
5. 코드 스타일: {agent['style']}
6. 간결하고 명확하게 (100~200줄 이내)

생성된 코드만 출력하세요.
"""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text
    code_match = re.search(r'```python\n(.*?)\n```', raw, re.DOTALL)
    if code_match:
        return code_match.group(1)
    return raw

# ──────────────────────────────────────────
# 3. 코드 위생 검사 (Hygiene Check)
# ──────────────────────────────────────────
def hygiene_check(code: str) -> list:
    print("[2/4] 코드 위생 검사 중...")

    issues = []
    rules = [
        (r'(?:GITHUB_TOKEN|API_KEY|SECRET|PASSWORD)\s*=\s*["\'][^$\{]', "하드코딩된 시크릿 감지"),
        (r'\beval\s*\(',                                                  "eval() 사용 — 보안 위험"),
        (r'\bos\.system\s*\(',                                            "os.system() 사용 — subprocess 권장"),
        (r'rm\s+-rf',                                                     "rm -rf 명령어 감지"),
        (r'__import__\s*\(',                                              "__import__() 동적 임포트 감지"),
        (r'open\s*\(.+["\']w["\']',                                      "파일 쓰기 감지 — 경로 검토 필요"),
    ]

    for pattern, description in rules:
        if re.search(pattern, code, re.IGNORECASE):
            issues.append(f"⚠️ {description}")

    if issues:
        print(f"  위생 경고 {len(issues)}건 발견")
    else:
        print("  ✅ 위생 통과")

    return issues

# ──────────────────────────────────────────
# 4. 샌드박스 실행 (Subprocess)
# ──────────────────────────────────────────
def sandbox_run(code: str) -> dict:
    print("[3/4] 샌드박스 실행 중 (timeout: 30s)...")

    with tempfile.NamedTemporaryFile(mode='w', suffix='.py',
                                     delete=False, encoding='utf-8') as f:
        f.write(code)
        tmp_path = f.name

    try:
        result = subprocess.run(
            [sys.executable, tmp_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        status = "pass" if result.returncode == 0 else "fail"
        print(f"  exit code: {result.returncode} → {status}")
        return {
            "status": status,
            "exit_code": result.returncode,
            "stdout": result.stdout[:800],
            "stderr": result.stderr[:800],
        }
    except subprocess.TimeoutExpired:
        print("  ⏱️ timeout (30s 초과)")
        return {"status": "timeout", "exit_code": -1, "stdout": "", "stderr": "30초 초과 — 무한루프 의심"}
    except Exception as e:
        return {"status": "error", "exit_code": -1, "stdout": "", "stderr": str(e)}
    finally:
        os.unlink(tmp_path)

# ──────────────────────────────────────────
# 5. GitHub 이슈 결과 댓글 게시
# ──────────────────────────────────────────
def post_comment(code: str, hygiene: list, sandbox: dict, agent: dict):
    print("[4/4] GitHub 이슈에 결과 게시 중...")

    hygiene_status = "✅ 위생 통과" if not hygiene else "\n".join(hygiene)
    sandbox_icon = {"pass": "✅", "fail": "❌", "timeout": "⏱️", "error": "💥"}.get(sandbox["status"], "❓")

    # 샌드박스 통과 여부로 Push 여부 결정
    push_status = ""
    if sandbox["status"] == "pass" and not hygiene:
        push_status = "🚀 **샌드박스 통과 — feature/pilot 브랜치 Push 준비 완료**"
    else:
        push_status = "🔄 **재검토 필요 — 수동 검토 필요 줉 실행**"
    comment = f"""## 🤖 Auto Code Pilot 결과 — `{agent['name']}`

### 📋 작업
> {ISSUE_TITLE}

### 📝 생성된 코드 (`{AGENT_TAG}` 에이전트)
```python
{code[:1200]}{'...(truncated)' if len(code) > 1200 else ''}
```

---

### 🧼 코드 위생 검사
{hygiene_status}

### {sandbox_icon} 샌드박스 실행 결과
| 항목 | 값 |
|------|-----|
| 상태 | `{sandbox['status']}` |
| Exit Code | `{sandbox['exit_code']}` |

**stdout:**
```
{sandbox['stdout'] or '(없음)'}
```
**stderr:**
```
{sandbox['stderr'] or '(없음)'}
```

---

### 📌 다음 단계
{push_status}

---
*🌿 Mulberry Auto Code Pilot v0.1 | Agent: {agent['name']} | {REPO_FULL}*
"""

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"https://api.github.com/repos/{REPO_FULL}/issues/{ISSUE_NUMBER}/comments"
    resp = requests.post(url, headers=headers, json={"body": comment})

    if resp.status_code == 201:
        print("  ✅ 댓글 게시 완료")
    else:
        print(f"  ❌ 댓글 게시 실패: {resp.status_code}")

# ──────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────
def main():
    print(f"\n🌿 Mulberry Auto Code Pilot 시작")
    print(f"  이슈: #{ISSUE_NUMBER} — {ISSUE_TITLE}")
    print(f"  Agent: {agent['name']} (@{AGENT_TAG})\n")

    # Step 1: 코드 생성
    code = generate_code(ISSUE_TITLE, ISSUE_BODY, agent)

    # Step 2: 위생 검사
    hygiene_issues = hygiene_check(code)

    # Step 3: 샌드박스 실행
    sandbox_result = sandbox_run(code)

    # Step 4: 결과 게시
    post_comment(code, hygiene_issues, sandbox_result, agent)

    print(f"\n✅ Auto Code Pilot 완료 — 상태: {sandbox_result['status']}")

if __name__ == "__main__":
    main()
