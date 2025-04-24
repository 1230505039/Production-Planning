**min_production_time Dinamik Programlama Çözümü**  
Bu proje, işlerin makineler üzerinde işlenme süreleri ve makineler arası geçiş maliyetleri göz önünde bulundurularak toplam üretim süresinin en aza indirgenmesini amaçlayan bir dinamik programlama yaklaşımı sunar.  

---

## 1. Problem Tanımı

- **İşler (Jobs)**: İndeksleri `0`dan `n-1`e kadar olan `n` adet iş.
- **Makineler (Machines)**: İndeksleri `0`dan `m-1`e kadar olan `m` adet makine.
- **İşleme Süreleri (processing_times)**: `n x m` boyutunda bir matris. `processing_times[i][j]`, `i` işinin `j` makinesinde tamamlanma süresini ifade eder.
- **Geçiş Maliyetleri (switch_costs)**: `m x m` boyutunda bir matris. `switch_costs[k][j]`, bir önceki işin `k` makinesinden bir sonraki işin `j` makinesine geçerken katlanılan ek süreyi gösterir.

Amaç, tüm işleri bir sırayla ve uygun makineler seçerek işlerken toplam zamanı (işleme süresi + geçiş maliyetleri) en az kılacak makine atamalarını belirlemektir.


## 2. Matris Zinciri Çarpımı ile İlişkisi

Bu problem, klasik **Matris Zinciri Çarpımı (Matrix Chain Multiplication)** problemine benzerlik gösterir. Her iş, bir matris çarpımı adımı olarak düşünülebilirken, makineler ise çarpım sırasını etkileyen mümkün yolları temsil eder:

- Matris zinciri çarpımında, çarpma sırasını belirlerken ara işlemlerin maliyetini en aza indirmeyi hedefleriz.
- Burada da işler dizisini işlerken makineler arası geçiş maliyetlerini ve işleme sürelerini toplayarak toplam maliyeti minimize etmeyi amaçlıyoruz.

Şema itibarıyla her adımda önceki durumdan (önceki makine seçiminden) gelen maliyeti ve güncel adımın işleme + geçiş maliyetini hesaba katarak en iyi sonucu buluruz.


## 3. Tablolama (Tabulation) ve Hafızalama (Memoization)

Bu projede **tablolama** (alt problem sonuçlarını matrise kaydetme) yaklaşımı kullanılmıştır:

1. **DP Matrisi Oluşturma**  
   `dp[i][j]` = `i` işine kadar hesaplanan en düşük toplam süre ve son işin `j` makinesinde tamamlanması durumu.
2. **Başlangıç Durumu**  
   İlk iş (`i = 0`) için `dp[0][j] = processing_times[0][j]` olarak tanımlanır.
3. **Durum Geçişi**  
   Genel halde:
   ```python
   dp[i][j] = min_{k in [0..m)} ( dp[i-1][k] + switch_costs[k][j] + processing_times[i][j] )
   ```
   Her `i` ve `j` kombinasyonu için tüm olası `k` makinelerinin maliyetleri hesaplanır.
4. **Path (Yol) Matrisi**  
   `path[i][j]` matrisi, `dp[i][j]` değerini elde ederken hangi `k` makinesi seçildiğini saklar. Böylece geriye dönerek ({\em traceback}) optimal makine kayıtları bulunur.

> Projede hafızalama (memoization) yerine doğrudan tablolama tercih edilmiştir, çünkü alt problemlerin sayı ve düzenli yapısı dolayısıyla taban tablolama matrisi kodu sadelik ve performans açısından yeterlidir.


## 4. Kod Açıklamaları

- **`min_production_time(processing_times, switch_costs)`**  
  - Girdi: `processing_times (n x m)`, `switch_costs (m x m)`  
  - Çıktı: `(min_time, best_machines)`
    - `min_time`: Hesaplanan en düşük toplam üretim süresi.
    - `best_machines`: Her iş için seçilen optimal makine dizisi.
  - Adımlar:
    1. DP ve path matrislerini `np.inf` ve `0` ile tanımlar.
    2. `i=0` için başlangıç maliyetlerini atar.
    3. Döngülerle `i=1..n-1`, `j=0..m-1`, `k=0..m-1` üzerinden maliyetleri hesaplar ve matrisi günceller.
    4. Son işin hangi makinede bittiğini bularak `min_time` ve `last_machine` değerlerini elde eder.
    5. `path` matrisini kullanarak `best_machines` dizisini geriye dönerek oluşturur.

- **Test Fonksiyonu**  
  `test_random()` fonksiyonu, rastgele değerler üretip sonucu validasyon ile kontrol eder:
  ```python
  np.random.seed(42)
  processing_times = np.random.randint(1,10,(n,m))
  switch_costs = np.random.randint(1,5,(m,m))
  for i in range(m): switch_costs[i][i] = 0

  min_time, best_machines = min_production_time(processing_times, switch_costs)
  # Sonucu, manuel olarak hesaplanan toplamla karşılaştırarak doğrular.
  ```


## 5. Test Sonuçları

```
Random Test Case (n=10, m=5):
Minimum Total Time: 73
Best Machine Selection: [3, 3, 3, 0, 0, 0, 1, 1, 3, 4]
Validation: Success
```

Yukarıdaki çıktılar, `test_random()` fonksiyonunun ürettiği örnek için elde edilmiştir ve doğruluk onayı başarıyla gerçekleşmiştir.


## 6. Zaman ve Uzay Karmaşıklığı Analizi

- **Zaman Karmaşıklığı (Time Complexity)**  
  - Üçlü iç içe döngü kullanılıyor: `i` için `n` adım, `j` için `m` adım, `k` için `m` adım.  
  - Toplam: **O(n \* m^2)**.

- **Uzay Karmaşıklığı (Space Complexity)**  
  - `dp` matrisi: `n x m`  
  - `path` matrisi: `n x m`  
  - Ekstra sabit alanlar (geçici değişkenler vs.)  
  - Toplam: **O(n \* m)**

---

*Bu proje, dinamik programlama yaklaşımının temel prensiplerini uygulayarak üretim hattı optimizasyonu problemini etkin şekilde çözer.*

