import streamlit as st
import pandas as pd

# Streamlit tarafından sağlanan default sayfa dizaynı ve ismi
st.set_page_config(layout="wide", page_title="Rüzgar Enerjisi", page_icon="⚡")

st.set_option('deprecation.showfileUploaderEncoding', False)
st.set_option('deprecation.showPyplotGlobalUse', False)
st.sidebar.markdown("<div style='position: fixed; top: 0; padding: 20px;'></div>", unsafe_allow_html=True)
st.sidebar.image("img/BZDAY.jpg", use_column_width=True)


@st.cache_resource()
def get_data():
    dataframe = pd.read_csv("Data/data.csv")
    return dataframe


st.title("Rüzgar Enerjisi 💨")

# sidebar

teknoloji_tab, sürdürülebilirlik_tab, biyoçeşitlilik_tab, iklim_tab, ekonomik_tab = st.tabs(
    ["Teknoloji Gelişimi", "Sürdürülebilirlik", "Biyoçeşitlilik", " İklim Değişikliği", "Ekonomik Kalkınma"])

# Ana Sayfa
sürdürülebilirlik_tab.markdown("""
<h2 style='font-size:35px'>Rüzgar Enerjisi ve Sürdürülebilirlik</h2>""", unsafe_allow_html=True)

first_col, last_col = sürdürülebilirlik_tab.columns((2))

# Rüzgar Enerjisi ve Sürdürülebilirlik Tabı
last_col.markdown("""
Rüzgar enerjisi, günümüzde sürdürülebilirlik ve çevre koruma çabalarının önemli bir parçası haline gelmiştir. Fosil yakıtların kullanımının getirdiği çevresel sorunlar ve iklim değişikliği tehdidi, alternatif ve temiz enerji kaynaklarına olan ilgiyi artırmıştır. Rüzgar enerjisi, bu bağlamda, karbon emisyonlarını azaltma ve çevre dostu bir enerji üretme potansiyeliyle dikkat çekmektedir.

Gelişen teknolojiyle birlikte, rüzgar enerjisi türbinlerinin verimliliği artmakta ve maliyetleri düşmektedir. Bu da rüzgar enerjisinin daha erişilebilir hale gelmesini sağlamaktadır. Rüzgar enerjisi türbinleri, rüzgarın kinetik enerjisini elektrik enerjisine dönüştürmek için kullanılan güçlü ve etkili makinelerdir. Bunlar, genellikle rüzgar çiftlikleri adı verilen alanlarda gruplar halinde bulunurlar ve büyük miktarda temiz enerji üretebilirler.

Rüzgar enerjisi projeleri, doğal kaynakların sürdürülebilir kullanımı ve çevresel etkilerin azaltılması için önemli bir adımdır. Bu projeler, rüzgar türbinlerinin kurulumu ve işletilmesiyle birlikte, genellikle ekosisteme zarar vermeden yapılan inşaat çalışmalarını içerir. Ayrıca, rüzgar enerjisi projeleri, bölgesel ekonomilere katkı sağlayabilir ve yerel istihdamı artırabilir.

Rüzgar enerjisinin sürdürülebilirlik üzerindeki olumlu etkileri, küresel düzeyde karbon emisyonlarını azaltarak ve temiz enerji üreterek hissedilir. Bu nedenle, rüzgar enerjisi projelerinin desteklenmesi ve teşvik edilmesi, sürdürülebilir bir enerji geleceğine doğru atılmış önemli bir adımdır.
""")

first_col.image("img/world.jpg", use_column_width=True)

# Teknoloji Gelişimi Tabı

teknoloji_tab.markdown("""
<h2 style='font-size:35px'>Rüzgar Enerjisi ve Teknoloji Gelişimi</h2>""", unsafe_allow_html=True)

first_t_col, last_t_col = teknoloji_tab.columns((2))
last_t_col.image("img/tech.png", use_column_width=True)

first_t_col.markdown("""
Rüzgar enerjisi, gün geçtikçe daha verimli ve ekonomik hale gelmektedir. Teknolojideki hızlı gelişmeler, rüzgar türbinlerinin verimliliğini artırmakta ve maliyetlerini düşürmektedir. Bu sayede, rüzgar enerjisi giderek daha rekabetçi bir enerji kaynağı haline gelmektedir. Yükselen verimlilik ve düşen maliyetler, rüzgar enerjisinin daha geniş çapta kullanılabilir hale gelmesini sağlamaktadır.

Son yıllarda, rüzgar türbinleri ve altyapıları üzerinde yapılan araştırmalar, daha yüksek verimlilik ve dayanıklılık sağlamak amacıyla önemli ilerlemeler kaydetmiştir. Örneğin, daha uzun kanat tasarımları ve daha güçlü jeneratörler, rüzgar türbinlerinin enerji üretimini artırmakta ve daha düşük rüzgar hızlarında bile etkin bir şekilde çalışabilmelerini sağlamaktadır. Bu gelişmeler, rüzgar enerjisinin kullanılabilirliğini artırarak, daha fazla bölgede ve farklı koşullarda rüzgar enerjisi projelerinin hayata geçirilmesine olanak tanımaktadır.

Depolama teknolojilerindeki ilerlemeler de rüzgar enerjisi sektörü için önemli bir avantaj sağlamaktadır. Rüzgar enerjisi genellikle değişken bir enerji kaynağıdır, bu da enerji üretiminin dalgalı ve belirsiz olmasına neden olabilir. Ancak, gelişen batarya teknolojileri sayesinde, rüzgar enerjisinin daha istikrarlı bir kaynak haline gelmesi mümkün olmaktadır. Batarya depolama sistemleri, fazla üretilen enerjinin depolanmasını ve daha sonra ihtiyaç duyulduğunda kullanılmasını sağlayarak, enerji arzının daha güvenilir ve tutarlı olmasına yardımcı olmaktadır.)
""")

# Ayrıca, akıllı grid sistemleri ve dijital teknolojilerin kullanımı da rüzgar enerjisi entegrasyonunu kolaylaştırmaktadır. Bu sistemler, rüzgar enerjisi üretiminin tahmin edilmesi ve taleple uyumlu hale getirilmesi için önemli bir rol oynamaktadır. Akıllı grid sistemleri, enerji talebinin düzenlenmesi ve enerji depolama sistemleriyle entegre edilmesi konusunda önemli bir araç sağlayarak, rüzgar enerjisinin daha etkin bir şekilde kullanılmasına olanak tanımaktadır. Bu sayede, rüzgar enerjisi daha güvenilir bir enerji kaynağı haline gelmekte ve enerji sistemlerinin daha verimli çalışmasına katkıda bulunmaktadır.

# Bu teknolojik yenilikler, rüzgar enerjisinin daha yaygın bir şekilde kullanılmasını sağlayarak, temiz ve yenilenebilir enerji kaynaklarının küresel enerji karışımında daha büyük bir paya sahip olmasına olanak tanımaktadır. Yenilenebilir enerji kaynaklarının artan kullanımı, fosil yakıtlara bağımlılığı azaltarak çevresel etkileri ve iklim değişikliği riskini azaltabilir. Bununla birlikte, sürekli olarak yeniliklerin ve gelişmelerin takip edilmesi ve uygulanması, rüzgar enerjisinin potansiyelinden tam anlamıyla yararlanılmasını sağlayabilir.)

# theme
hide_st_style = """
<style> #MainMenu {visibility: hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
"""

# Biyoçeşitlilik Tabı
biyoçeşitlilik_tab.markdown("""
<h2 style='font-size:35px'>Rüzgar Enerjisi ve Biyoçeşitlilik</h2>""", unsafe_allow_html=True)
biyoçeşitlilik_first_col, biyoçeşitlilik_last_col = biyoçeşitlilik_tab.columns((2))

# Sol tarafta metin içeriğini oluştur
biyoçeşitlilik_last_col.markdown("""
Rüzgar enerjisi projeleri, sadece enerji üretimine katkıda bulunmakla kalmaz, aynı zamanda biyoçeşitlilik üzerinde de etkiye sahiptir. Rüzgar enerjisi türbinleri, ekosistemdeki kuşlar ve yaban hayatı üzerinde potansiyel bir etkiye sahip olabilir. Özellikle, kuşların ve yarasaların rüzgar türbinlerine çarpması riski bulunmaktadır.

Bu nedenle, rüzgar enerjisi projeleri genellikle kuş göç yolları veya önemli yaban hayatı alanlarıyla çakışabilecek bölgelerde planlanırken, çevresel etkilerin en aza indirilmesi için titizlikle incelenmelidir. Ek olarak, rüzgar türbinlerinin yerleştirilmesi ve işletilmesi sırasında biyoçeşitliliği korumak için uygun önlemler alınmalıdır.

Ancak, doğru yerleştirme ve yönetim stratejileri kullanıldığında, rüzgar enerjisi projeleri biyoçeşitlilik üzerinde olumlu bir etkiye sahip olabilir. Özellikle, rüzgar enerjisi projelerinin alanlarının habitat restorasyonu veya koruma projeleriyle birleştirilmesi, biyoçeşitliliği artırabilir ve ekosistem sağlığını destekleyebilir.

Bu nedenle, rüzgar enerjisi projeleri biyoçeşitlilik üzerinde hem olumsuz hem de olumlu etkilere sahip olabilir. Proje planlaması ve uygulanması aşamasında çevresel etkilerin dikkate alınması ve koruyucu önlemlerin alınması önemlidir. Bu sayede, rüzgar enerjisi projeleri biyoçeşitlilik üzerinde olumlu bir etki yaratabilir ve doğal yaşamın korunmasına katkıda bulunabilir.
""")

# Sağ tarafta görüntüyü ekleyin
biyoçeşitlilik_first_col.image("img/veri.jpg", use_column_width=True)

# İklim Değişikliği Tabı

iklim_tab.markdown("""
<h2 style='font-size:35px'>Rüzgar Enerjisi ve İklim Değişikliği</h2>""", unsafe_allow_html=True)

iklim_first_col, iklim_last_col = iklim_tab.columns((2))

# Sol tarafta metin içeriğini oluştur
iklim_first_col.markdown("""
Rüzgar enerjisi, fosil yakıtlara dayalı enerji üretimine kıyasla önemli ölçüde daha az sera gazı salınımına neden olur. Bu nedenle, rüzgar enerjisi iklim değişikliğiyle mücadelede önemli bir rol oynayabilir.

Fosil yakıtlardan kaynaklanan karbondioksit emisyonlarının azaltılması, atmosferdeki sera gazı seviyelerinin düşürülmesine ve küresel ısınmanın etkilerinin hafifletilmesine yardımcı olabilir. Rüzgar enerjisi, bu anlamda, düşük karbonlu ve çevre dostu bir enerji kaynağıdır.

Ayrıca, rüzgar enerjisi projeleri, iklim değişikliğinin etkilerine uyum sağlamak için de önemli olabilir. Yenilenebilir enerji kaynaklarına dayalı bir enerji sistemine geçiş, iklim değişikliğine uyum sağlama sürecini destekleyebilir ve enerji arzının daha güvenilir hale gelmesini sağlayabilir.

Rüzgar enerjisinin iklim değişikliğiyle mücadeledeki rolü giderek daha önemli hale gelmektedir. İklim değişikliğinin etkileri giderek artmakta ve acil eylem gerektirmektedir. Bu bağlamda, rüzgar enerjisi gibi yenilenebilir enerji kaynaklarına yönelik yatırımların artırılması ve kullanımının teşvik edilmesi önemlidir. Bu, hem iklim değişikliğiyle mücadeleye katkıda bulunacak hem de enerji güvenliğini sağlayacaktır.

Ayrıca, rüzgar enerjisi projeleri, iklim değişikliğiyle mücadelede yenilikçi çözümler sunabilir. Örneğin, rüzgar enerjisi türbinlerinin deniz üzerine kurulması gibi projeler, hem enerji üretimini artırabilir hem de kıyı bölgelerde erozyonu azaltarak iklim değişikliği etkileriyle başa çıkmaya yardımcı olabilir.
""")

# Sağ tarafta görüntüyü ekleyin
iklim_last_col.image("img/RuzgarGulu.jpg", use_column_width=True)

# Ekonomik Kalkınma Tabı
ekonomik_tab.markdown("""
<h2 style='font-size:35px'>Rüzgar Enerjisi ve Ekonomik Kalkınma</h2>""", unsafe_allow_html=True)

ekonomik_first_col, ekonomik_last_col = ekonomik_tab.columns((2))

# Sol tarafta metin içeriğini oluştur
ekonomik_first_col.markdown("""
Rüzgar enerjisi projeleri, ekonomik kalkınma için potansiyel bir fırsat sunar. Bu projeler, iş imkanları yaratma, yerel ekonomilere katkı sağlama ve yenilenebilir enerji sektöründe büyümeyi teşvik etme potansiyeline sahiptir.

Rüzgar enerjisi türbinlerinin inşası, işletilmesi ve bakımı için çeşitli becerilere ve uzmanlıklara ihtiyaç duyulmaktadır. Bu da yerel işgücünün eğitilmesi ve istihdam edilmesi için bir fırsat oluşturabilir. Ayrıca, rüzgar enerjisi projeleri genellikle yerel tedarik zincirlerine dayanır, bu da yerel işletmeler için yeni iş fırsatları yaratabilir.

Ekonomik olarak, rüzgar enerjisi projeleri, enerji maliyetlerini düşürerek endüstriyel ve ticari kullanıcılar için rekabet avantajı sağlayabilir. Ayrıca, rüzgar enerjisi projeleri genellikle devlet teşvikleri ve destekleriyle desteklenir, bu da projelerin finansmanını kolaylaştırabilir ve yatırımcılar için cazip hale getirebilir.

Rüzgar enerjisi, aynı zamanda bölgesel kalkınmayı teşvik edebilir ve yerel ekonomilere canlılık kazandırabilir. Rüzgar enerjisi projeleri genellikle kırsal alanlarda kurulur ve bu bölgelerde yeni iş fırsatları yaratır. Bu da göçü azaltabilir ve yerel toplulukların sürdürülebilir bir gelecek inşa etmelerine yardımcı olabilir.

Bununla birlikte, rüzgar enerjisi projelerinin ekonomik etkileri, dikkatli bir şekilde yönetilmelidir. Projelerin yer seçimi, topluluk katılımı ve yerel paydaşlarla işbirliği önemlidir. Ayrıca, rüzgar enerjisi projelerinin uzun vadeli sürdürülebilirliği için ekonomik modellerin dikkatlice incelenmesi gerekmektedir.
""")

# Sağ tarafta görüntüyü ekleyin
ekonomik_last_col.image("img/ekonomi.jpeg", use_column_width=True)
