import streamlit as st
import pandas as pd
from io import BytesIO

# --------------------------------------------------
# Sayfa ayarları
# --------------------------------------------------
st.set_page_config(
    page_title=Yüzyüze Eğitim İstatistik Raporu,
    layout=wide
)

st.title(YÜZYÜZE EĞİTİM İSTATİSTİK RAPOR UYGULAMASI)

# --------------------------------------------------
# Açıklama bölümü
# --------------------------------------------------
st.markdown(
### 📌 Excel Dosya Formatı Açıklaması

Yükleyeceğiniz Excel veya CSV dosyası tek sayfa olmalı ve aşağıdaki sütunları aynı isimlerle içermelidir

- Kullanıcı Adı (A) Çalışana ait benzersiz kod  
- Ad Soyad (B) Bilgilendirme amaçlıdır, hesaplamalarda kullanılmaz  
- Şirket (C)  
  - SUNAR YATIRIM  
  - SUNAR MISIR  
  - ELİTA GIDA  
  - NÇS GIDA  
  - SUNAR UN VE YEM-OSMANİYE  
  - SUNAR UN VE YEM-KONYA  
  - SUNAR NP  
- Yaka Kategorisi (D)
  - BY → Beyaz Yaka  
  - MY → Mavi Yaka  
- Eğitim İsmi (E) Eğitimin adı  
- Eğitim Süresi (F) Saat cinsinden, tam sayı (ör. 2)

⚠️ Aynı kişi aynı eğitime birden fazla katılmışsa ayrı satırlar halinde yer almalıdır.
)

# --------------------------------------------------
# Dosya yükleme
# --------------------------------------------------
uploaded_file = st.file_uploader(
    Excel veya CSV dosyasını yükleyin,
    type=[xlsx, csv]
)

if uploaded_file
    # Dosya okuma
    if uploaded_file.name.endswith(.csv)
        df = pd.read_csv(uploaded_file)
    else
        df = pd.read_excel(uploaded_file)

    # Sütun adlarını temizle
    df.columns = df.columns.str.strip()

    # --------------------------------------------------
    # Şirket isimlerini normalize et
    # --------------------------------------------------
    df[Şirket] = df[Şirket].replace({
        SUNAR UN VE YEM-OSMANİYE SUNAR UN VE YEM,
        SUNAR UN VE YEM-KONYA SUNAR UN VE YEM
    })

    companies = [
        SUNAR YATIRIM,
        SUNAR MISIR,
        ELİTA GIDA,
        NÇS GIDA,
        SUNAR UN VE YEM,
        SUNAR NP
    ]

    results = []

    # --------------------------------------------------
    # Hesaplamalar
    # --------------------------------------------------
    for company in companies
        company_df = df[df[Şirket] == company]

        if company_df.empty
            results.append({
                Şirket company,
                Eğitim İsmi -,
                Eğitim Süresi (Saat) 0,
                Katılımcı Sayısı 0,
                Toplam Eğitim Saati 0,
                BY Sayısı 0,
                MY Sayısı 0,
                BY Toplam Saat 0,
                MY Toplam Saat 0
            })
            continue

        grouped = company_df.groupby(Eğitim İsmi)

        for training, g in grouped
            duration = g[Eğitim Süresi].iloc[0]
            participant_count = len(g)

            by_df = g[g[Yaka Kategorisi] == BY]
            my_df = g[g[Yaka Kategorisi] == MY]

            results.append({
                Şirket company,
                Eğitim İsmi training,
                Eğitim Süresi (Saat) duration,
                Katılımcı Sayısı participant_count,
                Toplam Eğitim Saati participant_count  duration,
                BY Sayısı len(by_df),
                MY Sayısı len(my_df),
                BY Toplam Saat len(by_df)  duration,
                MY Toplam Saat len(my_df)  duration
            })

    result_df = pd.DataFrame(results)

    # --------------------------------------------------
    # Eğitim bazlı tablo
    # --------------------------------------------------
    st.subheader(📊 Eğitim Bazlı Detaylı Tablo)
    st.dataframe(result_df, use_container_width=True)

    # --------------------------------------------------
    # Şirket bazlı özet
    # --------------------------------------------------
    summary_df = (
        result_df
        .groupby(Şirket)[[BY Toplam Saat, MY Toplam Saat, Toplam Eğitim Saati]]
        .sum()
        .reset_index()
    )

    st.subheader(🏢 Şirket Bazlı Toplam Özet)
    st.dataframe(summary_df, use_container_width=True)

    # --------------------------------------------------
    # Excel çıktıları (HATASIZ)
    # --------------------------------------------------
    detay_buffer = BytesIO()
    result_df.to_excel(detay_buffer, index=False)
    detay_buffer.seek(0)

    st.download_button(
        label=📥 Eğitim Detay Tablosunu Excel Olarak İndir,
        data=detay_buffer,
        file_name=egitim_detay_raporu.xlsx,
        mime=applicationvnd.openxmlformats-officedocument.spreadsheetml.sheet
    )

    ozet_buffer = BytesIO()
    summary_df.to_excel(ozet_buffer, index=False)
    ozet_buffer.seek(0)

    st.download_button(
        label=📥 Şirket Özet Tablosunu Excel Olarak İndir,
        data=ozet_buffer,
        file_name=sirket_ozet_raporu.xlsx,
        mime=applicationvnd.openxmlformats-officedocument.spreadsheetml.sheet
    )