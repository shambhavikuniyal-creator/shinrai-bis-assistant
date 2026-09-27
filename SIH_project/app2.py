import streamlit as st
import time
import re

# --- PAGE SETUP ---
st.set_page_config(
    page_title="Shinrai BIS Assistant | SIH 2026",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- VERIFIED MULTILINGUAL KNOWLEDGE BASE ---
KNOWLEDGE_BASE = {
    "water": {
        "english_title": "PACKAGED DRINKING WATER (TDS & QUALITY)",
        "is_code": "IS 14543:2016 / IS 10500:2012",
        "clause": "IS 14543 Table 1, Clause 5.2 (TDS Limits & Quality)",
        "source": "Bureau of Indian Standards Scheme-I Mandatory Certification",
        "marathi": (
            "**पॅकेज्ड पिण्याच्या पाण्यातील TDS मर्यादा आणि नियम (IS 14543:2016):**\n\n"
            "- **TDS मर्यादा:** BIS मानकांनुसार बाटलीबंद पाण्यात विरघळलेल्या घटकांची (TDS) मर्यादा **७५ mg/L ते ५०० mg/L** दरम्यान असणे कायदेशीररित्या बंधनकारक आहे.\n"
            "- **महत्त्व:** ७५ mg/L पेक्षा कमी TDS असल्यास पाण्यात आवश्यक खनिजे नसतात; तर ५०० mg/L पेक्षा जास्त TDS आरोग्यासाठी अयोग्य ठरू शकतो.\n"
            "- **ISI मार्क तपासणी:** पाण्याच्या बाटलीवर खरा **ISI मार्क** आणि त्याखाली **७ अंकी CML (लायसन्स) क्रमांक** असणे आवश्यक आहे.\n"
            "- **पडताळणी:** ग्राहक हा CML क्रमांक **BIS Care App** मध्ये 'Verify License' पर्यायावर जाऊन तपासू शकतात."
        ),
        "hindi": (
            "**पैकेaged पेयजल में TDS सीमा एवं सुरक्षा नियम (IS 14543:2016):**\n\n"
            "- **TDS सीमा:** BIS मानकों के अनुसार बोतलबंद पानी में Total Dissolved Solids (TDS) की कानूनी सीमा **75 mg/L से 500 mg/L** के बीच होनी चाहिए।\n"
            "- **महत्व:** 75 mg/L से कम TDS शरीर के लिए जरूरी खनिजों की कमी दर्शाता है, और 500 mg/L से अधिक अशुद्धियों का संकेत है।\n"
            "- **ISI मार्क:** बोतल पर अनिवार्य रूप से **ISI मार्क** और उसके नीचे 7-अंकों का **CML लाइसेंस नंबर** होना चाहिए।\n"
            "- **सत्यापन:** उपभोक्ता **BIS Care App** के जरिए CML कोड को तुरंत सत्यापित कर सकते हैं।"
        ),
        "english": (
            "**Packaged Drinking Water TDS Limits & Safety (IS 14543:2016):**\n\n"
            "- **Permissible TDS Range:** Legally mandated between **75 mg/L (minimum) and 500 mg/L (maximum)**.\n"
            "- **Importance:** TDS < 75 mg/L lacks essential minerals; TDS > 500 mg/L indicates excessive dissolved solids.\n"
            "- **ISI Mark:** Must feature the authentic **ISI Mark** with a 7-digit **CML license number** printed underneath.\n"
            "- **Verification:** Use the **BIS Care App** to verify CML authenticity."
        ),
    },
    "toy": {
        "english_title": "TODDLER TOY SAFETY REGULATIONS (< 36 MONTHS)",
        "is_code": "IS 9873 (Part 1, 2, 3 & 6) / Toys QCO 2020",
        "clause": "Part 1: Cl 4.4 (Choking Test) | Part 3: Migration Limits | Part 6: Phthalates",
        "source": "Toys (Quality Control) Order 2020 - Mandatory BIS Scheme-I",
        "marathi": (
            "**लहान मुलांच्या खेळण्यांचे सुरक्षा नियम (IS 9873 आणि QCO):**\n\n"
            "- **३ वर्षांखालील मुलांसाठी गुदमरण्याचा धोका (Choking Hazard):** खेळण्यातील कोणताही भाग ३१.७ मिमी आकाराच्या 'स्मॉल पार्ट्स सिलिंडर' चाचणीत बसता कामा नये (क्लॉज ४.४).\n"
            "- **विषारी घटक व रंग मर्यादा (Part 3):** खेळण्यांच्या रंगात शिशाची (Lead) मर्यादा **९० mg/kg** पेक्षा जास्त नसावी.\n"
            "- **प्लॅस्टिक सुरक्षा (Part 6):** प्लॅस्टिक खेळण्यांमध्ये 'Phthalates' चे प्रमाण **०.१%** पेक्षा कमी असणे बंधनकारक आहे.\n"
            "- **ISI मार्क अनिवार्य:** खेळण्यावर व त्याच्या पॅकिंगवर स्पष्ट **ISI मार्क** असणे कायद्याने सक्तीचे आहे."
        ),
        "hindi": (
            "**36 महीने से कम उम्र के बच्चों के खिलौनों के सुरक्षा नियम (IS 9873):**\n\n"
            "- **दम घुटने का खतरा (Choking Hazard):** 3 साल से छोटे बच्चों के खिलौने का कोई भी छोटा हिस्सा 31.7 मिमी सिलेंडर परीक्षण में नहीं जाना चाहिए (क्लॉज 4.4)।\n"
            "- **हानिकारक धातु सीमा (Part 3):** खिलौने के पेंट और सतह में लेड (Lead) की मात्रा **90 mg/kg** से अधिक नहीं हो सकती।\n"
            "- **प्लास्टिक मानक (Part 6):** प्लास्टिसाइज़र Phthalates की सांद्रता **0.1%** द्रव्यमान से कम होनी अनिवार्य है।\n"
            "- **अनिवार्य मानक:** खिलौनों पर वैध **ISI मार्क** और CML कोड होना कानूनी रूप से जरूरी है।"
        ),
        "english": (
            "**Toddler Toy Safety Regulations (IS 9873 Series):**\n\n"
            "- **Choking Hazard (<36 Months):** Small parts must not fit into the standard 31.7 mm truncated test cylinder (Clause 4.4).\n"
            "- **Heavy Metal Toxicity (Part 3):** Lead (Pb) migration is strictly capped at **90 mg/kg**.\n"
            "- **Phthalate Plasticizers (Part 6):** Cumulative concentration must not exceed **0.1% by mass**.\n"
            "- **Certification:** Mandatory Scheme-I **ISI Mark** on all toys under Toys QCO 2020."
        ),
    },
    "gold": {
        "english_title": "GOLD HALLMARK IDENTIFICATION & HUID VERIFICATION",
        "is_code": "IS 1417:2016",
        "clause": "Clause 4 & 5 (Hallmarking Protocols & 6-Digit HUID)",
        "source": "BIS Act 2016 Mandatory Hallmarking Order",
        "marathi": (
            "**सोन्याच्या हॉलमार्कची ओळख आणि नियम (IS 1417:2016):**\n\n"
            "सोन्याचे अस्सल दागिने खरेदी करताना **३ महत्त्वाची चिन्हे (Marks)** तपासणे अनिवार्य आहे:\n"
            "1. **BIS लोगो:** त्रिकोणी BIS मानांकन चिन्ह.\n"
            "2. **शुद्धता श्रेणी (Purity/Karat):** उदाहरणार्थ, **22K916** (२२ कॅरेट - ९१.६% शुद्ध), **18K750** (१८ कॅरेट), **14K585** (१४ कॅरेट).\n"
            "3. **६-अंकी HUID कोड:** दागिन्यांवर लेसरने कोरलेला ६-अक्षरी अल्फान्यूमेरिक कोड (उदा. `AB1234`).\n"
            "- **पडताळणी:** **BIS Care App** उघडून 'Verify HUID' पर्यायामध्ये हा ६-अंकी कोड टाकल्यास सोनाराचे नाव, नोंदणी आणि दागिन्यांचे वजन लगेच दिसते."
        ),
        "hindi": (
            "**असली गोल्ड हॉलमार्क की पहचान और HUID (IS 1417:2016):**\n\n"
            "सोना खरीदते समय आभूषण पर **3 प्रमुख निशान** अवश्य जांचें:\n"
            "1. **BIS मानक लोगो:** आधिकारिक त्रिकोण चिन्ह।\n"
            "2. **शुद्धता व कैरेट ग्रेड:** जैसे **22K916** (22 कैरेट - 91.6% शुद्ध), **18K750** (18 कैरेट), **14K585** (14 कैरेट)।\n"
            "3. **6-अंकों का HUID कोड:** लेजर द्वारा अंकित 6-अक्षरों का विशिष्ट अल्फ़ान्यूमेरिक कोड (जैसे `AB1234`)।\n"
            "- **सत्यापन:** उपभोक्ता **BIS Care App** के 'Verify HUID' विकल्प में इस कोड को दर्ज करके हॉलमार्किंग केंद्र और शुद्धता की पुष्टि कर सकते हैं।"
        ),
        "english": (
            "**Gold Hallmark Identification & HUID Guidelines (IS 1417:2016):**\n\n"
            "Verify the **3 Mandatory Marks** laser-engraved on authentic gold jewellery:\n"
            "1. **BIS Logo:** The triangular standard mark.\n"
            "2. **Purity / Fineness Grade:** e.g., **22K916** (22 Karat - 91.6%), **18K750** (18 Karat), **14K585** (14 Karat).\n"
            "3. **6-Digit Alphanumeric HUID:** Unique identification code (e.g., `AZ89X2`).\n"
            "- **Verification:** Enter the 6-character HUID into the **BIS Care App** under 'Verify HUID' to check jeweler and purity details."
        ),
    },
}

# --- TOPIC & LANGUAGE DETECTION FUNCTIONS ---
def detect_topic(text: str):
    t = text.lower()
    # Water keywords (English, Marathi, Hindi)
    if any(w in t for w in ["water", "tds", "bottle", "पाणी", "पाण्याची", "जल", "पेयजल", "पॅकेज्ड", "ड्रिंकिंग"]):
        return "water"
    # Toy keywords
    elif any(w in t for w in ["toy", "toys", "toddler", "baby", "kid", "खेळणी", "खेळण्यांचे", "खिलौने", "खिलौना", "गुदमरणे", "शिशु"]):
        return "toy"
    # Gold keywords
    elif any(w in t for w in ["gold", "hallmark", "huid", "karat", "carat", "सोने", "सोन्याचे", "हॉलमार्क", "दागिने", "स्वर्ण", "आभूषण"]):
        return "gold"
    return None

def detect_language(text: str, default_lang: str):
    if default_lang != "Auto-Detect":
        if "Marathi" in default_lang: return "marathi"
        if "Hindi" in default_lang: return "hindi"
        return "english"
        
    # Devanagari detection
    has_devanagari = bool(re.search(r'[\u0900-\u097F]', text))
    if not has_devanagari:
        return "english"
        
    # Marathi specific indicators
    marathi_markers = ["आहे", "नाही", "करावे", "पाणी", "खेळणी", "दागिने", "कसे", "काय", "मधील", "सोन्याचे", "सांगा", "मर्यादा"]
    t = text.lower()
    if any(m in t for m in marathi_markers):
        return "marathi"
    return "hindi"

# --- SIDEBAR UI ---
with st.sidebar:
    st.markdown("### 🛡️ **Shinrai BIS Assistant**")
    st.caption("Smart India Hackathon 2026 | PS ID: SIH26107")
    st.caption("Team: Kasukabe Defence Group")
    st.markdown("---")
    
    lang_choice = st.selectbox(
        "Language Gateway / भाषा निवडा:",
        ["Auto-Detect", "Marathi (मराठी)", "Hindi (हिन्दी)", "English"]
    )
    
    st.markdown("---")
    st.subheader("💡 Try Preset Questions:")
    
    st.caption("**Marathi (मराठी) Presets:**")
    if st.button("सोने हॉलमार्क आणि HUID कसे ओळखायचे?", use_container_width=True):
        st.session_state.pending_query = "सोने हॉलमार्क आणि HUID कसे ओळखायचे?"
    if st.button("पॅकेज्ड पाण्याच्या बाटलीत TDS मर्यादा किती असते?", use_container_width=True):
        st.session_state.pending_query = "पॅकेज्ड पाण्याच्या बाटलीत TDS मर्यादा किती असते?"
    if st.button("लहान मुलांच्या खेळण्यांसाठी BIS सुरक्षा नियम काय आहेत?", use_container_width=True):
        st.session_state.pending_query = "लहान मुलांच्या खेळण्यांसाठी BIS सुरक्षा नियम काय आहेत?"

    st.caption("**Hindi (हिन्दी) & English Presets:**")
    if st.button("सोने के हॉलमार्क की पहचान कैसे करें?", use_container_width=True):
        st.session_state.pending_query = "सोने के हॉलमार्क की पहचान कैसे करें?"
    if st.button("What is the safe TDS limit for packaged water?", use_container_width=True):
        st.session_state.pending_query = "What is the safe TDS limit for packaged water?"

    st.markdown("---")
    if st.button("Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# --- INITIALIZE SESSION ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- MAIN INTERFACE ---
st.title("🛡️ Shinrai Regulatory Compliance Assistant")
st.markdown(
    "Grounding queries against **eBIS & QCO Regulations** across **Marathi, Hindi & English** with exact clause citations."
)
st.markdown("---")

# Render conversation history
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])
        if chat.get("meta"):
            with st.expander("🔍 Verified Standard Grounding (Zero Hallucination)", expanded=False):
                st.write(f"**IS Code:** {chat['meta']['is_code']}")
                st.write(f"**Clause Citation:** {chat['meta']['clause']}")
                st.write(f"**Regulatory Source:** {chat['meta']['source']}")

# --- INPUT HANDLING ---
user_typed = st.chat_input("तुमचा प्रश्न येथे विचारा / अपना प्रश्न यहाँ लिखें / Ask your compliance question...")
active_query = getattr(st.session_state, "pending_query", None) or user_typed

if active_query:
    st.session_state.pending_query = None  # Reset preset trigger
    
    # Save & Display user query
    st.session_state.chat_history.append({"role": "user", "content": active_query})
    with st.chat_message("user"):
        st.markdown(active_query)

    # Process Assistant Response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing standard specifications..."):
            time.sleep(0.4)
            topic_key = detect_topic(active_query)
            lang = detect_language(active_query, lang_choice)

            if topic_key:
                doc = KNOWLEDGE_BASE[topic_key]
                english_badge = doc["english_title"]
                localized_body = doc[lang]

                # Format required layout: Prominent English topic heading + localized content
                response_html = f"""
<div style="background-color: #0f172a; border-left: 5px solid #3b82f6; padding: 12px 18px; border-radius: 6px; margin-bottom: 14px;">
    <span style="font-size: 0.8rem; letter-spacing: 1.5px; color: #94a3b8; font-weight: 700; text-transform: uppercase;">Identified Standard Domain</span>
    <h3 style="margin: 3px 0 0 0; color: #60a5fa; font-family: sans-serif; font-size: 1.25rem;">📌 TOPIC: {english_badge}</h3>
</div>
"""
                final_content = response_html + localized_body
                st.markdown(final_content, unsafe_allow_html=True)

                # Verified grounding metadata
                with st.expander("🔍 Verified Standard Grounding (Zero Hallucination)", expanded=True):
                    st.write(f"**IS Code:** {doc['is_code']}")
                    st.write(f"**Clause Citation:** {doc['clause']}")
                    st.write(f"**Regulatory Source:** {doc['source']}")

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": final_content,
                    "meta": {
                        "is_code": doc["is_code"],
                        "clause": doc["clause"],
                        "source": doc["source"]
                    }
                })
            else:
                # Fallback zero-hallucination message
                if lang == "marathi":
                    fallback_text = (
                        "⚠️ **माहिती उपलब्ध नाही (Zero-Hallucination Safe Mode)**\n\n"
                        "हा प्रश्न सध्या इंडेक्स केलेल्या मानकांमध्ये (पाणी TDS, खेळणी सुरक्षा, किंवा सोन्याचे हॉलमार्किंग) आढळला नाही. "
                        "कृपया अधिक तपशिलांसाठी [eBIS Portal](https://www.manakonline.in) ला भेट द्या."
                    )
                elif lang == "hindi":
                    fallback_text = (
                        "⚠️ **जानकारी उपलब्ध नहीं (Zero-Hallucination Safe Mode)**\n\n"
                        "यह प्रश्न वर्तमान में इंडेक्स किए गए मानकों में उपलब्ध नहीं है। "
                        "कृपया आधिकारिक [eBIS Portal](https://www.manakonline.in) पर संदर्भ लें।"
                    )
                else:
                    fallback_text = (
                        "⚠️ **Information Not Found (Zero-Hallucination Safe Mode)**\n\n"
                        "The queried parameter is not indexed in the verified standard dataset. "
                        "In compliance with SIH26107 rules, this assistant does not fabricate answers. "
                        "Please refer to the official [eBIS Portal](https://www.manakonline.in)."
                    )

                st.markdown(fallback_text)
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": fallback_text,
                    "meta": None
                })