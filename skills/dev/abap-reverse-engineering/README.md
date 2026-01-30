# ABAP Reverse Engineering Skill

SAP ABAP 코드를 분석하여 비즈니스 로직과 기술 구조를 문서화하는 OpenCode/Oh My OpenCode 스킬입니다.

## 🎯 목적

레거시 ABAP 시스템의 역공학(Reverse Engineering)을 통해:
- 문서화되지 않은 코드의 비즈니스 로직 파악
- 데이터 흐름 및 의존성 분석
- 기술 스펙 문서 자동 생성

## 📦 설치

### OpenCode (기본)

```bash
# 프로젝트 로컬 설치
mkdir -p .opencode/skills
cp -r abap-reverse-engineering .opencode/skills/

# 또는 글로벌 설치
mkdir -p ~/.config/opencode/skill
cp -r abap-reverse-engineering ~/.config/opencode/skill/
```

### Oh My OpenCode

```bash
# 프로젝트 로컬 설치 (동일)
mkdir -p .opencode/skills
cp -r abap-reverse-engineering .opencode/skills/

# 또는 Claude Code 호환 경로
mkdir -p .claude/skills
cp -r abap-reverse-engineering .claude/skills/
```

## 🚀 사용법

### 1. 스킬 로드

OpenCode에서 다음과 같이 스킬을 호출합니다:

```
/skill abap-reverse-engineering
```

또는 자연어로:

```
ABAP 역공학 스킬을 로드해줘
```

### 2. 코드 분석 요청

```
다음 ABAP 코드를 분석해서 6가지 산출물을 만들어줘:

[ABAP 코드 붙여넣기]
```

### 3. 파일 기반 분석

```
./src 폴더의 ABAP 파일들을 분석해줘
```

## 📄 산출물

| 산출물 | 설명 |
|--------|------|
| 비즈니스 로직 명세서 | 업무 규칙, 계산식, 유효성 검증 |
| 데이터 흐름 명세서 | 테이블 사용, 트랜잭션 경계 |
| 기능 명세서 | 화면, 이벤트, 기능 목록 |
| 인터페이스 명세서 | RFC, BAPI, IDoc 스펙 |
| 테이블/구조 명세서 | 테이블, 구조, 변수 정의 |
| 호출 관계도 | 호출 계층, 의존성 매트릭스 |

## 📁 디렉토리 구조

```
abap-reverse-engineering/
├── SKILL.md              # 메인 스킬 정의
├── README.md             # 이 파일
└── templates/            # 산출물 템플릿
    └── 00_분석_요약_템플릿.md
```

## 🔧 지원 ABAP 유형

- ✅ Report Program
- ✅ Module Pool (Dynpro)
- ✅ Function Module / Function Group
- ✅ Class / Interface (ABAP OO)
- ✅ BADI / Enhancement
- ✅ BAPI
- ✅ CDS View
- ✅ AMDP

## 💡 팁

1. **대규모 코드 분석**: INCLUDE가 많은 경우 전체 코드를 한 번에 제공하면 더 정확한 분석 가능
2. **특정 영역 집중**: "비즈니스 로직만 분석해줘" 처럼 특정 산출물만 요청 가능
3. **반복 분석**: 산출물 생성 후 "인터페이스 부분 더 자세히" 처럼 추가 분석 요청 가능

## 📝 라이선스

MIT License

## 🤝 기여

이슈 및 PR 환영합니다!
