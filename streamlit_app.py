# pip install streamlit matplotlib requests

import streamlit as st
import datetime
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib
import os
import requests

# ------------------- 페이지 기본 설정 -------------------
st.set_page_config(page_title="카페인 섭취 시간대별 수면 영향", layout="centered")
st.title("☕ 카페인 섭취 시간대별 수면 영향 분석")
st.write("취침 예정 시간과 카페인 섭취 시간을 입력하면, 수면에 미치는 영향을 시각적으로 보여줍니다.")
st.markdown("---")

# ------------------- ✅ 한글 폰트 설정 -------------------
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 깨짐 방지

font_path = ""
if os.name == "nt":  # Windows
    font_path = "C:/Windows/Fonts/malgun.ttf"
elif os.name == "posix":  # Mac, Linux, Streamlit Cloud
    font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"

# Streamlit Cloud용 — 폰트가 없을 때 자동 다운로드
if not os.path.exists(font_path):
    try:
        os.makedirs(os.path.dirname(font_path), exist_ok=True)
        url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf"
        r = requests.get(url)
        with open(font_path, "wb") as f:
            f.write(r.content)
    except Exception as e:
        st.warning("⚠️ 폰트를 다운로드하지 못했습니다. 한글이 깨질 수 있습니다.")

if os.path.exists(font_path):
    font_name = fm.FontProperties(fname=font_path).get_name()
    matplotlib.rc('font', family=font_name)
else:
    st.warning("⚠️ 한글 폰트를 찾지 못했습니다. 텍스트가 네모로 표시될 수 있습니다.")

# ------------------- 사용자 입력 -------------------
sleep_time = st.time_input("🛏️ 취침 예정 시간", datetime.time(23, 0))
intake_time = st.time_input("☕ 카페인 섭취 시간", datetime.time(15, 0))

# 시간 차이 계산
sleep_dt = datetime.datetime.combine(datetime.date.today(), sleep_time)
intake_dt = datetime.datetime.combine(datetime.date.today(), intake_time)
if intake_dt > sleep_dt:
    intake_dt -= datetime.timedelta(days=1)
hours_until_sleep = (sleep_dt - intake_dt).total_seconds() / 3600

# ------------------- 구간별 영향 분류 -------------------
if hours_until_sleep >= 8:
    risk_level = "🟩 안전 (Safe)"
    advice = "카페인 대사가 충분히 이루어져 수면에 거의 영향을 주지 않습니다."
elif 4 <= hours_until_sleep < 8:
    risk_level = "🟨 주의 (Moderate)"
    advice = "수면 효율이 약간 저하될 수 있습니다. 가능하면 취침 8시간 이전 섭취를 권장합니다."
else:
    risk_level = "🟥 위험 (High Impact)"
    advice = "카페인이 체내에 상당량 남아 수면 시작이 지연되고 깊은 수면이 감소할 수 있습니다."

# ------------------- 결과 출력 -------------------
st.subheader("결과 요약")
st.write(f"☕ 섭취 시점: 취침 {hours_until_sleep:.1f}시간 전")
st.write(f"📊 현재 구간: {risk_level}")
st.info(advice)

# ------------------- 시각화 -------------------
fig, ax = plt.subplots(figsize=(8, 1.5))
zones = [
    (0, 4, "red", "위험"),
    (4, 8, "gold", "주의"),
    (8, 12, "green", "안전")
]

for start, end, color, label in zones:
    ax.barh(0, width=end - start, left=start, color=color, alpha=0.5, label=label)

# 사용자 섭취 위치 표시
ax.scatter(hours_until_sleep, 0, color="black", s=100, zorder=5, label="섭취 시점")
ax.text(hours_until_sleep, 0.15, f"{hours_until_sleep:.1f}h 전", ha="center", fontsize=10)

# 축 설정
ax.set_xlim(0, 12)
ax.set_yticks([])
ax.set_xlabel("취침 전 남은 시간 (시간 단위)")
ax.invert_xaxis()  # 오른쪽이 취침 시점
ax.legend(loc="upper right", ncol=4)
st.pyplot(fig)

st.caption("※ 연구 근거: 카페인 반감기 약 5시간, 취침 8시간 이내 섭취 시 수면 효율 저하 (ACU, 2023; Healthline, 2020)")

