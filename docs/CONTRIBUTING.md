# 기여 가이드

## Skill 추가 방법

1. 적절한 도메인 폴더 선택 (`skills/dev/`, `skills/hr/` 등)
2. skill 폴더 생성: `skills/<domain>/<skill-name>/`
3. `skill.md` 작성 ([템플릿 참고](SKILL-TEMPLATE.md))
4. PR 생성

## 폴더 구조

```
skills/<domain>/<skill-name>/
└── skill.md
```

## 네이밍 규칙

- 폴더명: kebab-case (예: `code-review`, `onboarding-guide`)
- 영어 사용 권장
- 명확하고 간결하게

## PR 프로세스

1. 브랜치 생성: `feat/<domain>/<skill-name>`
2. skill 작성
3. PR 생성 및 리뷰 요청
4. 승인 후 머지

## 좋은 Skill의 조건

- 명확한 사용 시점 설명
- 단계별 가이드 포함
- 실제 예시 제공
- 주의사항 명시
