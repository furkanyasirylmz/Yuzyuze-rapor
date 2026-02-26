import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(
    page_title="Yuzyuze Egitim Istatistik Raporu",
    layout="wide"
)

st.title("YUZYUZE EGITIM ISTATISTIK RAPOR UYGULAMASI")

st.markdown("""
### Excel Dosya Formati Aciklamasi

Yukleyeceginiz Excel veya CSV dosyasi tek sayfa olmali ve asagidaki sutunlari ayni isimlerle icermelidir:

- Kullanici Adi (A): Calisana ait benzersiz kod
- Ad Soyad (B): Bilgilendirme amaclidir
- Sirket (C):
  SUNAR YATIRIM
  SUNAR MISIR
  ELITA GIDA
  NCS GIDA
  SUNAR UN VE YEM-OSMANIYE
  SUNAR UN VE YEM-KONYA
  SUNAR NP
- Yaka Kategorisi (D):
  BY = Beyaz Yaka
  MY = Mavi Yaka
- Egitim Ismi (E): Egitimin adi
- Egitim Suresi (F): Saat cinsinden tam sayi (orn 2)

Ayni kisi ayni egitime birden fazla katilmissa ayri satirlar halinde yer almalidir.
""")

uploaded_file = st.file_uploader(
    "Excel veya CSV dosyasini yukleyin",
    type=["xlsx", "csv"]
)

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    df.columns = df.columns.str.strip()

    df["Şirket"] = df["Şirket"].replace({
        "SUNAR UN VE YEM-OSMANİYE": "SUNAR UN VE YEM",
        "SUNAR UN VE YEM-KONYA": "SUNAR UN VE YEM"
    })

    companies = [
        "SUNAR YATIRIM",
        "SUNAR MISIR",
        "ELİTA GIDA",
        "NÇS GIDA",
        "SUNAR UN VE YEM",
        "SUNAR NP"
    ]

    results = []

    for company in companies:
        company_df = df[df["Şirket"] == company]

        if company_df.empty:
            results.append({
                "Şirket": company,
                "Eğitim İsmi": "-",
                "Eğitim Süresi (Saat)": 0,
                "Katılımcı Sayısı": 0,
                "Toplam Eğitim Saati": 0,
                "BY Sayısı": 0,
                "MY Sayısı": 0,
                "BY Toplam Saat": 0,
                "MY Toplam Saat": 0
            })
            continue

        grouped = company_df.groupby("Eğitim İsmi")

        for training, g in grouped:
            duration = g["Eğitim Süresi"].iloc[0]
            participant_count = len(g)

            by_df = g[g["Yaka Kategorisi"] == "BY"]
            my_df = g[g["Yaka Kategorisi"] == "MY"]

            results.append({
                "Şirket": company,
                "Eğitim İsmi": training,
                "Eğitim Süresi (Saat)": duration,
                "Katılımcı Sayısı": participant_count,
                "Toplam Eğitim Saati": participant_count * duration,
                "BY Sayısı": len(by_df),
                "MY Sayısı": len(my_df),
                "BY Toplam Saat": len(by_df) * duration,
                "MY Toplam Saat": len(my_df) * duration
            })

    result_df = pd.DataFrame(results)

    st.subheader("Egitim Bazli Detayli Tablo")
    st.dataframe(result_df, use_container_width=True)

    summary_df = (
        result_df
        .groupby("Şirket")[["BY Toplam Saat", "MY Toplam Saat", "Toplam Eğitim Saati"]]
        .sum()
        .reset_index()
    )

    st.subheader("Sirket Bazli Toplam Ozet")
    st.dataframe(summary_df, use_container_width=True)

    detay_buffer = BytesIO()
    result_df.to_excel(detay_buffer, index=False)
    detay_buffer.seek(0)

    st.download_button(
        label="Egitim Detay Tablosunu Excel Olarak Indir",
        data=detay_buffer,
        file_name="egitim_detay_raporu.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    ozet_buffer = BytesIO()
    summary_df.to_excel(ozet_buffer, index=False)
    ozet_buffer.seek(0)

    st.download_button(
        label="Sirket Ozet Tablosunu Excel Olarak Indir",
        data=ozet_buffer,
        file_name="sirket_ozet_raporu.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
