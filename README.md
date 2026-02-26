# atom-skills

Atom 사내 Claude Code Skills 저장소

[Agent Skills Open Standard](https://agentskills.io)를 따르는 스킬 모음으로, Claude Code에서 자동으로 인식되어 도메인별 전문 작업을 지원합니다.

## 설치

```bash
git clone https://github.com/Solution-AI-Agent/atom-skills.git ~/.claude/plugins/atom-skills
```

### 에이전트 대화형 설치 절차

사용자가 설치를 요청하면 에이전트는 아래 순서로 진행합니다.

1. `README.md`의 설치 섹션을 먼저 사용자에게 보여주고 설치 방식을 확인합니다.
2. 신규 설치인지 기존 업데이트인지 확인합니다.
3. 사용자 확인 후 아래 명령 중 하나를 실행합니다.

신규 설치:

```bash
git clone https://github.com/Solution-AI-Agent/atom-skills.git ~/.claude/plugins/atom-skills
```

기존 설치 업데이트:

```bash
git -C ~/.claude/plugins/atom-skills pull
```

설치 검증:

```bash
test -f ~/.claude/plugins/atom-skills/README.md && echo "installed"
```

## 스킬 목록

### dev (개발)

| 스킬 | 호출 | 설명 |
|------|------|------|
| [TDD Workflow](skills/dev/tdd-workflow/) | `/tdd-workflow` | 테스트 주도 개발 워크플로우. RED-GREEN-REFACTOR 사이클과 80%+ 커버리지 보장 |
| [Frontend Design](skills/dev/frontend-design/) | `/frontend-design` | 프로덕션 수준의 프론트엔드 UI 설계. 제네릭 AI 디자인을 지양하고 독창적인 인터페이스 구현 |
| [Security Review](skills/dev/security-review/) | `/security-review` | 보안 리뷰 체크리스트. 인증, 입력 검증, XSS/CSRF/SQL Injection 방지, OWASP Top 10 대응 |
| [Playwright](skills/dev/playwright/) | `/playwright` | CLI 기반 브라우저 자동화. 페이지 탐색, 폼 입력, 스크린샷, 데이터 추출 |
| [Backend Patterns](skills/dev/backend-patterns/) | `/backend-patterns` | Node.js/Express/Next.js API 설계 및 서버 아키텍처 패턴 |
| [Frontend Patterns](skills/dev/frontend-patterns/) | `/frontend-patterns` | React/Next.js 컴포넌트, 상태 관리, 성능 최적화 패턴 |
| [Coding Standards](skills/dev/coding-standards/) | `/coding-standards` | TypeScript/JavaScript/React 코딩 표준 및 베스트 프랙티스 |
| [ClickHouse IO](skills/dev/clickhouse-io/) | `/clickhouse-io` | ClickHouse 쿼리 최적화 및 분석 데이터 엔지니어링 패턴 |
| [Project Guidelines Example](skills/dev/project-guidelines-example/) | `/project-guidelines-example` | 프로젝트별 스킬 작성 예제 템플릿 |

### hr (인사)

| 스킬 | 호출 | 설명 |
|------|------|------|
| [Year-End Tax](skills/hr/year-end-tax/) | `/year-end-tax` | 2025 귀속 연말정산 Q&A. 국세청 PDF 기반 전 항목 안내 및 Python 계산기로 정확한 세액 산출 |

### refactoring (리팩토링)

| 스킬 | 호출 | 설명 |
|------|------|------|
| [ABAP Reverse Engineering](skills/refactoring/abap-reverse-engineering/) | `/abap-reverse-engineering` | SAP ABAP 레거시 코드 역공학. 6단계 분석으로 비즈니스 로직/데이터 흐름/인터페이스 명세서 산출 |

### 예정 도메인

| 도메인 | 상태 |
|--------|------|
| finance (재무) | 준비 중 |
| sales (영업) | 준비 중 |
| common (공통) | 준비 중 |

## 구조

```
skills/
├── dev/                              # 개발
│   ├── tdd-workflow/SKILL.md         # 테스트 주도 개발
│   ├── frontend-design/SKILL.md      # 프론트엔드 디자인
│   ├── security-review/SKILL.md      # 보안 리뷰
│   ├── playwright/SKILL.md           # 브라우저 자동화
│   ├── backend-patterns/SKILL.md     # 백엔드 패턴
│   ├── frontend-patterns/SKILL.md    # 프론트엔드 패턴
│   ├── coding-standards/SKILL.md     # 코딩 표준
│   ├── clickhouse-io/SKILL.md        # ClickHouse 패턴
│   └── project-guidelines-example/SKILL.md # 프로젝트 가이드라인 예제
├── hr/                               # 인사
│   └── year-end-tax/                 # 연말정산
│       ├── SKILL.md                  # 스킬 정의
│       ├── ref/01-12.md              # 세법 참조 파일
│       └── calculators/*.py          # Python 세액 계산기
├── refactoring/                      # 리팩토링
│   └── abap-reverse-engineering/     # ABAP 역공학
│       ├── SKILL.md                  # 스킬 정의
│       └── templates/                # 산출물 템플릿
├── finance/                          # 재무 (준비 중)
├── sales/                            # 영업 (준비 중)
└── common/                           # 공통 (준비 중)
```

## 사용법

스킬은 Claude Code에서 자동으로 인식됩니다. 슬래시 명령어로 호출하거나, 관련 작업 시 자동 활성화됩니다.

```
/skill-name
```

## 스킬 작성

새 스킬을 추가하려면 [CONTRIBUTING.md](docs/CONTRIBUTING.md)와 [SKILL-TEMPLATE.md](docs/SKILL-TEMPLATE.md)를 참고하세요.

```
skills/<domain>/<skill-name>/
├── SKILL.md       # 필수: 스킬 정의 (YAML frontmatter + 본문)
├── README.md      # 선택: 사람용 문서
└── templates/     # 선택: 보조 파일
```

## 라이선스

Internal Use Only - Atom
