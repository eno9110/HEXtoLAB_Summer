#Summer
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from skimage import color

st.title('HEXtoLAB_Summer')

# === HEXカラーをL*a*b*に変換する関数 ===
def hex_to_lab(hex_list):
    """複数のHEXカラーをL*a*b*に一括変換"""
    lab_list = []
    for hex_color in hex_list:
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        rgb_normalized = np.array([r, g, b]) / 255.0
        lab = color.rgb2lab(rgb_normalized.reshape((1, 1, 3))).reshape(3)
        lab_list.append(lab)
    return np.array(lab_list)

# === Streamlit UI ===
st.title("L* a* b* 色空間の3D可視化とCSV出力_Summer")

# === HEXカラーリスト（指定された色_Summer） ===
hex_colors = [
    "#f8f7f2", "#99a2af", "#51617a", "#edd4be", "#946b55",
    "#79553d", "#385076", "#7d8fb5", "#9fc1da", "#98c1ef",
    "#4474b6", "#6b88cc", "#cde692", "#1fb585", "#029666",
    "#f8f0a5", "#ccf7f0", "#c48796", "#f9d1df", "#ffbdd8",
    "#f66779", "#ea264e", "#fc0b3e", "#cf0000", "#d25573",
    "#ad0550", "#a61415", "#e0a4ee", "#baa9d6", "#6e0056"
]

# === HEX → L*a*b* 変換 ===
lab_colors = hex_to_lab(hex_colors)

# === データフレーム作成（CSV保存用） ===
df = pd.DataFrame(lab_colors, columns=['L*', 'a*', 'b*'])
df.insert(0, 'HEX', hex_colors)

# === CSVファイルに保存 ===
csv_filename = 'hex_to_lab_colors_summer.csv'
df.to_csv(csv_filename, index=False)

# === CSVダウンロードボタン ===
st.write("### HEXカラーとL* a* b* 座標のCSV出力_summer")
st.download_button(
    label="CSVをダウンロード",
    data=df.to_csv(index=False).encode('utf-8'),
    file_name=csv_filename,
    mime='text/csv'
)

# === 3Dグラフで可視化 ===
fig = go.Figure()

# 各色を3Dプロット
for hex_color, (l, a, b) in zip(hex_colors, lab_colors):
    fig.add_trace(go.Scatter3d(
        x=[a], y=[b], z=[l],
        mode='markers+text',
        marker=dict(size=6, color=hex_color, opacity=0.5),
        text=[hex_color],
        hovertemplate=(
            f"HEX:{hex_color}<br>"
            f"L*:{1:.2f}<br>"
            f"a*:{a:2f}<br>"
            f"b*:{b:2f}<extra></extra>"   
        )
        #textposition="top center"
    ))

# === グラフレイアウト設定 ===
fig.update_layout(
    title=dict(
        text="SummerPalette",
        y=0.95,#タイトルを上部へ移動，デフォルト0.9
        x=0.5,#中央揃え
        xanchor="center",#中央揃え
        yanchor="top"#上揃え  
    ),
    scene=dict(
        xaxis_title='a* 軸',
        yaxis_title='b* 軸',
        zaxis_title='L* 軸',
        xaxis=dict(range=[-100, 100]),
        yaxis=dict(range=[-100, 100]),
        zaxis=dict(range=[0, 100]),
        aspectmode='manual',
        aspectratio=dict(x=1, y=1, z=1)  # L*:a*:b* = 2:1:1 に設定
    ),
    margin=dict(l=10, r=10, b=10, t=10)
)

# === Streamlitで3Dグラフ表示 ===
st.write("### L* a* b* 色空間 3D可視化_summer")
st.plotly_chart(fig)

