// Q-Net 접근 차단으로 공식 원문 대조 미완료. 아래 값은 학습용 잠정 설정.
export const PROFILE = {
  name: "중식조리기능사", subjects: ["중식 재료관리, 음식조리 및 위생관리"] as const,
  questionCount: 60, durationMinutes: 60, choiceCount: 4, passScore: 60,
  maxScore: 100, hasSubjectCutoff: false, rulesVerificationStatus: "pending",
  selectionPolicy: "통합 과목 내 무작위 60문항; 공식 단원별 분포 재현 아님",
} as const;
