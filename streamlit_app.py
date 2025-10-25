import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="카페인 섭취 시간대별 수면 영향", layout="centered")

# 제목 및 설명
st.title("☕ 카페인 섭취 시간대별 수면 영향 (400mg 기준)")

st.write("""
💡 **연구 기반 요약**
- 본 그래프는 400mg(고용량, 커피 약 4잔) 섭취 시 수면에 미치는 영향을 나타냅니다.  
- 100mg(일반적인 커피 1잔)은 **취침 전 4시간까지** 섭취해도 수면 구조나 효율에 **유의미한 변화가 없습니다.**
""")

# 데이터 (시간: 취침 전 기준)
hours = np.array([12, 8, 4, 0])
impact = np.array([0.2, 0.5, 0.9, 1.0])  # 상대적 수면 영향 강도 (400mg 기준)

# 그래프 설정
fig, ax = plt.subplots(figsize=(7, 3))
bars = ax.bar(hours, impact, width=2.5, color=["#6aa84f", "#f1c232", "#e69138", "#cc0000"])

# x, y 축 설정
ax.set_xticks(hours)
ax.set_xticklabels(["12시간 전", "8시간 전", "4시간 전", "취침 직전"])
ax.set_ylim(0, 1.1)
ax.set_ylabel("수면 영향 강도 (상대적)")
ax.set_title("카페인 400mg 섭취 시 수면 영향 변화")

# 그래프 내 글자 제거 (요청 반영)
for bar in bars:
    bar.set_linewidth(0)

# 설명 구간 추가
st.pyplot(fig)

st.markdown("---")
st.subheader("📘 해석 가이드")
st.write("""
- 🟩 **12시간 전 (안전 구간)**: 수면 구조에 거의 영향 없음  
- 🟨 **8시간 전 (경계 구간)**: 수면 효율(SE)과 WASO(수면 중 각성 시간)에 부분적 영향  
- 🟧 **4시간 전 (주의 구간)**: SOL(수면 시작 시간) 지연, N3(깊은 수면) 감소 시작  
- 🟥 **취침 직전 (위험 구간)**: 수면 단편화, 총 수면시간(TST) 감소, 수면의 질 저하  
""")

st.info("""
✅ **정리:**  
- 100mg(커피 1잔)은 취침 전 4시간까지 안전합니다.  
- 400mg(커피 4잔)은 취침 전 12시간 이내 섭취 시 수면의 질이 저하됩니다.
""")




