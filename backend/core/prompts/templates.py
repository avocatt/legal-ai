"""Different prompt templates for legal reasoning."""
from typing import List

from .base import BasePromptTemplate


class BasicLegalPrompt(BasePromptTemplate):
    """Basic prompt template for legal questions."""

    def __init__(self):
        """Initialize the basic legal prompt template.

        Sets up a simple template that focuses on using context to answer
        legal questions with proper terminology and article references.
        """
        template = """Sen Türk Ceza Kanunu konusunda uzmanlaşmış bir hukuk asistanısın.

Bağlam:
{context}

Soru: {question}

Yanıtını oluştururken şu kurallara uy:
1. Sadece verilen bağlamda bulunan bilgileri kullan
2. Yasal terimleri doğru ve yerinde kullan
3. Cevabını kanun maddeleriyle destekle
4. Açık ve anlaşılır bir dil kullan

Yanıt:"""
        super().__init__(template)

    def format(self, **kwargs) -> str:
        """Format the template with context and question."""
        if not self.validate_inputs(**kwargs):
            raise ValueError("Invalid inputs")
        return self.template.format(**kwargs)

    def validate_inputs(self, **kwargs) -> bool:
        """Validate required inputs exist."""
        return all(k in kwargs for k in ["context", "question"])


class StructuredLegalPrompt(BasePromptTemplate):
    """Structured prompt template with explicit sections."""

    def __init__(self):
        """Initialize the structured legal prompt template.

        Sets up a comprehensive template that breaks down the response
        into clearly defined sections for thorough legal analysis.
        """
        template = """Sen Türk Ceza Kanunu konusunda uzmanlaşmış bir hukuk asistanısın.

Bağlam:
{context}

Soru: {question}

Yanıtını aşağıdaki yapıda oluştur:

1. SORU KAPSAMI:
   - Sorunun hangi yasal konuları içerdiğini belirt
   - İlgili yasal terimleri tanımla
   - Yanıtın odaklanacağı ana noktaları belirle

2. İLGİLİ KANUN MADDELERİ:
   - Her maddeyi "Madde X:" formatında belirt
   - Maddeleri önem sırasına göre sırala
   - Her maddenin konuyla ilgili kısmını alıntıla
   - Maddelerin birbiriyle ilişkisini belirt

3. HUKUKİ ANALİZ:
   - Her maddenin nasıl yorumlanması gerektiğini açıkla
   - Varsa istisnai durumları ve şartları belirt
   - Yasal terimlerin pratik uygulamasını açıkla
   - Varsa içtihatlardan veya doktrinden örnekler ver

4. SONUÇ:
   - Ana noktaları özetle
   - Net ve kesin bir yanıt oluştur
   - Tüm yasal referansları tekrar belirt
   - Varsa dikkat edilmesi gereken özel durumları vurgula

Yanıtını oluştururken şu kurallara kesinlikle uy:
1. Her bölümü belirtilen sırayla ve başlıklarıyla birlikte yaz
2. Sadece verilen bağlamda bulunan bilgileri kullan, spekülasyon yapma
3. Her yasal terimi ilk kullanımında tanımla ve açıkla
4. Kanun maddelerini tam referanslarıyla birlikte kullan
5. Açık, anlaşılır ve profesyonel bir dil kullan
6. Her bölümü en az 2-3 cümleyle açıkla
7. Bölümler arasında mantıksal bağlantı kur
8. Önemli noktaları bold (**) ile vurgula

Yanıt:"""
        super().__init__(template)
        self.metadata["sections"] = [
            "SORU KAPSAMI",
            "İLGİLİ KANUN MADDELERİ",
            "HUKUKİ ANALİZ",
            "SONUÇ",
        ]

    def format(self, **kwargs) -> str:
        """Format the template with context and question."""
        if not self.validate_inputs(**kwargs):
            raise ValueError("Invalid inputs")
        return self.template.format(**kwargs)

    def validate_inputs(self, **kwargs) -> bool:
        """Validate required inputs exist."""
        return all(k in kwargs for k in ["context", "question"])

    def get_sections(self) -> List[str]:
        """Get the defined sections."""
        return self.metadata["sections"]


class MultiStepLegalPrompt(BasePromptTemplate):
    """Multi-step reasoning prompt template for complex legal questions."""

    def __init__(self):
        """Initialize the multi-step legal prompt template.

        Sets up a template that guides the model through a step-by-step
        reasoning process for complex legal questions.
        """
        template = """Sen Türk Ceza Kanunu konusunda uzmanlaşmış bir hukuk asistanısın.

Bağlam:
{context}

Soru: {question}

Bu soruyu yanıtlamak için aşağıdaki adımları izle:

1. SORU ANALİZİ:
   - Sorunun ana konusunu belirle
   - İlgili yasal kavramları tanımla
   - Hangi kanun maddelerinin geçerli olduğunu tespit et

2. YASAL ÇERÇEVE:
   - İlgili kanun maddelerini listele
   - Maddelerin birbiriyle ilişkisini açıkla
   - Varsa içtihatları belirt

3. HUKUKİ DEĞERLENDİRME:
   - Her maddeyi ayrı ayrı ele al
   - Maddelerin nasıl uygulanacağını açıkla
   - İstisnai durumları belirt

4. SONUÇ:
   - Tüm analizleri özetle
   - Net bir yanıt oluştur
   - Yasal referansları ekle

Yanıtını oluştururken şu kurallara uy:
1. Her adımı ayrı ayrı ele al
2. Sadece verilen bağlamda bulunan bilgileri kullan
3. Yasal terimleri doğru ve yerinde kullan
4. Açık ve anlaşılır bir dil kullan
5. Adımlar arasında mantıksal bağlantı kur

Yanıt:"""
        super().__init__(template)
        self.metadata["steps"] = [
            "Soru Analizi",
            "Yasal Çerçeve",
            "Hukuki Değerlendirme",
            "Sonuç",
        ]

    def format(self, **kwargs) -> str:
        """Format the template with context and question."""
        if not self.validate_inputs(**kwargs):
            raise ValueError("Invalid inputs")
        return self.template.format(**kwargs)

    def validate_inputs(self, **kwargs) -> bool:
        """Validate required inputs exist."""
        return all(k in kwargs for k in ["context", "question"])

    def get_steps(self) -> List[str]:
        """Get the reasoning steps."""
        return self.metadata["steps"]
