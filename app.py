import streamlit as st
import time
import random
import os

# --- 0. 系統配置 (手機版優化) ---
st.set_page_config(
    page_title="Kaolahan", 
    page_icon="🍲", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 1. 核心功能：全自動檔案搜尋系統 ---
@st.cache_resource
def index_audio_files():
    """
    自動掃描當前目錄下的所有資料夾，建立 {檔名: 完整路徑} 的對照表。
    解決路徑設定錯誤的問題。
    """
    audio_map = {}
    # 從當前目錄 (.) 開始往下掃描
    start_dir = "." 
    
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if file.lower().endswith(('.m4a', '.mp3')):
                # 將檔名 (如 kaolahan.m4a) 對應到 完整路徑
                audio_map[file.lower()] = os.path.join(root, file)
    
    return audio_map

# 初始化檔案索引
AUDIO_FILES_MAP = index_audio_files()

def play_audio(filename):
    """從索引中查找並播放音檔"""
    filename_key = filename.lower()
    
    if filename_key in AUDIO_FILES_MAP:
        full_path = AUDIO_FILES_MAP[filename_key]
        try:
            with open(full_path, "rb") as f:
                audio_bytes = f.read()
            st.audio(audio_bytes, format='audio/mp4')
        except Exception as e:
            st.error(f"讀取錯誤: {e}")
    else:
        st.warning(f"⚠️ 找不到: {filename}")
        # 除錯用：顯示按鈕讓老師知道程式沒找到
        st.caption("請確認檔名是否正確，或檔案是否已上傳")

def safe_rerun():
    try:
        st.rerun()
    except:
        st.stop()

# --- CSS 美化 (豐收暖橘 - 手機版) ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    
    .word-card {
        background: linear-gradient(135deg, #FFF3E0 0%, #ffffff 100%);
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 10px;
        border-bottom: 3px solid #FF7043;
    }
    .emoji-icon { font-size: 40px; margin-bottom: 5px; }
    .amis-text { font-size: 22px; font-weight: bold; color: #E64A19; }
    .chinese-text { font-size: 15px; color: #795548; }
    
    .sentence-box {
        background-color: #FFF8E1;
        border-left: 4px solid #FFA000;
        padding: 12px;
        margin: 8px 0;
        border-radius: 0 8px 8px 0;
    }

    .stButton>button {
        width: 100%; border-radius: 10px; font-size: 18px; font-weight: 600;
        background-color: #FFCCBC; color: #BF360C; border: 1px solid #FF7043; 
        padding: 10px; margin-top: 5px;
    }
    .stButton>button:hover { background-color: #FFAB91; }
    
    /* 隱藏除錯區塊的標題樣式 */
    .streamlit-expanderHeader { font-size: 14px; color: #888; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 資料庫 ---
vocab_data = [
    {"amis": "Kaolahan", "chi": "所喜歡的", "icon": "❤️", "source": "核心單字", "audio": "kaolahan.m4a"},
    {"amis": "Facidol", "chi": "麵包樹果", "icon": "🍈", "source": "食材", "audio": "facidol.m4a"},
    {"amis": "Haca", "chi": "也 / 亦", "icon": "➕", "source": "連接詞", "audio": "haca.m4a"},
    {"amis": "Maemin", "chi": "全部 / 所有的", "icon": "💯", "source": "數量", "audio": "maemin.m4a"},
    {"amis": "Sikaen", "chi": "菜餚 / 配菜", "icon": "🍱", "source": "食物", "audio": "sikaen.m4a"},
    {"amis": "Dateng", "chi": "菜 / 野菜", "icon": "🥬", "source": "食物", "audio": "dateng.m4a"},
    {"amis": "Kohaw", "chi": "湯", "icon": "🍲", "source": "食物", "audio": "kohaw.m4a"},
    {"amis": "Mato’asay", "chi": "老人 / 長輩", "icon": "👵", "source": "人物", "audio": "matoasay.m4a"},
]

sentences = [
    {"amis": "O maan ko kaolahan iso a sikaen?", "chi": "你喜歡什麼樣的菜呢？", "icon": "❓", "source": "問句", "audio": "sentence_01.m4a"},
    {"amis": "O foting ko kaolahan ako a dateng.", "chi": "魚是我最喜歡的菜。", "icon": "🐟", "source": "回答", "audio": "sentence_02.m4a"},
    {"amis": "Kaolahan no wama konini a kohaw.", "chi": "這碗是爸爸最喜歡的湯。", "icon": "👨", "source": "描述", "audio": "sentence_03.m4a"},
    {"amis": "Tadakaolahan no mato’asay kona dateng.", "chi": "這些是老人家最喜歡的菜。", "icon": "👵", "source": "描述", "audio": "sentence_04.m4a"},
    {"amis": "Kaolahan ako a maemin konini a sikaen.", "chi": "這些都是我最喜歡的菜餚。", "icon": "😋", "source": "感嘆", "audio": "sentence_05.m4a"},
    {"amis": "O facidol i, o tadakaolahan haca no ’Amis.", "chi": "麵包樹果也是阿美族人最愛。", "icon": "🍈", "source": "文化", "audio": "sentence_06.m4a"},
]

# --- 3. 隨機題庫 ---
raw_quiz_pool = [
    {"q": "「麵包樹果」的阿美語怎麼說？", "audio_file": "facidol.m4a", "options": ["Facidol", "Foting", "Dateng"], "ans": "Facidol", "hint": "阿美族人最愛的食材之一"},
    {"q": "O maan ko kaolahan iso a sikaen?", "audio_file": "sentence_01.m4a", "options": ["你喜歡什麼樣的菜呢？", "這是誰煮的菜？", "你要去哪裡買菜？"], "ans": "你喜歡什麼樣的菜呢？", "hint": "Maan 是「什麼」"},
    {"q": "Kaolahan no wama konini a kohaw.", "audio_file": "sentence_03.m4a", "options": ["這碗是爸爸最喜歡的湯", "這碗是媽媽煮的湯", "我不喜歡喝湯"], "ans": "這碗是爸爸最喜歡的湯", "hint": "Wama 是爸爸"},
    {"q": "單字測驗：Maemin", "audio_file": "maemin.m4a", "options": ["全部", "一點點", "沒有"], "ans": "全部", "hint": "Kaolahan ako a maemin"},
    {"q": "單字測驗：Mato’asay", "audio_file": "matoasay.m4a", "options": ["老人/長輩", "小孩", "年輕人"], "ans": "老人/長輩", "hint": "Tadakaolahan no mato’asay"},
    {"q": "O foting ko kaolahan ako a dateng.", "audio_file": "sentence_02.m4a", "options": ["魚是我最喜歡的菜", "我喜歡吃麵包樹果", "這道菜很鹹"], "ans": "魚是我最喜歡的菜", "hint": "Foting 是魚"},
    {"q": "「湯」的阿美語是？", "audio_file": "kohaw.m4a", "options": ["Kohaw", "Dateng", "Sapaiyo"], "ans": "Kohaw", "hint": "喝熱熱的 Kohaw"}
]

# --- 4. 狀態初始化 ---
if 'init' not in st.session_state:
    st.session_state.score = 0
    st.session_state.current_q_idx = 0
    
    selected_questions = random.sample(raw_quiz_pool, 4)
    final_questions = []
    for q in selected_questions:
        q_copy = q.copy()
        shuffled_opts = random.sample(q['options'], len(q['options']))
        q_copy['shuffled_options'] = shuffled_opts
        final_questions.append(q_copy)
        
    st.session_state.quiz_questions = final_questions
    st.session_state.init = True

# --- 5. 主介面 ---

st.markdown("<h2 style='text-align: center; color: #BF360C; margin-bottom: 0;'>Kaolahan 所喜歡的</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8D6E63; font-size: 14px;'>講師：高春美 | 教材提供者：高春美</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📖 詞彙與句型", "🎲 隨機挑戰"])

# === Tab 1: 學習模式 ===
with tab1:
    st.markdown("### 📝 核心單字")
    for word in vocab_data:
        st.markdown(f"""
        <div class="word-card">
            <div class="emoji-icon">{word['icon']}</div>
            <div class="amis-text">{word['amis']}</div>
            <div class="chinese-text">{word['chi']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"🔊 播放", key=f"btn_v_{word['amis']}"):
            play_audio(word['audio'])

    st.markdown("---")
    st.markdown("### 🗣️ 實用句型")
    for i, sent in enumerate(sentences):
        st.markdown(f"""
        <div class="sentence-box">
            <div style="font-size: 18px; color: #E65100; font-weight: bold;">{sent['icon']} {sent['amis']}</div>
            <div style="font-size: 15px; color: #5D4037; margin-top: 5px;">{sent['chi']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"▶️ 朗讀", key=f"btn_s_{i}"):
            play_audio(sent['audio'])

# === Tab 2: 測驗模式 ===
with tab2:
    st.markdown("### 🧠 隨機測驗")
    
    current_idx = st.session_state.current_q_idx
    questions = st.session_state.quiz_questions
    
    if current_idx < len(questions):
        q_data = questions[current_idx]
        progress = (current_idx / len(questions))
        st.progress(progress)
        
        st.markdown(f"**Q{current_idx + 1}: {q_data['q']}**")
        
        if q_data.get('audio_file'):
            if st.button("🔊 聽題目", key=f"quiz_audio_{current_idx}"):
                play_audio(q_data['audio_file'])
        
        st.write(" ")
        
        if f"answered_{current_idx}" not in st.session_state:
            for idx, opt in enumerate(q_data['shuffled_options']):
                if st.button(opt, key=f"opt_{current_idx}_{idx}"):
                    if opt == q_data['ans']:
                        st.session_state.score += 25
                        st.success(f"🎉 正確！")
                    else:
                        st.error(f"❌ 錯了！答案是：{q_data['ans']}")
                    
                    st.session_state[f"answered_{current_idx}"] = True
                    time.sleep(1.5)
                    st.session_state.current_q_idx += 1
                    safe_rerun()
        else:
            st.info("下一題...")
            
    else:
        st.progress(1.0)
        st.balloons()
        final_score = st.session_state.score
        
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background-color: #FFF3E0; border-radius: 15px; margin-top: 20px;">
            <h2 style="color: #E64A19;">測驗完成！</h2>
            <h1 style="font-size: 50px; color: #BF360C;">{final_score} 分</h1>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 再玩一次", type="primary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            safe_rerun()

# --- 6. 故障排除區 (如果還是不行，請點開這個) ---
with st.expander("🔧 故障排除 (如果沒聲音請點我)"):
    st.write("程式目前找到的音檔清單：")
    if not AUDIO_FILES_MAP:
        st.error("❌ 警告：程式完全找不到任何 .m4a 檔案！請確認檔案是否已上傳。")
    else:
        st.success(f"✅ 成功找到 {len(AUDIO_FILES_MAP)} 個音檔")
        st.json(AUDIO_FILES_MAP)
