# Skill 템플릿

새 skill 작성 시 아래 템플릿을 복사하여 사용하세요.

---

```markdown
---
name: skill-name
description: 이 skill이 언제 사용되는지 한 줄 설명
domain: dev | hr | finance | sales | common
author: 작성자명
---

# Skill 제목

## 언제 사용하나요?

- 이 skill이 적용되는 상황
- 트리거 조건

## 프로세스

1. 첫 번째 단계
2. 두 번째 단계
3. ...

## 예시

실제 사용 예시를 보여주세요.

## 주의사항

- 하지 말아야 할 것
- 흔한 실수
```

---

## 필드 설명

| 필드 | 필수 | 설명 |
|------|------|------|
| name | O | skill 식별자 (폴더명과 동일) |
| description | O | Claude가 skill 선택 시 참고하는 설명 |
| domain | O | 도메인 카테고리 |
| author | O | 작성자/담당팀 |
