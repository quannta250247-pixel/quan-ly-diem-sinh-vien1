import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Tiêu đề ứng dụng
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")

# Dữ liệu mẫu 10 sinh viên
data = {
    'Họ tên': ['An', 'Bình', 'Chi', 'Dũng', 'Hà', 'Lan', 'Minh', 'Nam', 'Phúc', 'Trang'],
    'Chuyên cần': [8.0, 9.0, 7.0, 9.5, 7.5, 6.0, 9.0, 7.0, 7.5, 9.5],
    'Giữa kỳ': [7.0, 8.0, 6.5, 8.5, 7.0, 6.0, 8.5, 7.0, 7.5, 9.0],
    'Cuối kỳ': [7.5, 8.5, 6.0, 9.0, 7.5, 6.5, 8.5, 7.0, 7.5, 9.0]
}

df = pd.DataFrame(data)

# Tính điểm tổng kết và xếp loại
df['Tổng kết'] = (0.2 * df['Chuyên cần'] + 0.3 * df['Giữa kỳ'] + 0.5 * df['Cuối kỳ']).round(2)

def xep_loai(diem):
    if diem >= 8.5: return 'Giỏi'
    elif diem >= 7.0: return 'Khá'
    elif diem >= 5.0: return 'Trung bình'
    else: return 'Yếu'

df['Xếp loại'] = df['Tổng kết'].apply(xep_loai)

# 1. Hiển thị bảng điểm
st.subheader("📋 Bảng điểm chi tiết của 10 sinh viên")
st.dataframe(df, use_container_width=True)

# 2. Hiển thị thông tin thống kê
st.subheader("📊 Thống kê chung")
diem_tb = df['Tổng kết'].mean()
sv_max = df.loc[df['Tổng kết'].idxmax()]
sv_min = df.loc[df['Tổng kết'].idxmin()]
so_dat = (df['Tổng kết'] >= 5.0).sum()

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Điểm TB của lớp", value=f"{diem_tb:.2f}")
    st.metric(label="Số sinh viên đạt (>= 5.0)", value=so_dat)
with col2:
    st.metric(label="SV điểm cao nhất", value=f"{sv_max['Họ tên']} ({sv_max['Tổng kết']})")
    st.metric(label="SV điểm thấp nhất", value=f"{sv_min['Họ tên']} ({sv_min['Tổng kết']})")

# 3. Danh sách xổ xuống chọn sinh viên
st.subheader("🔍 Tra cứu thông tin sinh viên")
selected_student = st.selectbox("Chọn tên sinh viên:", df['Họ tên'])
student_info = df[df['Họ tên'] == selected_student].iloc[0]

st.write(f"- **Chuyên cần:** {student_info['Chuyên cần']}")
st.write(f"- **Giữa kỳ:** {student_info['Giữa kỳ']}")
st.write(f"- **Cuối kỳ:** {student_info['Cuối kỳ']}")
st.write(f"- **Tổng kết:** **{student_info['Tổng kết']}**")
st.write(f"- **Xếp loại:** **{student_info['Xếp loại']}**")

# 4. Biểu đồ cột điểm tổng kết
st.subheader("📈 Biểu đồ điểm tổng kết")
fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(df['Họ tên'], df['Tổng kết'], color='cornflowerblue')
ax.set_xlabel('Điểm tổng kết')
ax.set_ylabel('Sinh viên')
ax.set_xlim(0, 10)
for i, v in enumerate(df['Tổng kết']):
    ax.text(v + 0.1, i, str(v), va='center')
ax.invert_yaxis()
st.pyplot(fig)

# 5. Thông tin người tạo ở cuối trang
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray; font-size: small;'>Người tạo: [Họ tên của bạn] - [MSSV của bạn]</p>", unsafe_allow_html=True)
