# Dicoding "Belajar Analisis Data dengan Python"

## Deskripsi
Proyek "Belajar Analisis Data dengan Python" dari paltform Dicoding menggunakan data Bike Sharing Dataset. 
Tujuan proyek inia adalah untuk mengvisualisasikan dan menganalisis data yang disediakan dari tahun 2011 hingga 2012.
[Bike Sharing Dataset](https://drive.google.com/file/d/1RaBmV6Q6FYWU4HWZs80Suqd7KQC34diQ/view)

## Streamlit
Streamlit Cloud : [Bike Sharing Dashboard](http://localhost:8513/)
Copy paste the link and open it in Google Chrome

## Direktori
- **/Dataset Bike Sharing**: Berisi data yang digunakan dengan format .csv.
- **/DashboardBike**: Berisi dashboard.py dan data yang digunakan untuk membuat dashboard.
- **Proyek Analisis Data Dicoding - Bike Sharing.ipynb**: File yang digunakan untuk analisis data.
- **requirements.txt**: Berisi library yang digunakan dalam proses analisis data. 

## Instalasi
1. Install Visual Studio Code.
2. Clone repository komputer lokal 
3. Memiliki library Python yang sesuai 
    ```shell
    pip install streamlit
    pip install -r requirements.txt
    ```
4. Masuk ke direktori proyek (local)
    ```shell
    cd DashboardBike
    ```
5. Jalankan streamlit app
   ```shell
    streamlit run dashboardbike.py
   ```