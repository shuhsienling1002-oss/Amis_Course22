import streamlit as st
import time
import random
from io import BytesIO

# --- 1. 核心相容性修復 ---
def safe_rerun():
    """自動判斷並執行重整"""
    try:
        st.rerun()
    except AttributeError:
        try:
            st.experimental_rerun()
        except:
            st.stop()

def safe_play_audio(text):
    """語音播放安全模式"""
    try:
        from gtts import gTTS
        # 使用印尼語 (id) 發音
        tts = gTTS(text=text, lang='id')
        fp = BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')
    except Exception as e:
        st.caption(f"🔇 (語音生成暫時無法使用)")

# --- 0. 系統配置 ---
st.set_page_config(page_title="Unit 22: O Kakaenen", page_icon="🍚", layout="centered")

# --- CSS 美化 (美食暖色調) ---
st.markdown("""
    <style>
    body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .source-tag { font-size: 12px; color: #aaa; text-align: right; font-style: italic; }
    
    /* 單字卡 */
    .word-card {
        background: linear-gradient(135deg, #FFF3E0 0%, #ffffff 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 15px;
        border-bottom: 4px solid #FF9800;
    }
    .emoji-icon { font-size: 48px; margin-bottom: 10px; }
    .amis-text { font-size: 22px; font-weight: bold; color: #E65100; }
    .chinese-text { font-size: 16px; color: #7f8c8d; }
    
    /* 句子框 */
    .sentence-box {
        background-color: #FFF8E1;
        border-left: 5px solid #FFB74D;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }

    /* 按鈕 */
    .stButton>button {
        width: 100%; border-radius: 12px; font-size: 20px; font-weight: 600;
        background-color: #FFE0B2; color: #E65100; border: 2px solid #FF9800; padding: 12px;
    }
    .stButton>button:hover { background-color: #FFCC80; border-color: #F57C00; }
    .stProgress > div > div > div > div { background-color: #FF9800; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 資料庫 (Unit 22: Moedict Vocabulary) ---
vocab_data = [
    {"amis": "Kakaenen", "chi": "食物 / 糧食", "icon": "🍱", "source": "Moedict: kakaenen"},
    {"amis": "Hemay", "chi": "飯 / 米飯", "icon": "🍚", "source": "Moedict: hemay"},
    {"amis": "Nanom", "chi": "水", "icon": "💧", "source": "Moedict: nanom"},
    {"amis": "Titi", "chi": "肉", "icon": "🥩", "source": "Moedict: titi"},
    {"amis": "Dateng", "chi": "蔬菜 / 菜", "icon": "🥬", "source": "Moedict: dateng"},
    {"amis": "^epah", "chi": "酒", "icon": "🍶", "source": "CSV Row 517"}, # 修正
    {"amis": "Fita'ol", "chi": "蛋", "icon": "🥚", "source": "Moedict: fita'ol"},
    {"amis": "Heci", "chi": "果實 / 肉(果肉)", "icon": "🍎", "source": "Moedict: heci"},
    {"amis": "Komaen", "chi": "吃", "icon": "🥢", "source": "Moedict: komaen"},
    {"amis": "Minanom", "chi": "喝", "icon": "🥤", "source": "Moedict: minanom"},
    {"amis": "Miala", "chi": "拿 / 取", "icon": "🖐️", "source": "Moedict: miala"},
    {"amis": "Midimata'", "chi": "挑 / 扛 (重物)", "icon": "🏋️", "source": "Moedict: midimata'"},
    {"amis": "Macahiw", "chi": "餓", "icon": "😫", "source": "Moedict: macahiw"},
    {"amis": "Mafecol", "chi": "飽", "icon": "😌", "source": "CSV Row 1465"}, # 修正
]

# --- 句子庫 (7句: 嚴格源自 CSV 並移除連字號) ---
sentences = [
    {"amis": "Komaen ca mama to hemay.", "chi": "爸爸他們吃飯。", "icon": "🍚", "source": "Row 2 (Cleaned)"},
    {"amis": "Mafecolto kiso haw?", "chi": "你吃飽了嗎？", "icon": "😌", "source": "Row 1465 (Cleaned)"},
    {"amis": "Aka kakomaen to ^epah i papotal!", "chi": "不要在外面喝酒！", "icon": "🍶", "source": "Row 1837 (Cleaned)"},
    {"amis": "Minanom cangra.", "chi": "他們喝水。", "icon": "💧", "source": "Row 3 (Cleaned)"},
    {"amis": "Mialaay ko wawa to titi.", "chi": "小孩正在拿豬肉。", "icon": "🥩", "source": "Row 11 (Cleaned)"},
    {"amis": "O maan ko kakaenen iso?", "chi": "你要吃的是什麼? (你想吃什麼?)", "icon": "❓", "source": "Row 13 (Cleaned)"},
    {"amis": "Midimata' ca ina to kakaenen.", "chi": "媽媽他們挑著食物。", "icon": "🍱", "source": "Row 447 (Cleaned)"},
]

# --- 3. 隨機題庫 (Synced) ---
raw_quiz_pool = [
    {
        "q": "Mafecolto kiso haw?",
        "audio": "Mafecolto kiso haw",
        "options": ["你吃飽了嗎？", "你餓了嗎？", "你喝水了嗎？"],
        "ans": "你吃飽了嗎？",
        "hint": "Mafecol 是飽 (Row 1465)"
    },
    {
        "q": "Aka kakomaen to ^epah.",
        "audio": "Aka kakomaen to ^epah",
        "options": ["不要喝酒", "不要吃飯", "不要喝水"],
        "ans": "不要喝酒",
        "hint": "^epah 是酒 (Row 1837)"
    },
    {
        "q": "O maan ko kakaenen iso?",
        "audio": "O maan ko kakaenen iso",
        "options": ["你想吃什麼？", "你正在吃什麼？", "這是什麼食物？"],
        "ans": "你想吃什麼？",
        "hint": "Kakaenen (食物) (Row 13)"
    },
    {
        "q": "單字測驗：Dateng",
        "audio": "Dateng",
        "options": ["蔬菜", "肉", "蛋"],
        "ans": "蔬菜",
        "hint": "綠色的食物"
    },
    {
        "q": "單字測驗：Midimata'",
        "audio": "Midimata'",
        "options": ["挑/扛", "吃", "拿"],
        "ans": "挑/扛",
        "hint": "用肩膀扛東西 (Row 447)"
    },
    {
        "q": "單字測驗：Macahiw",
        "audio": "Macahiw",
        "options": ["餓", "飽", "渴"],
        "ans": "餓",
        "hint": "想吃東西的感覺"
    },
    {
        "q": "單字測驗：Titi",
        "audio": "Titi",
        "options": ["肉", "飯", "酒"],
        "ans": "肉",
        "hint": "豬肉、牛肉都是 Titi"
    },
    {
        "q": "單字測驗：^epah",  # 修正此處
        "audio": "^epah",
        "options": ["酒", "水", "茶"],
        "ans": "酒",
        "hint": "喝了會醉 (Moedict/CSV)"
    }
]

# --- 4. 狀態初始化 (洗牌邏輯) ---
if 'init' not in st.session_state:
    st.session_state.score = 0
    st.session_state.current_q_idx = 0
    st.session_state.quiz_id = str(random.randint(1000, 9999))
    
    # 抽題與洗牌
    selected_questions = random.sample(raw_quiz_pool, 3)
    final_questions = []
    for q in selected_questions:
        q_copy = q.copy()
        shuffled_opts = random.sample(q['options'], len(q['options']))
        q_copy['shuffled_options'] = shuffled_opts
        final_questions.append(q_copy)
        
    st.session_state.quiz_questions = final_questions
    st.session_state.init = True

# --- 5. 主介面 ---
st.markdown("<h1 style='text-align: center; color: #E65100;'>Unit 22: O Kakaenen</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>食物與飲食 (User Corrected)</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📚 詞彙與句型", "🎲 隨機挑戰"])

# === Tab 1: 學習模式 ===
with tab1:
    st.subheader("📝 核心單字")
    col1, col2 = st.columns(2)
    for i, word in enumerate(vocab_data):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class="word-card">
                <div class="emoji-icon">{word['icon']}</div>
                <div class="amis-text">{word['amis']}</div>
                <div class="chinese-text">{word['chi']}</div>
                <div class="source-tag">src: {word['source']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔊 聽發音", key=f"btn_vocab_{i}"):
                safe_play_audio(word['amis'])

    st.markdown("---")
    st.subheader("🗣️ 實用句型 (Data-Driven)")
    for i, s in enumerate(sentences):
        st.markdown(f"""
        <div class="sentence-box">
            <div style="font-size: 20px; font-weight: bold; color: #E65100;">{s['icon']} {s['amis']}</div>
            <div style="font-size: 16px; color: #555; margin-top: 5px;">{s['chi']}</div>
            <div class="source-tag">src: {s['source']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"▶️ 播放句型", key=f"btn_sent_{i}"):
            safe_play_audio(s['amis'])

# === Tab 2: 隨機挑戰模式 ===
with tab2:
    st.markdown("### 🎲 隨機評量")
    
    if st.session_state.current_q_idx < len(st.session_state.quiz_questions):
        q_data = st.session_state.quiz_questions[st.session_state.current_q_idx]
        
        st.progress((st.session_state.current_q_idx) / 3)
        st.markdown(f"**Question {st.session_state.current_q_idx + 1} / 3**")
        
        st.markdown(f"### {q_data['q']}")
        if q_data['audio']:
            if st.button("🎧 播放題目音檔", key=f"btn_audio_{st.session_state.current_q_idx}"):
                safe_play_audio(q_data['audio'])
        
        # 使用洗牌後的選項
        unique_key = f"q_{st.session_state.quiz_id}_{st.session_state.current_q_idx}"
        user_choice = st.radio("請選擇正確答案：", q_data['shuffled_options'], key=unique_key)
        
        if st.button("送出答案", key=f"btn_submit_{st.session_state.current_q_idx}"):
            if user_choice == q_data['ans']:
                st.balloons()
                st.success("🎉 答對了！")
                time.sleep(1)
                st.session_state.score += 100
                st.session_state.current_q_idx += 1
                safe_rerun()
            else:
                st.error(f"不對喔！提示：{q_data['hint']}")
                
    else:
        st.progress(1.0)
        st.markdown(f"""
        <div style='text-align: center; padding: 30px; background-color: #FFE0B2; border-radius: 20px; margin-top: 20px;'>
            <h1 style='color: #E65100;'>🏆 挑戰成功！</h1>
            <h3 style='color: #333;'>本次得分：{st.session_state.score}</h3>
            <p>你已經學會飲食相關用語了！</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 再來一局 (重新抽題)", key="btn_restart"):
            st.session_state.score = 0
            st.session_state.current_q_idx = 0
            st.session_state.quiz_id = str(random.randint(1000, 9999))
            
            new_questions = random.sample(raw_quiz_pool, 3)
            final_qs = []
            for q in new_questions:
                q_copy = q.copy()
                shuffled_opts = random.sample(q['options'], len(q['options']))
                q_copy['shuffled_options'] = shuffled_opts
                final_qs.append(q_copy)
            
            st.session_state.quiz_questions = final_qs
            safe_rerun()
