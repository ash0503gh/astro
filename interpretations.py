"""
Rule-Based Interpretations for Vedic Birth Charts
Provides basic readings for planet placements, house lordships, etc.
Fully localized in English and Classical Jyotish Hindi (Devanagari).
"""

ASC_READINGS = {
    "Mesha": "Bold, pioneering, and action-oriented. Natural leader with strong willpower and physical vitality. Can be impulsive but always ready to forge ahead.",
    "Vrishabha": "Stable, artistic, and wealth-conscious. Values comfort and security. Patient approach with a love for beauty, food, and material pleasures.",
    "Mithuna": "Curious, communicative, and versatile. Quick-witted with a love for learning and socializing. Adaptable but can be restless.",
    "Karka": "Nurturing, intuitive, and emotionally deep. Strong attachment to home and family. Protective nature with powerful intuition.",
    "Simha": "Regal, confident, and charismatic. Natural authority figure who seeks recognition. Generous and creative with a dramatic flair.",
    "Kanya": "Analytical, service-oriented, and detail-focused. Practical approach to life with strong organizational skills. Health-conscious.",
    "Tula": "Diplomatic, relationship-focused, and aesthetically inclined. Seeks balance and harmony. Strong sense of justice and partnership.",
    "Vrishchika": "Intense, transformative, and deeply perceptive. Strong willpower with an interest in hidden knowledge. Resilient through life's challenges.",
    "Dhanu": "Philosophical, optimistic, and dharma-oriented. Loves travel, higher learning, and spiritual pursuits. Naturally fortunate.",
    "Makara": "Ambitious, disciplined, and structured. Builds steadily toward long-term goals. Practical wisdom with a serious approach.",
    "Kumbha": "Innovative, humanitarian, and independent. Original thinker who values freedom and social causes. Unconventional approach.",
    "Meena": "Spiritual, compassionate, and imaginative. Deep connection to the unseen world. Artistic and empathetic with intuitive wisdom.",
}

ASC_READINGS_HI = {
    "Mesha": "साहसी, अग्रणी और कर्मठ व्यक्तित्व। प्रबल इच्छाशक्ति और शारीरिक ऊर्जा से युक्त जन्मजात नेता। शीघ्र निर्णय लेने वाले और सदैव आगे बढ़ने के लिए तत्पर।",
    "Vrishabha": "स्थिर, कलाप्रिय और धन के प्रति सजग। सुख-सुविधा और सुरक्षा को महत्व देने वाले। धैर्यवान, सौंदर्य, सुरुचिपूर्ण भोजन और सांसारिक सुखों के प्रेमी।",
    "Mithuna": "जिज्ञासु, संवादकुशल और बहुमुखी प्रतिभा के धनी। तीव्र बुद्धि, सीखने और मेल-जोल की प्रवृत्ति। अनुकूलनशील स्वभाव।",
    "Karka": "स्नेही, संवेदनशील, अंतर्ज्ञानी और भावनात्मक रूप से गहरे। घर और परिवार के प्रति अत्यधिक लगाव। रक्षक स्वभाव और प्रबल पूर्वाभास क्षमता।",
    "Simha": "तेजस्वी, आत्मविश्वासी और राजसी स्वभाव। जन्मजात नेतृत्व क्षमता और मान-सम्मान के आकांक्षी। उदार, रचनात्मक और प्रभावशाली व्यक्तित्व।",
    "Kanya": "विश्लेषणात्मक, सेवाभावी और सूक्ष्म दृष्टि वाले। व्यावहारिक दृष्टिकोण, उत्कृष्ट संगठन क्षमता और स्वास्थ्य के प्रति सजग।",
    "Tula": "कुशल रणनीतिकार, संबंधप्रिय और सौंदर्यप्रेमी। जीवन में संतुलन और सामंजस्य के आकांक्षी। न्यायप्रिय और साझेदारी में विश्वास रखने वाले।",
    "Vrishchika": "गंभीर, परिवर्तनकारी और गहन दृष्टि वाले। दृढ़ इच्छाशक्ति, रहस्यमयी ज्ञान में रुचि और जीवन की चुनौतियों से पार पाने में सक्षम।",
    "Dhanu": "दार्शनिक, आशावादी और धर्मपरायण। यात्रा, उच्च शिक्षा और आध्यात्मिक अन्वेषण के प्रेमी। स्वाभाविक रूप से भाग्यशाली।",
    "Makara": "महत्वाकांक्षी, अनुशासित और व्यवस्थित। दीर्घकालिक लक्ष्यों की प्राप्ति हेतु निरंतर प्रयासरत। गंभीर सोच और व्यावहारिक ज्ञान।",
    "Kumbha": "नवीन दृष्टिकोण वाले, मानवतावादी और स्वतंत्र विचारक। मौलिक सोच, सामाजिक सरोकारों और व्यक्तिगत स्वतंत्रता को महत्व देने वाले।",
    "Meena": "आध्यात्मिक, करुणामयी और कल्पनाशील। सूक्ष्म जगत से गहरा जुड़ाव। कलात्मक, संवेदनशील और सहज ज्ञान से युक्त।",
}

SIGNS_HI_MAP = {
    "Mesha": "मेष", "Vrishabha": "वृषभ", "Mithuna": "मिथुन", "Karka": "कर्क",
    "Simha": "सिंह", "Kanya": "कन्या", "Tula": "तुला", "Vrishchika": "वृश्चिक",
    "Dhanu": "धनु", "Makara": "मकर", "Kumbha": "कुम्भ", "Meena": "मीन",
}

LORDS_HI_MAP = {
    "Mars": "मंगल", "Venus": "शुक्र", "Mercury": "बुध", "Moon": "चन्द्र",
    "Sun": "सूर्य", "Jupiter": "बृहस्पति (गुरु)", "Saturn": "शनि", "Rahu": "राहु", "Ketu": "केतु"
}

# --- English Planet In House (Complete for all 9 planets x 12 houses) ---

PLANET_IN_HOUSE = {
    "Sun": {
        1: "Strong personality and leadership. Self-confident with natural authority. Good vitality.",
        2: "Wealth through government or authority. Family pride. Powerful speech.",
        3: "Courageous and bold. Good relationship with siblings. Success through effort.",
        4: "Status through property or vehicles. Connection to the homeland. Respected family lineage.",
        5: "Creative intelligence. Love for leadership and strategy. Blessed with wise children.",
        6: "Victory over competitors. Strong immunity and stamina. Success in administrative fields.",
        7: "Partnerships with influential people. Spouse may be authoritative and dignified.",
        8: "Interest in occult, deep research, and transformation. Strong resilience through adversity.",
        9: "Fortunate father. Connection to dharma, philosophy, and higher learning. Good fortune.",
        10: "Digbala — peak directional strength. Exceptional for career, executive roles, and public acclaim.",
        11: "Large social circle. Gains through government, authorities, or prominent networks. Fulfilled desires.",
        12: "Spiritual inclinations. Overseas travels or living abroad. Detached and charitable nature.",
    },
    "Moon": {
        1: "Emotional, caring, and popular personality. Attractive appearance and empathetic intuition.",
        2: "Wealth accumulation, sweet persuasive speech, and love for family traditions and good food.",
        3: "Mentally active, imaginative, and communicative. Strong emotional bond with siblings.",
        4: "Digbala — emotional comfort, property, vehicles, deep maternal affection, and mental peace.",
        5: "Romantic, highly creative, and emotionally intuitive. Artistic talents and love for learning.",
        6: "Emotional resilience developed through service. Attentive to diet, health, and routine.",
        7: "Charming, social, and sensitive spouse. Success in public dealings and partnerships.",
        8: "Deep psychic intuition, interest in esoteric subjects, and emotional transformation.",
        9: "Spiritual and philosophical disposition. Travel over water, righteous deeds, and fortunate mother.",
        10: "Public popularity and recognition. Career in public service, administration, or creative arts.",
        11: "Large circle of loyal friends. Financial prosperity and fulfilled personal desires.",
        12: "Introspective, spiritual, and imaginative. Deep meditative mind and affinity for travel abroad.",
    },
    "Mars": {
        1: "Energetic, athletic, and courageous. Decisive drive with strong physical stamina.",
        2: "Direct and assertive speech. Wealth generated through initiative and technical skills.",
        3: "Very strong placement. Immense courage, boldness, and success through competition and enterprise.",
        4: "Gains in real estate, land, and vehicles. Active household requiring mutual understanding.",
        5: "Sharp analytical intelligence. Competitive drive in sports and academics.",
        6: "Excellent position. Complete victory over opponents, strong vitality, and triumph in disputes.",
        7: "Passionate partnerships. Strong business acumen; demands active collaboration in marriage.",
        8: "Deep endurance, interest in surgery, technology, or research. Transformative life events.",
        9: "Righteous warrior for principles. Active participant in dharmic causes and pilgrimages.",
        10: "Digbala / Kuldeepak yoga — supreme leadership, executive authority, engineering, and career glory.",
        11: "Substantial gains through enterprise, influential allies, and ambitious accomplishments.",
        12: "Foreign enterprise or connections. Energy channeled toward charitable or institutional work.",
    },
    "Mercury": {
        1: "Quick-witted, articulate, and youthful demeanor. Versatile intellect and sharp commercial mind.",
        2: "Eloquent, diplomatic speech. Financial expertise, accounting skills, and wealth through commerce.",
        3: "Exceptional skills in writing, communications, IT, and media. Inquisitive mind.",
        4: "Intellectual domestic environment, good formal education, mental peace, and maternal guidance.",
        5: "High intellect, analytical brilliance, creative writing, and astute strategic thinking.",
        6: "Master of debate and problem-solving. Success in competitive exams, banking, law, or analysis.",
        7: "Intelligent, pragmatic, and communicative partner. Lucrative business partnerships.",
        8: "Talent in esoteric research, astrology, data analysis, and deep investigative work.",
        9: "Higher learning, philosophy, publishing, and righteous counsel. Respected for wisdom.",
        10: "Excellence in trade, media, software, administration, or corporate management.",
        11: "Diverse income streams, intellectual social networks, and successful business ventures.",
        12: "International commerce, solitary research, vivid imagination, and philosophical contemplation.",
    },
    "Jupiter": {
        1: "Digbala — wise, optimistic, dignified, and respected personality. Good health and divine grace.",
        2: "Prosperous family lineage, learned and truthful speech, and steady accumulation of wealth.",
        3: "Virtuous communications, supportive siblings, and natural talent in teaching or advisory roles.",
        4: "Spacious residence, vehicles, strong maternal blessing, and profound inner satisfaction.",
        5: "Exceptional wisdom, purva punya (past merit), brilliant progeny, and noble judgment.",
        6: "Peaceful resolution of conflicts through wisdom. Excellent in legal or counseling services.",
        7: "Virtuous, loyal, and fortunate spouse. Harmonious marital life and prosperous alliances.",
        8: "Deep metaphysical wisdom, longevity, divine protection during trials, and occult insight.",
        9: "Supreme placement. Highly fortunate, spiritually elevated, blessed by mentors and elders.",
        10: "Prominent career, respected leadership, government honor, and exemplary moral standing.",
        11: "Great abundance, fulfillment of aspirations, influential friendships, and social prestige.",
        12: "Expenditure on noble and religious causes. Deep affinity for meditation and spiritual liberation.",
    },
    "Venus": {
        1: "Charming, charismatic, and refined personality. Natural affinity for beauty, fashion, and the arts.",
        2: "Sweet, persuasive speech. Financial prosperity, luxury items, and fondness for fine dining.",
        3: "Talents in music, drama, creative writing, or design. Pleasant travels and harmonious relations.",
        4: "Digbala — luxurious residence, fine vehicles, domestic happiness, and aesthetic surroundings.",
        5: "Romantic nature, artistic creativity, joyful romance, and affectionate relationship with children.",
        6: "Success in service, design, or wellness sectors. Benefits from balanced daily lifestyle habits.",
        7: "Exceptional for marriage. Loving, attractive, and supportive spouse with shared prosperity.",
        8: "Unearned gains, marital prosperity, longevity, and appreciation for esoteric mysticism.",
        9: "Fortune through arts, culture, and auspicious travels. High ethical and aesthetic ideals.",
        10: "Flourishing career in media, entertainment, luxury goods, design, cinema, or hospitality.",
        11: "Abundant wealth, affluent social circle, luxurious comforts, and fulfilled material desires.",
        12: "Luxurious lifestyle, overseas travels, artistic enjoyment, and spiritual devotion.",
    },
    "Saturn": {
        1: "Disciplined, mature, and patient personality. Steady development leading to lasting success.",
        2: "Prudent financial habits, measured speech, and solid, enduring wealth built over time.",
        3: "Persistent courage, technical aptitude, and relentless drive to overcome obstacles.",
        4: "Gains through land, traditional properties, and agriculture. Responsible domestic duties.",
        5: "Methodical, serious thinker. Deep interest in science, history, or classical philosophy.",
        6: "Supreme placement. Complete defeat of adversaries, relief from debts, and tireless perseverance.",
        7: "Digbala — mature, faithful, and stabilizing partner. Enduring commitments and reliability.",
        8: "Ayushman yoga — exceptional longevity, scientific research acumen, and deep resilience.",
        9: "Traditional, philosophical mindset. Hard-earned fortune achieved through honesty and patience.",
        10: "Remarkable career rise through hard work, administrative capability, and executive authority.",
        11: "Consistent financial growth, loyal friends, and realization of long-term life goals.",
        12: "Spiritual detachment, love of solitude, and successful ties with foreign organizations.",
    },
    "Rahu": {
        1: "Unconventional, ambitious, and charismatic personality. Trailblazing mindset and global appeal.",
        2: "Financial gains through technology, foreign avenues, or modern markets. Diplomatic speech.",
        3: "Great bravery, boldness, and extraordinary success in media, internet, sports, or politics.",
        4: "Modern domestic environment, extensive travel, and residence away from birthplace.",
        5: "Keen speculative acumen, sharp inventive intelligence, and interest in cutting-edge tech.",
        6: "Superb position. Total destruction of opposition, victory in competitions, and fearless drive.",
        7: "Unconventional or foreign spouse. Broad international exposure and dynamic partnerships.",
        8: "Deep investigative abilities, cybersecurity or data science talent, and sudden windfalls.",
        9: "Unorthodox perspectives, multicultural exposure, and rewarding foreign journeys.",
        10: "Spectacular rise in career, media, politics, or multinational enterprises.",
        11: "Immense gains, diverse revenue streams, influential networks, and rapid elevation.",
        12: "Overseas relocation, multinational business, and inclination toward mystical retreats.",
    },
    "Ketu": {
        1: "Spiritual, introspective, and detached demeanor. Powerful intuition and search for truth.",
        2: "Spiritual and philosophical speech. Non-materialistic approach to wealth and family.",
        3: "Subtle inner bravery, analytical depth, independent work ethic, and technical aptitude.",
        4: "Search for inner peace, detachment from material surroundings, and meditative mindset.",
        5: "Deep spiritual intelligence, karmic intuition, and mastery of traditional or sacred texts.",
        6: "Overcoming difficulties through spiritual resilience. Inclination toward healing or yoga.",
        7: "Spiritual or simple-hearted spouse. Emphasis on soul connection over worldly glamour.",
        8: "Remarkable occult intuition, metaphysical mastery, research depth, and transformative insights.",
        9: "Sacred pilgrimages, deep spiritual devotion, and dedication to righteous principles.",
        10: "Distinction in advisory, scientific research, charitable, or spiritual pursuits.",
        11: "Unexpected karmic blessings, virtuous associations, and fulfillment of higher life goals.",
        12: "Moksha Karaka — supreme placement for spiritual awakening, meditation, and inner liberation.",
    },
}

# --- Classical Jyotish Hindi Planet In House (Complete for all 9 planets x 12 houses) ---

PLANET_IN_HOUSE_HI = {
    "Sun": {
        1: "तेजस्वी, प्रभावशाली और नेतृत्व क्षमता से युक्त व्यक्तित्व। स्वाभिमानी स्वभाव एवं उत्तम शारीरिक ओज व जीवन शक्ति।",
        2: "पैतृक संपत्ति व शासन-प्रशासन से धन लाभ। वाणी में दृढ़ता एवं अधिकार भाव, परिवार में प्रतिष्ठा।",
        3: "अत्यंत साहसी, पराक्रमी और पराक्रम से भाग्योदय। बंधु-बांधवों से संबंध और पुरुषार्थ द्वारा सफलता।",
        4: "भूमि, भवन और वाहन सुख में प्रतिष्ठा। मातृभूमि व कुल-परिवार के प्रति गहरा अनुराग एवं सम्मान।",
        5: "कुशाग्र बुद्धि, रचनात्मक मेधा और नेतृत्व क्षमता। संतति सुख तथा ज्ञान व उच्च चिंतन में रुचि।",
        6: "शत्रुहंता योग, विरोधियों पर विजय और रोग प्रतिरोधक क्षमता। सेवा, प्रशासन अथवा प्रतिस्पर्धा में श्रेष्ठ सफलता।",
        7: "प्रभावशाली व स्वाभिमानी जीवनसाथी। साझेदारी और सार्वजनिक जीवन में मान-सम्मान एवं प्रभाव।",
        8: "गूढ़ विद्याओं, तंत्र-मंत्र और अनुसंधान में रुचि। जीवन में आकस्मिक परिवर्तन और आंतरिक आत्मबल।",
        9: "धर्मनिष्ठ, भाग्यशाली और पिता के प्रति सम्मान। उच्च शिक्षा, तीर्थाटन और ईश्वर कृपा से भाग्योदय।",
        10: "दशम भाव में सूर्य का 'दिग्बल' — करियर में सर्वोच्च सफलता, शासन-प्रशासन, उच्च पद व राजकीय मान-सम्मान।",
        11: "विशाल सामाजिक संपर्क, शासन या उच्चाधिकारियों से प्रचुर लाभ। महत्वाकांक्षाओं और अभिलाषाओं की पूर्ति।",
        12: "अध्यात्म और मोक्ष मार्ग में रुचि। विदेशी संपर्कों या दूरस्थ स्थानों से लाभ, एकांत प्रिय और परोपकारी स्वभाव।",
    },
    "Moon": {
        1: "संवेदनशील, सौम्य और आकर्षक व्यक्तित्व। लोकप्रिय स्वभाव, कल्पनाशीलता एवं दयालुता।",
        2: "धन और संपत्ति में वृद्धि, मिष्टभाषी और आकर्षक वाणी। पारिवारिक सुख और सुरुचिपूर्ण भोजन के प्रेमी।",
        3: "सक्रिय और रचनात्मक मन, उत्कृष्ट संवाद क्षमता। यात्राओं के शौकीन और भाई-बहनों से स्नेहपूर्ण संबंध।",
        4: "चतुर्थ भाव में चंद्रमा का 'दिग्बल' — मातृसुख, सुंदर वाहन, गृह सुख और मन की अपार शांति।",
        5: "प्रखर कल्पनाशीलता, कलात्मक और भावुक मन। संतति से प्रेम, विद्या और मंत्र साधना में रुचि।",
        6: "दूसरों की सेवा और सहायता में सुख। मानसिक तनाव या कफ संबंधित स्वास्थ्य पर ध्यान देना हितकर।",
        7: "सुंदर, गुणवान और संवेदनशील जीवनसाथी। व्यापारिक साझेदारी और लोक-व्यवहार में लोकप्रियता।",
        8: "गहन अंतर्ज्ञान, रहस्यमयी विषयों में रुचि। पैतृक धन लाभ किंतु मानसिक शांति का विशेष ध्यान रखें।",
        9: "धार्मिक, दार्शनिक और भाग्यवान। जल यात्राओं के योग, माता का सहयोग और परोपकारी प्रवृत्ति।",
        10: "करियर में लोकप्रियता और जन-संपर्क। सार्वजनिक कार्यों, व्यापार या समाज सेवा में विशेष प्रतिष्ठा।",
        11: "असंख्य मित्र और समृद्ध सामाजिक नेटवर्क। महिला वर्ग से विशेष लाभ एवं मनोकामनाओं की सहज पूर्ति।",
        12: "आध्यात्मिक चिंतन, एकांत साधना और सूक्ष्म विषयों की समझ। विदेश यात्रा या विदेशी भूमि पर निवास के योग।",
    },
    "Mars": {
        1: "ऊर्जावान, साहसी और निडर व्यक्तित्व। शारीरिक बल, दृढ़ निश्चय और त्वरित निर्णय लेने की क्षमता।",
        2: "स्पष्ट और तेज वाणी। स्वयं के पुरुषार्थ से धनार्जन, तकनीकी व भूमि संबंधी कार्यों से लाभ।",
        3: "तृतीय भाव में मंगल अत्यंत शुभ — अदम्य साहस, पराक्रम, खेलकूद व सेना/प्रशासन में भारी सफलता।",
        4: "अचल संपत्ति, भूमि, भवन और वाहनों का उत्तम सुख। पारिवारिक जीवन में शांति बनाए रखना श्रेयस्कर।",
        5: "कुशाग्र व रणनीतिक बुद्धि। प्रतिस्पर्धात्मक परीक्षाओं में सफलता, संतति के प्रति सुरक्षात्मक दृष्टिकोण।",
        6: "शत्रु-जयी, कर्जों से मुक्ति और उत्तम स्वास्थ्य। चिकित्सा, वकालत, पुलिस या सेना में उच्च सफलता।",
        7: "ऊर्जावान और महत्वाकांक्षी जीवनसाथी। दांपत्य जीवन में परस्पर सम्मान व सामंजस्य आवश्यक।",
        8: "गूढ़ अन्वेषण, शल्य चिकित्सा या अनुसंधान में सफलता। अप्रत्याशित घटनाओं से निपटने का असीम आत्मबल।",
        9: "धार्मिक सिद्धांतों के रक्षक, साहसी और न्यायप्रिय। तीर्थ यात्राओं और सत्कर्मों में सक्रिय भागीदारी।",
        10: "दशम भाव में मंगल का 'कुलदीपक योग' — करियर में अपार सफलता, नेतृत्व, तकनीकी या प्रशासनिक प्रतिष्ठा।",
        11: "उद्यमशीलता और साहस से धन व लाभ की प्रचुर प्राप्ति। प्रभावशाली मित्रों का सहयोग और लक्ष्य सिद्धि।",
        12: "दूरस्थ स्थानों या विदेशों से व्यापारिक संबंध। ऊर्जा का सदुपयोग और आत्म-अनुशासन आवश्यक।",
    },
    "Mercury": {
        1: "तीव्र बुद्धि, हाजिरजवाबी और आकर्षक संवाद शैली। युवा जैसा उत्साह, बहुमुखी प्रतिभा और व्यापारिक समझ।",
        2: "अत्यंत मधुर और प्रभावशाली वाणी, उत्कृष्ट वित्तीय प्रबंधन। वाणी आधारित कार्यों से प्रचुर धनलाभ।",
        3: "लेखन, पत्रकारिता, मीडिया व संचार में असाधारण कौशल। भाई-बहनों से मधुर संबंध और बौद्धिक सक्रियता।",
        4: "उच्च शिक्षा, बौद्धिक वातावरण और सुखद गृहस्थ जीवन। माता से ज्ञान और अच्छे वाहन का सुख।",
        5: "असाधारण मेधा, गणितीय व विश्लेषणात्मक क्षमता। शेयर बाजार, शोध अथवा शिक्षा में विशेष सफलता।",
        6: "तर्कशक्ति और विश्लेषणात्मक क्षमता से विरोधियों पर विजय। बैंकिंग, एकाउंट्स या सेवा क्षेत्र में उत्तम प्रदर्शन।",
        7: "बुद्धिमान, चतुर और व्यावहारिक जीवनसाथी। व्यापारिक साझेदारी और वाणिज्यिक सौदों में उत्कृष्ट लाभ।",
        8: "गूढ़ शोध, डेटा विश्लेषण, ज्योतिष या रहस्यमयी विद्याओं में प्रवीणता। दीर्घायु और पैतृक लाभ।",
        9: "उच्च विद्या, धर्मशास्त्र और दर्शन में गहरी रुचि। लेखन, प्रकाशन और विद्वानों से सम्मान।",
        10: "व्यापार, प्रबंधन, सूचना प्रौद्योगिकी (IT) या संचार में उच्च पद। बौद्धिक कौशल से करियर में प्रतिष्ठा।",
        11: "विविध स्रोतों से निरंतर आय। बौद्धिक मित्रों का समूह, व्यापारिक योजनाओं से भरपूर सफलता।",
        12: "विदेशी व्यापार, अनुसंधान या एकांत चिंतन से लाभ। तीव्र कल्पनाशीलता और अंतर्मुखी बौद्धिक चिंतन।",
    },
    "Jupiter": {
        1: "प्रथम भाव में बृहस्पति का 'दिग्बल' — ज्ञानी, उदार, नीतिवान और सर्वत्र सम्मानित व्यक्तित्व। दीर्घायु और ईश्वर कृपा।",
        2: "संस्कारवान कुल, समृद्ध परिवार और ज्ञानवर्धक वाणी। संचित धन में निरंतर वृद्धि और सत्यवादिता।",
        3: "सदाचारी, ज्ञानवर्धक संवाद और बंधुओं का शुभ सहयोग। लेखन, परामर्श और अध्यापन में प्रतिष्ठा।",
        4: "गृह-सुख, मातृकृपा, विशाल भवन और वाहनों की प्राप्ति। मन में संतोष और आध्यात्मिक शांति।",
        5: "पूर्व जन्म के पुण्यों का उदय — असाधारण ज्ञान, मंत्र सिद्धि, श्रेष्ठ संतति सुख और विवेकपूर्ण निर्णय।",
        6: "सदाचार और ज्ञान से विरोधियों का शमन। स्वास्थ्य के प्रति सचेत, सेवा भाव और न्यायिक कार्यों में सफलता।",
        7: "चरित्रवान, संस्कारी और भाग्यशाली जीवनसाथी। सुखी वैवाहिक जीवन और सफल सामाजिक साझेदारी।",
        8: "गूढ़ आध्यात्मिक ज्ञान, दीर्घायु और अप्रत्याशित दैवीय सहायता। मोक्ष व रहस्यमयी विद्याओं में रुचि।",
        9: "नवम भाव में गुरु अत्यंत श्रेष्ठ — परम भाग्यशाली, गुरु-कृपा प्राप्त, धर्मपरायण और समाज में पूज्यनीय।",
        10: "सदाचारी करियर, उच्च सामाजिक प्रतिष्ठा, न्यायाधीश, सलाहकार, प्रोफेसर या उच्च प्रशासनिक पद।",
        11: "अथाह धनलाभ, मनोवांछित फल की प्राप्ति, उच्चवर्गीय सज्जनों का साथ और समाज में प्रतिष्ठा।",
        12: "धार्मिक कार्यों और परोपकार में व्यय। मोक्ष मार्ग में अग्रसर, तीर्थाटन और आत्मिक शांति।",
    },
    "Venus": {
        1: "अत्यंत आकर्षक, सौम्य और कलात्मक व्यक्तित्व। सौंदर्य, कला, संगीत और विलासिता के प्रति स्वाभाविक रुचि।",
        2: "सुंदर मुखाकृति, मधुर वाणी और आभूषण-वस्त्रों से सुसज्जित। परिवार में समृद्धि और स्वादिष्ट भोजन के शौकीन।",
        3: "ललित कलाओं, गायन, अभिनय या लेखन में रुचि। मधुर संबंध, सुरुचिपूर्ण जीवनशैली और आनंदमय यात्राएं।",
        4: "चतुर्थ भाव में शुक्र का 'दिग्बल' — आलीशान भवन, सुंदर वाहन, मातृसुख और भौतिक सुख-सुविधाओं की प्रचुरता।",
        5: "रोमांटिक और रचनात्मक स्वभाव, कलात्मक प्रतिभा। सुयोग्य व गुणी संतान, प्रेम संबंधों में मधुरता।",
        6: "कला या सौंदर्य प्रसाधनों के व्यापार में सफलता। स्वास्थ्य व आहार-विहार में संतुलन रखना लाभप्रद।",
        7: "सप्तम भाव में शुक्र — अत्यंत रूपवान, सुसंस्कृत और निष्ठावान जीवनसाथी। दांपत्य जीवन में प्रेम व सामंजस्य।",
        8: "आकस्मिक धन लाभ, वसीयत या विवाह से संपत्ति की प्राप्ति। दीर्घायु और गूढ़ सौंदर्यशास्त्र में रुचि।",
        9: "कला, संस्कृति और धार्मिक स्थलों की यात्राओं से भाग्योदय। उच्च स्तरीय ज्ञान और भाग्य का साथ।",
        10: "सिनेमा, फैशन, मीडिया, डिजाइनिंग, आतिथ्य या विलासिता उद्योग में करियर। कार्यक्षेत्र में यश।",
        11: "विपुल धनलाभ, विलासिता के साधनों की प्राप्ति, कलाप्रेमी व प्रभावशाली मित्रों का संग।",
        12: "द्वादश भाव में शुक्र अत्यंत शुभ — भोग, ऐश्वर्य, शय्या सुख और विदेशी भूमि पर विलासितापूर्ण जीवन।",
    },
    "Saturn": {
        1: "गंभीर, विचारशील, अनुशासित और धैर्यवान व्यक्तित्व। जीवन में संघर्ष के उपरांत दृढ़ और स्थायी सफलता।",
        2: "मितव्ययी, संभलकर बोलने वाले और व्यावहारिक। धीरे-धीरे किंतु मजबूत वित्तीय आधार का निर्माण।",
        3: "कठिन परिश्रम और धैर्य से भाग्योदय। तकनीकी कौशल, साहसी कदम और विरोधियों पर दबदबा।",
        4: "पारिवारिक जिम्मेदारियों का निर्वहन। भूमि, पुरानी संपत्ति या खनिज से लाभ, सादगीपूर्ण जीवन।",
        5: "गंभीर चिंतन, दर्शन और तकनीकी अध्ययन में रुचि। संतति के प्रति कर्तव्यनिष्ठ दृष्टिकोण।",
        6: "षष्ठ भाव में शनि अत्यंत बलवान — शत्रुओं का पूर्ण पराभव, मुकदमों में विजय, अटूट रोग-प्रतिरोधक क्षमता।",
        7: "सप्तम भाव में शनि का 'दिग्बल' — परिपक्व, निष्ठावान और गंभीर जीवनसाथी। विवाह के बाद स्थायित्व व उन्नति।",
        8: "अष्टम भाव में शनि — दीर्घायु (आयुष्मान योग), अनुसंधान, पुरातत्व, बीमा या गूढ़ विषयों में सफलता।",
        9: "परंपरागत धर्म और न्याय के प्रति गहरी निष्ठा। धीमा किंतु अटूट भाग्योदय, जन-कल्याण के कार्यों में रुचि।",
        10: "कर्मठ, न्यायप्रिय और संगठनात्मक क्षमता से युक्त। लोक सेवा, उद्योग, राजनीति या कारपोरेट में स्थायी शीर्ष पद।",
        11: "निरंतर और स्थायी आय, दीर्घकालिक निवेशों से प्रचुर लाभ। निष्ठावान और सहयोगी मित्रों का साथ।",
        12: "आध्यात्मिक वैराग्य, एकांत साधना और विदेशी संपर्कों से लाभ। परोपकारी और शांत स्वभाव।",
    },
    "Rahu": {
        1: "असामान्य, क्रांतिकारी और महत्वाकांक्षी व्यक्तित्व। पारंपरिक सीमाओं से परे सोचने वाले, विदेश में प्रभाव।",
        2: "विदेशी भाषाओं, आधुनिक वित्तीय बाजारों या तकनीक से धन लाभ। कूटनीतिक और प्रभावशाली वाणी।",
        3: "तृतीय भाव में राहु परम बलवान — निर्भय, पराक्रमी, मीडिया, इंटरनेट, खेल या राजनीति में अप्रत्याशित सफलता।",
        4: "विदेशी शैली का घर, आधुनिक सुख-सुविधाएं। मातृभूमि से दूर या विदेशों में निवास के प्रबल योग।",
        5: "आधुनिक तकनीक, शेयर बाजार, कोडिंग या नवाचार में तीक्ष्ण बुद्धि। विलक्षण सोच और बौद्धिक प्रतिभा।",
        6: "षष्ठ भाव में राहु परम शुभ — सभी शत्रुओं का दमन, प्रतिस्पर्धाओं में अजेय, मुकदमों और बाधाओं पर विजय।",
        7: "विदेशी या भिन्न पृष्ठभूमि से जीवनसाथी। अंतरराष्ट्रीय व्यापार और सार्वजनिक सौदों में विस्तार।",
        8: "गूढ़ शोध, डेटा साइंस, साइबर सुरक्षा या गुप्त विद्याओं में गहरी पैठ। अचानक वित्तीय लाभ।",
        9: "परंपराओं से हटकर स्वतंत्र विचार, विदेशी यात्राएं और बहुसांस्कृतिक दृष्टिकोण से भाग्योदय।",
        10: "दशम भाव में राहु अत्यंत शक्तिशाली — राजनीति, मीडिया, तकनीक या वैश्विक स्तर पर त्वरित व विशाल सफलता।",
        11: "एकादश भाव में राहु — अपार धनलाभ, कई अनपेक्षित स्रोतों से आय, प्रभावशाली संपर्कों से उन्नति।",
        12: "विदेश गमन, अंतरराष्ट्रीय कंपनियों में कार्य, ध्यान और रहस्यमयी अनुभवों की ओर झुकाव।",
    },
    "Ketu": {
        1: "आध्यात्मिक, अंतर्मुखी और तत्वज्ञानी व्यक्तित्व। भौतिक जगत से अनासक्ति, तीव्र अंतर्ज्ञान और स्वतंत्र आत्मा।",
        2: "आध्यात्मिक और दार्शनिक वाणी। गुप्त ज्ञान, सात्विक जीवन और भौतिक मोह से परे सोच।",
        3: "अद्भुत आंतरिक साहस, लेखन, शोध और तकनीकी दक्षता। एकांत में एकाग्र होकर कार्य करने की क्षमता।",
        4: "आंतरिक शांति और ध्यान में सुख। मातृभूमि से दूर आध्यात्मिक वातावरण में मानसिक शांति।",
        5: "पूर्व जन्म के ज्ञान का भंडार, असाधारण अंतर्दृष्टि, वैदिक मंत्र साधना और गुप्त विद्याओं में प्रवीणता।",
        6: "विरोधियों और बाधाओं का आध्यात्मिक शक्ति से शमन। सेवा भाव, चिकित्सा या योग में सफलता।",
        7: "आध्यात्मिक और सरल जीवनसाथी। दांपत्य जीवन में भौतिक से अधिक आत्मिक जुड़ाव का महत्व।",
        8: "अष्टम भाव में केतु — तीव्र अंतर्ज्ञान, पराविज्ञान, गुप्त विद्याओं और ध्यान में उच्चतम सिद्धियां।",
        9: "नवम भाव में केतु — उच्च आध्यात्मिक चेतना, तीर्थाटन, ईश्वर के प्रति पूर्ण समर्पण और मोक्ष साधना।",
        10: "निस्वार्थ भाव से कार्य, परामर्श, शोध या आध्यात्मिक संस्थाओं में मान-सम्मान एवं प्रतिष्ठा।",
        11: "अपेक्षाओं से परे अचानक लाभ। संत-महात्माओं का संग और जीवन के उच्चतर लक्ष्यों की पूर्ति।",
        12: "द्वादश भाव में केतु 'मोक्ष कारक' — आध्यात्मिक मुक्ति, ध्यान, समाधि और परम शांति की प्राप्ति।",
    },
}

# --- Dignities ---

DIGNITY_READINGS = {
    "exalted": "is exalted — operating at peak strength. Its positive qualities shine brightly.",
    "debilitated": "is debilitated — facing challenges expressing its energy. Growth comes through overcoming these obstacles.",
    "own_sign": "is in its own sign — comfortable, confident, and functioning well in its natural domain.",
    "neutral": "is in a neutral position — performing adequately with moderate strength.",
}

DIGNITY_READINGS_HI = {
    "exalted": "उच्च राशिस्थ हैं — अपनी पूर्ण एवं सर्वोच्च शक्ति में विद्यमान। इनके शुभ फल प्रचुरता से प्राप्त होंगे।",
    "debilitated": "नीच राशिस्थ हैं — अपने स्वाभाविक फलों की अभिव्यक्ति में चुनौतियों का सामना करेंगे। वैदिक उपाय और शांति लाभदायक रहेगी।",
    "own_sign": "अपनी स्वराशि में स्थित हैं — अत्यंत सहज, बली और अपने प्राकृतिक कारकतत्वों में श्रेष्ठ परिणाम देने वाले।",
    "neutral": "सम राशि में स्थित हैं — मध्यम और संतुलित फल प्रदान करने की स्थिति में हैं।",
}

RETROGRADE_READING = (
    "Being retrograde, {planet}'s energy is internalized and intensified. "
    "Past-life karmic themes related to {planet}'s significations are highlighted. "
    "Results may be delayed but ultimately deeper and more transformative."
)

RETROGRADE_READING_HI = (
    "वक्री होने के कारण, {planet} की ऊर्जा आंतरिक एवं अत्यंत गहन हो जाती है। "
    "पूर्व जन्म के प्रारब्ध कर्मों से जुड़े विषय सक्रिय होंगे तथा परिणाम कुछ विलंब से किंतु गहरे व परिवर्तनकारी प्राप्त होंगे।"
)

# --- Yogas & Doshas Hindi Mappings ---

YOGA_HI_MAP = {
    "Gajakesari Yoga": ("गजकेसरी योग", "गुरु-चंद्र संबंध से विद्या, धन, मान-सम्मान और अखंड यश की प्राप्ति।"),
    "Budhaditya Yoga": ("बुधादित्य योग", "सूर्य-बुध युति से कुशाग्र बुद्धि, संचार कौशल और बौद्धिक सफलता।"),
    "Chandra-Mangal Yoga": ("चन्द्र-मंगल योग", "चंद्र-मंगल युति से साहस, उद्यम और धनार्जन के श्रेष्ठ योग।"),
    "Dhana Yoga": ("धन योग", "धन भाव अथवा लाभ भाव के स्वामी की शुभ स्थिति से धन संचय के योग।"),
    "Raj Yoga": ("राजयोग", "केंद्र और त्रिकोण के स्वामियों के संबंध से सत्ता, अधिकार, उच्च पद और प्रतिष्ठा।"),
    "Viparita Raj Yoga": ("विपरीत राजयोग", "त्रिक भावों के स्वामियों के परस्पर संबंध से विपरीत परिस्थितियों में अभूतपूर्व सफलता।"),
    "Neechabhanga Raj Yoga": ("नीचभंग राजयोग", "नीच ग्रह के दोष का परिहार होकर असाधारण सफलता व शक्ति की प्राप्ति।"),
    "Adhi Yoga": ("अधि योग", "चंद्रमा से शुभ ग्रहों की विशेष स्थिति से नेतृत्व क्षमता व सामाजिक सम्मान।"),
    "Saraswati Yoga": ("सरस्वती योग", "बुध, गुरु और शुक्र के शुभ प्रभाव से विद्या, संगीत, कला व वाणी में असाधारण प्रतिभा।"),
    "Ruchaka Yoga": ("रुचक योग", "मंगल के केंद्र में स्वराशि/उच्च होने से पराक्रम, साहस और प्रशासनिक शक्ति।"),
    "Bhadra Yoga": ("भद्र योग", "बुध के केंद्र में स्वराशि/उच्च होने से कुशाग्र मेधा, वाणी और व्यापार में सफलता।"),
    "Hamsa Yoga": ("हंस योग", "गुरु के केंद्र में स्वराशि/उच्च होने से धार्मिक ज्ञान, सदाचार और समाज में पूज्यता।"),
    "Malavya Yoga": ("मालव्य योग", "शुक्र के केंद्र में स्वराशि/उच्च होने से सौंदर्य, कला, वाहन और वैभव का सुख।"),
    "Shasha Yoga": ("शश योग", "शनि के केंद्र में स्वराशि/उच्च होने से न्यायप्रियता, जन-समर्थन और स्थायी सत्ता।"),
}

DOSHA_HI_MAP = {
    "Mangal Dosha (Manglik)": "मांगलिक दोष (मंगल दोष)",
    "Kaal Sarp Dosha": "कालसर्प दोष",
    "Pitra Dosha": "पितृ दोष",
    "Surya Grahan Dosha": "सूर्य ग्रहण दोष",
    "Chandra Grahan Dosha": "चन्द्र ग्रहण दोष",
    "Kemdrum Dosha": "केमद्रुम दोष",
    "Shani Sadhe Sati": "शनि साढ़े साती",
    "Shani Dhayya": "शनि ढैय्या",
}

SEVERITY_HI_MAP = {
    "high": "तीव्र प्रभाव",
    "moderate": "मध्यम प्रभाव",
    "low": "अल्प प्रभाव",
    "cancelled": "भंग / निष्फल",
}


def generate_basic_reading(
    planets: list,
    houses: list,
    ascendant: dict,
    yogas: list,
    doshas: list,
    language: str = "en",
) -> dict:
    """Generate a comprehensive rule-based reading in English or Classical Jyotish Hindi."""

    reading = {
        "ascendant": "",
        "personality": "",
        "planets": [],
        "key_strengths": [],
        "key_challenges": [],
        "career": "",
        "relationships": "",
        "summary": "",
    }

    # --- Ascendant Reading ---
    asc_sign = ascendant["sign"]
    if language == "hi":
        sign_hi = SIGNS_HI_MAP.get(asc_sign, asc_sign)
        lord_hi = LORDS_HI_MAP.get(ascendant.get("lord", ""), ascendant.get("lord", ""))
        reading["ascendant"] = ASC_READINGS_HI.get(asc_sign, f"{sign_hi} लग्न।")
        # In Hindi mode: purely Devanagari, no English parenthetical sign name
        reading["personality"] = (
            f"लग्न में {sign_hi} उदित होने से, "
            f"लग्नेश {lord_hi} हैं। "
            f"{ASC_READINGS_HI.get(asc_sign, '')}"
        )
    else:
        reading["ascendant"] = ASC_READINGS.get(asc_sign, f"Ascendant in {asc_sign}.")
        reading["personality"] = (
            f"With {asc_sign} ({ascendant.get('sign_english', '')}) rising, "
            f"the Ascendant lord is {ascendant.get('lord', '')}. "
            f"{ASC_READINGS.get(asc_sign, '')}"
        )

    # --- Planet-by-planet readings ---
    strengths = []
    challenges = []

    for p in planets:
        pname = p["name"]
        house = p["house"]
        dignity = p.get("dignity", "neutral")

        if language == "hi":
            p_hi = LORDS_HI_MAP.get(pname, p.get("vedic_name", pname))
            s_hi = SIGNS_HI_MAP.get(p["sign"], p["sign"])
            placement_str = f"भाव {house} में {s_hi} राशि में {p_hi} की स्थिति"

            # House placement text in Hindi
            house_text = PLANET_IN_HOUSE_HI.get(pname, {}).get(house, "")
            full_text = house_text

            # Dignity text in Hindi
            dignity_text = DIGNITY_READINGS_HI.get(dignity, "")
            if dignity_text:
                full_text = (full_text + " " if full_text else "") + f"{p_hi} {dignity_text}"

            # Retrograde text in Hindi
            if p.get("retrograde") and pname not in ("Rahu", "Ketu"):
                full_text = (full_text + " " if full_text else "") + RETROGRADE_READING_HI.format(planet=p_hi)

            planet_reading = {
                "name": pname,
                "vedic_name": p_hi,
                "placement": placement_str,
                "reading": full_text,
            }

            # Strengths & challenges in Hindi
            if dignity == "exalted":
                strengths.append(f"{p_hi} {s_hi} (भाव {house}) में उच्च राशिस्थ")
            elif dignity == "own_sign":
                strengths.append(f"{p_hi} अपनी स्वराशि {s_hi} में सशक्त")
            elif dignity == "debilitated":
                challenges.append(f"{p_hi} {s_hi} में नीच राशिस्थ — वैदिक उपाय व शांति आवश्यक")

            if house in [6, 8, 12] and pname not in ("Rahu", "Ketu"):
                challenges.append(f"{p_hi} त्रिक भाव (भाव {house}) में स्थित")

        else:
            placement_str = f"{pname} in {p['sign']} ({p.get('sign_english', '')}) in House {house}"
            house_text = PLANET_IN_HOUSE.get(pname, {}).get(house, "")
            full_text = house_text

            dignity_text = DIGNITY_READINGS.get(dignity, "")
            if dignity_text:
                full_text = (full_text + " " if full_text else "") + f"{pname} {dignity_text}"

            if p.get("retrograde") and pname not in ("Rahu", "Ketu"):
                full_text = (full_text + " " if full_text else "") + RETROGRADE_READING.format(planet=pname)

            planet_reading = {
                "name": pname,
                "vedic_name": p.get("vedic_name", pname),
                "placement": placement_str,
                "reading": full_text,
            }

            if dignity == "exalted":
                strengths.append(f"{pname} exalted in {p['sign']} (House {house})")
            elif dignity == "own_sign":
                strengths.append(f"{pname} strong in own sign {p['sign']}")
            elif dignity == "debilitated":
                challenges.append(f"{pname} debilitated in {p['sign']} — needs remedial attention")

            if house in [6, 8, 12] and pname not in ("Rahu", "Ketu"):
                challenges.append(f"{pname} in dusthana House {house}")

        reading["planets"].append(planet_reading)

    # Add yoga-based strengths
    for yoga in yogas:
        if yoga.get("category") == "benefic":
            if language == "hi":
                mapped = YOGA_HI_MAP.get(yoga["name"])
                y_name = yoga.get("name_hi") or (mapped[0] if mapped else yoga["name"])
                y_desc = yoga.get("description_hi") or (mapped[1] if mapped else yoga.get("description", ""))
                strengths.append(f"{y_name} — {y_desc[:80]}")
            else:
                strengths.append(f"{yoga['name']} — {yoga['description'][:80]}")

    # Add dosha-based challenges
    for dosha in doshas:
        if dosha.get("present") and dosha.get("severity") not in ("none", "cancelled"):
            if language == "hi":
                d_name = dosha.get("name_hi") or DOSHA_HI_MAP.get(dosha["name"], dosha["name"])
                sev_hi = SEVERITY_HI_MAP.get(dosha.get("severity", ""), dosha.get("severity", ""))
                challenges.append(f"{d_name} ({sev_hi})")
            else:
                challenges.append(f"{dosha['name']} ({dosha['severity']})")

    reading["key_strengths"] = strengths[:8]
    reading["key_challenges"] = challenges[:8]

    # --- Career indicators ---
    house_10_planets = [p for p in planets if p["house"] == 10]
    house_10_data = next((h for h in houses if h["house"] == 10), None)
    career_text = ""
    if language == "hi":
        if house_10_planets:
            names_hi = [LORDS_HI_MAP.get(p["name"], p.get("vedic_name", p["name"])) for p in house_10_planets]
            career_text = f"दशम (कर्म) भाव में {', '.join(names_hi)} स्थित हैं। "
            names = [p["name"] for p in house_10_planets]
            if "Sun" in names:
                career_text += "शासन, प्रशासन, नेतृत्व अथवा राजकीय सेवा के क्षेत्र अनुकूल हैं। "
            if "Mars" in names:
                career_text += "इंजीनियरिंग, तकनीकी, सैन्य सेवा, शल्य चिकित्सा या खेलकूद में सफलता। "
            if "Mercury" in names:
                career_text += "संचार, सूचना प्रौद्योगिकी (IT), लेखन, वाणिज्य अथवा व्यापार क्षेत्र। "
            if "Jupiter" in names:
                career_text += "शिक्षा, शिक्षण, विधि (कानून), वित्त अथवा परामर्श/सलाहकारिता। "
            if "Venus" in names:
                career_text += "कला, रचनात्मक क्षेत्र, मनोरंजन, मीडिया, सौंदर्य अथवा आतिथ्य सत्कार। "
            if "Saturn" in names:
                career_text += "कॉर्पोरेट प्रबंधन, लोक सेवा, उद्योग, निर्माण अथवा विनिर्माण क्षेत्र। "
            if "Rahu" in names:
                career_text += "आधुनिक तकनीक, बहुराष्ट्रीय कंपनियां (MNC) अथवा लीक से हटकर नए क्षेत्र। "
        elif house_10_data:
            lord_10 = LORDS_HI_MAP.get(house_10_data.get("lord", ""), house_10_data.get("lord", ""))
            career_text = (
                f"दशम भाव के स्वामी {lord_10} हैं। "
                f"करियर की दिशा {lord_10} की भाव स्थिति एवं ग्रह बल द्वारा निर्धारित होगी।"
            )
    else:
        if house_10_planets:
            names = [p["name"] for p in house_10_planets]
            career_text = f"Career house (10th) has {', '.join(names)}, suggesting "
            if "Sun" in names:
                career_text += "government, leadership, or authority roles. "
            if "Mars" in names:
                career_text += "engineering, military, surgery, or sports. "
            if "Mercury" in names:
                career_text += "communication, IT, writing, or commerce. "
            if "Jupiter" in names:
                career_text += "teaching, law, finance, or advisory roles. "
            if "Venus" in names:
                career_text += "arts, entertainment, luxury goods, or hospitality. "
            if "Saturn" in names:
                career_text += "corporate, government service, manufacturing, or mining. "
            if "Rahu" in names:
                career_text += "technology, foreign companies, or unconventional fields. "
        elif house_10_data:
            career_text = (
                f"10th house lord is {house_10_data['lord']}. "
                f"Career direction influenced by {house_10_data['lord']}'s placement and dignity."
            )
    reading["career"] = career_text

    # --- Relationship indicators ---
    house_7_planets = [p for p in planets if p["house"] == 7]
    venus = next((p for p in planets if p["name"] == "Venus"), None)
    rel_text = ""
    if language == "hi":
        if house_7_planets:
            names_hi = [LORDS_HI_MAP.get(p["name"], p.get("vedic_name", p["name"])) for p in house_7_planets]
            rel_text = f"सप्तम (विवाह व साझेदारी) भाव में {', '.join(names_hi)} स्थित हैं। "
        if venus:
            v_sign_hi = SIGNS_HI_MAP.get(venus["sign"], venus["sign"])
            rel_text += (
                f"शुक्र {v_sign_hi} में (भाव {venus['house']}) स्थित हैं। "
                f"{'शुक्र स्वराशि या उच्च के होने से दांपत्य जीवन में सुख और सौहार्द की वृद्धि होती है।' if venus.get('dignity') in ('exalted', 'own_sign') else 'वैवाहिक संबंधों में परस्पर समझ और धैर्य से प्रगाढ़ता आएगी।'}"
            )
    else:
        if house_7_planets:
            names = [p["name"] for p in house_7_planets]
            rel_text = f"Partnership house (7th) has {', '.join(names)}. "
        if venus:
            rel_text += (
                f"Venus is in {venus['sign']} (House {venus['house']}). "
                f"{'Venus is strong — good for relationships and harmony.' if venus.get('dignity') in ('exalted', 'own_sign') else 'Relationships benefit from patience and understanding.'}"
            )
    reading["relationships"] = rel_text

    # --- Summary ---
    if language == "hi":
        reading["summary"] = (
            f"इस कुण्डली में {len(yogas)} शुभ योग तथा "
            f"{len([d for d in doshas if d.get('present')])} सक्रिय दोष उपस्थित हैं। "
            f"समग्र रूप से, {'मजबूत ग्रह स्थितियों के साथ यह एक शुभ व सशक्त कुण्डली है' if len(strengths) > len(challenges) else 'चुनौतियों के समाधान और वैदिक उपायों द्वारा निरंतर उन्नति की संभावनाएं हैं'}।"
        )
    else:
        reading["summary"] = (
            f"This chart has {len(yogas)} yoga(s) and "
            f"{len([d for d in doshas if d.get('present')])} active dosha(s). "
            f"Overall, {'a well-supported chart with strong planetary placements' if len(strengths) > len(challenges) else 'a chart with growth opportunities through overcoming challenges'}."
        )

    return reading
