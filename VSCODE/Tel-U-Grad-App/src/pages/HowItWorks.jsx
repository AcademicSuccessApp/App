import React from 'react';

const HowItWorks = () => {
  return (
    <div style={{ maxWidth: 900, margin: '0 auto', padding: '2.5rem 1rem' }}>
      <h2 style={{ fontWeight: 800, fontSize: '2rem', marginBottom: '1.5rem' }}>
        Cara Kerja
      </h2>
      <p style={{ color: '#888', fontSize: '1.1rem', marginBottom: '1.5rem' }}>
        Website ini dirancang untuk membantu Mahasiswa Telkom University Purwokerto memprediksi peluang kelulusan mereka. Cara kerjanya sangat sederhana: mahasiswa cukup memasukkan data akademik seperti nilai IPS dari tiga semester pertama, program studi, dan kode dosen wali. Data ini kemudian diproses oleh sistem menggunakan model prediksi berbasis machine learning yang telah dilatih secara khusus dengan data mahasiswa Telkom University Purwokerto.
      </p>
      <p style={{ color: '#888', fontSize: '1.1rem' }}>
        Model prediksi ini menganalisis pola dari data yang dimasukkan dan membandingkannya dengan data historis mahasiswa sebelumnya. Hasil prediksi akan menampilkan kemungkinan kelulusan mahasiswa dengan tingkat akurasi hingga 81%. Dengan demikian, mahasiswa dapat memperoleh gambaran yang lebih jelas mengenai peluang kelulusan dan dapat merencanakan langkah selanjutnya secara lebih tepat.
      </p>
    </div>
  );
};

export default HowItWorks; 